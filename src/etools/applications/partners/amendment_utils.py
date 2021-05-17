import copy
import datetime
import decimal

from django.db.models.fields.files import FieldFile


def copy_m2m_relations(instance, instance_copy, relations, objects_map):
    for m2m_relation in relations:
        m2m_instances = getattr(instance, m2m_relation).all()
        objects_map[m2m_relation] = [i.pk for i in m2m_instances]
        getattr(instance_copy, m2m_relation).add(*m2m_instances)


def copy_simple_fields(instance, instance_copy, fields_map, exclude=None):
    exclude = exclude or []
    for field in instance._meta.get_fields():
        field_is_simple = not (field.many_to_many or field.many_to_one or field.one_to_many or field.one_to_one)
        if field.name not in exclude and field.concrete and field_is_simple and not field.auto_created:
            value = getattr(instance, field.name)
            setattr(instance_copy, field.name, value)

            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            elif isinstance(value, datetime.date):
                value = value.isoformat()
            elif isinstance(value, decimal.Decimal):
                value = value.to_eng_string()
            elif isinstance(value, FieldFile):
                value = value.name
            fields_map[field.name] = value


def merge_simple_fields(instance, instance_copy, fields_map, exclude=None):
    exclude = exclude or []
    for field in instance._meta.get_fields():
        field_is_simple = not (field.many_to_many or field.many_to_one or field.one_to_many or field.one_to_one)
        if field.name not in exclude and field.concrete and field_is_simple and not field.auto_created:
            if field.name not in fields_map:
                # field added after amendment created
                continue

            original_value = fields_map[field.name]
            current_value = getattr(instance, field.name)
            modified_value = getattr(instance_copy, field.name)

            # todo: field type should be checked better, not value
            if original_value:
                if isinstance(current_value, datetime.datetime):
                    original_value = datetime.datetime.fromisoformat(original_value)
                elif isinstance(current_value, datetime.date):
                    original_value = datetime.date.fromisoformat(original_value)
                elif isinstance(current_value, decimal.Decimal):
                    original_value = decimal.Decimal(original_value)
                elif isinstance(current_value, FieldFile):
                    # todo: compare code should be modified also
                    # original_value = original_value.name
                    continue

            if original_value == modified_value:
                # nothing changed
                continue

            if modified_value == current_value:
                # same field changes already performed
                continue

            if current_value != original_value:
                # value changed in both objects, cannot be merged automatically
                raise ValueError(f'field {field.name} was changed in both instances of {instance._meta.model_name}. '
                                 f'was {original_value}, now {current_value} and {modified_value}')

            setattr(instance, field.name, modified_value)

        # todo: figure out best place for saving
        instance.save()


def copy_one_to_many(instance, instance_copy, related_name, fields_map, relations_to_copy, exclude_fields, kwargs):
    related_field = [f for f in instance._meta.get_fields() if f.name == related_name][0]

    for item in getattr(instance, related_name).all():
        local_kwargs = copy.deepcopy(kwargs)
        if item._meta.label not in local_kwargs:
            local_kwargs[item._meta.label] = {}
        local_kwargs[item._meta.label][related_field.field.name] = instance_copy

        item_copy, copy_map = copy_instance(item, relations_to_copy, exclude_fields, local_kwargs)
        fields_map.append(copy_map)


def copy_instance(instance, relations_to_copy, exclude_fields, defaults):
    related_fields_to_copy = relations_to_copy.get(instance._meta.label, [])
    fields_to_exclude = exclude_fields.get(instance._meta.label, [])

    instance_copy = type(instance)(**defaults.get(instance._meta.label, {}))
    copy_map = {
        'original_pk': instance.pk,
    }
    copy_simple_fields(instance, instance_copy, copy_map, exclude=fields_to_exclude)

    for field in instance._meta.get_fields():
        if field.name in fields_to_exclude or field.name not in related_fields_to_copy:
            continue

        if field.many_to_one:
            # just set foreign key
            value = getattr(instance, field.name)
            setattr(instance_copy, field.name, value)
            copy_map[field.name] = value.pk if value else None

    instance_copy.save()
    copy_map['copy_pk'] = instance_copy.pk

    for field in instance._meta.get_fields():
        if field.name in fields_to_exclude or field.name not in related_fields_to_copy:
            continue

        if field.one_to_one:
            # full copy related instance (if exists use current one)
            # todo: implement copy if object not available
            # todo: not only simple fields can be required
            copy_map[field.name] = {}
            related_instance_copy = getattr(instance_copy, field.name)
            # todo: use exclude
            copy_simple_fields(getattr(instance, field.name), related_instance_copy, copy_map[field.name])
            related_instance_copy.save()

        if field.one_to_many:
            # copy all related instances
            copy_map[field.name] = []
            copy_one_to_many(instance, instance_copy, field.name, copy_map[field.name], relations_to_copy,
                             exclude_fields, defaults)

        if field.many_to_many:
            # link all related instances with copy
            copy_m2m_relations(instance, instance_copy, [field.name], copy_map)

    return instance_copy, copy_map


