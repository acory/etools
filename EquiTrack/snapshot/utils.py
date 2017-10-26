from __future__ import unicode_literals

from django.forms import model_to_dict
from rest_framework.utils import model_meta

from snapshot.models import Activity


def jsonify(data):
    for key, value in data.items():
        if type(value) not in [int, float, bool, str, dict]:
            data[key] = unicode(data[key])
    return data


def set_relation_values(obj, data):
    obj_dict = jsonify(model_to_dict(obj))
    instance_info = model_meta.get_field_info(obj.__class__)
    for field_name, relation_info in instance_info.relations.items():
        if relation_info.to_many:
            field = getattr(obj, field_name)
            obj_dict[field_name] = [x.pk for x in field.all()]
            if data is not None and data.get(field_name):
                data[field_name] = [x.pk for x in data[field_name]]

    return obj_dict, data


def create_change_dict(target_before, data):
    if target_before is not None:
        previous_obj_dict, data = set_relation_values(target_before, data)
        change = {}
        for k, v in data.items():
            if k in previous_obj_dict and data[k] != previous_obj_dict[k]:
                change.update({
                    k: {
                        "before": previous_obj_dict[k],
                        "after": data[k],
                    }
                })
        change = jsonify(change)
    else:
        change = ""

    return change


def create_snapshot(target, target_before, by_user, data):
    """If target_before is None, then action is create, otherwise update

    For to many relation fields add them to the target
    and use their pk for values
    """
    action = Activity.CREATE if target_before is None else Activity.UPDATE
    current_obj_dict, _ = set_relation_values(target, None)
    change = create_change_dict(target_before, data)

    activity = Activity.objects.create(
        target=target,
        by_user=by_user,
        action=action,
        data=current_obj_dict,
        change=change
    )

    return activity