def merge_instance(instance, instance_copy, fields_map, relations_to_copy, exclude_fields):
    related_fields_to_copy = relations_to_copy.get(instance._meta.label, [])
    fields_to_exclude = exclude_fields.get(instance._meta.label, [])

    merge_simple_fields(instance, instance_copy, fields_map, exclude=fields_to_exclude)

    for field in instance._meta.get_fields():
        if field.name not in fields_map:
            # field added after amendment
            continue

        if field.many_to_one:
            value = fields_map[field.name]
            if value:
                original_value = field.related_model.objects.get(pk=value)
            else:
                original_value = None

            modified_value = getattr(instance_copy, field.name)
            current_value = getattr(instance, field.name)
            if original_value == modified_value:
                # nothing changed
                continue

            if modified_value == current_value:
                # same field changes already performed
                continue

            if current_value != original_value:
                # value changed in both objects, cannot be merged automatically
                raise ValueError(f'field {field.name} was changed in both instances of {instance._meta.model_name}. '
                                 f'was {original_value}, now {current_value} and {modified_value}')

            setattr(instance, field.name, modified_value)

    instance.save()

    for field in instance._meta.get_fields():
        if field.name in fields_to_exclude or field.name not in related_fields_to_copy:
            continue

        if field.one_to_one:
            # todo: if one of related objects is missing, raise error

            related_instance = getattr(instance, field.name)
            related_instance_copy = getattr(instance_copy, field.name)
            merge_simple_fields(
                related_instance,
                related_instance_copy,
                fields_map[field.name],
                exclude=exclude_fields.get(instance._meta.label, [])
            )

        if field.one_to_many:
            if field.name not in fields_map:
                continue

            for related_instance_data in fields_map[field.name]:
                related_instance = field.related_model.objects.filter(pk=related_instance_data['original_pk']).first()
                related_instance_copy = field.related_model.objects.filter(pk=related_instance_data['copy_pk']).first()
                if related_instance_copy:
                    if not related_instance:
                        # created
                        pass
                    else:
                        # update instance
                        pass
                elif related_instance:
                    # deleted
                    pass

        if field.many_to_many:
            if field.name not in fields_map:
                continue

            original_value = fields_map[field.name]
            modified_value = getattr(instance_copy, field.name).values_list('pk', flat=True)

            # no checks at this moment, so m2m fields can be edited in multiple amendments
            new_links = set(modified_value) - set(original_value)
            removed_links = set(original_value) - set(modified_value)
            getattr(instance, field.name).add(*new_links)
            getattr(instance, field.name).remove(*removed_links)


INTERVENTION_AMENDMENT_RELATED_FIELDS = {
    'partners.Intervention': [
        # one to many
        'result_links',
        'supply_items',
        'risks',

        # 1 to 1
        'planned_budget',
        'management_budgets',

        # many to one
        'agreement',
        'budget_owner',

        # many to many
        'country_programmes', 'unicef_focal_points', 'partner_focal_points',
        'sections', 'offices', 'flat_locations'
    ],
    'partners.InterventionResultLink': [
        # one to many
        'll_results',

        # many to many
        'ram_indicators',
    ],
    'partners.LowerResult': [
        # one to many
        'activities',
    ]
}
INTERVENTION_AMENDMENT_IGNORED_FIELDS = {
    'partners.Intervention': ['number', 'status', 'created', 'modified'],
    'partners.InterventionBudget': ['created', 'modified'],
    'partners.InterventionManagementBudget': ['created', 'modified'],
}
INTERVENTION_AMENDMENT_DEFAULTS = {
    'partners.Intervention': {
        'status': 'draft',
    }
}
