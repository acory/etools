import json

from collections import OrderedDict

from vision.vision_data_synchronizer import VisionDataSynchronizer
from vision.utils import wcf_json_date_as_datetime, comp_decimals
from funds.models import Grant, Donor
from audit.models import PurchaseOrder, AuditorFirm


class POSynchronizer(VisionDataSynchronizer):

    ENDPOINT = 'GetPurchaseOrderInfo_JSON'
    REQUIRED_KEYS = (
        "PO_NUMBER",
        "PO_DATE",
        "EXPIRY_DATE",
        "VENDOR_CODE",
        "VENDOR_NAME",
        "VENDOR_CTRY_NAME",
        "DONOR_NAME",
        "GRANT_REF",
    )

    MAPPING = {
        'order': {
            "order_number": "PO_NUMBER",
            "contract_start_date": "PO_DATE",
            "auditor_firm": "VENDOR_CODE",
        },
        'auditor_firm': {
            "vendor_number": "VENDOR_CODE",
            "name": "VENDOR_NAME",
            "country": "VENDOR_CTRY_NAME",
        },
        'grant': {
            "name": "GRANT_REF",
            "expiry": "EXPIRY_DATE",
            "donor": "DONOR_NAME"
        },
        'donor': {
            "name": "DONOR_NAME",
        }
    }
    MODEL_MAPPING = OrderedDict({
        'donor': Donor,
        'grant': Grant,
        'auditor_firm': AuditorFirm,
        'order': PurchaseOrder,
    })
    DATE_FIELDS = ['EXPIRY_DATE', 'PO_DATE', ]

    def _convert_records(self, records):
        if isinstance(records, list):
            return records
        return json.loads(records)

    def _filter_records(self, records):
        records = super(POSynchronizer, self)._filter_records(records)

        def bad_record(record):
            if not record['VENDOR_NAME']:
                return False
            return True

        return filter(bad_record, records)

    def _save_records(self, records):
        processed = 0

        filtered_records = self._filter_records(records)

        def _get_field_value(field_name, field_json_code, json_item, model):
            if field_json_code in self.DATE_FIELDS:
                return wcf_json_date_as_datetime(json_item[field_json_code])
            elif field_name in self.MODEL_MAPPING.keys():
                related_model = self.MODEL_MAPPING[field_name]

                reversed_dict = dict(zip(self.MAPPING[field_name].values(), self.MAPPING[field_name].keys()))
                return related_model.objects.get(**{
                    reversed_dict[field_json_code]: json_item.get(field_json_code, None)
                })
            return json_item[field_json_code]

        def _process_record(json_item):
            try:
                for model_name, model in self.MODEL_MAPPING.items():
                    mapped_item = dict(
                        [(field_name, _get_field_value(field_name, field_json_code, json_item, model)) \
                         for field_name, field_json_code in self.MAPPING[model_name].items()]
                    )
                    kwargs = dict(
                        [(field_name, value) for field_name, value in mapped_item.items() \
                         if model._meta.get_field(field_name).unique]
                    )
                    defaults = dict(
                        [(field_name, value) for field_name, value in mapped_item.items() \
                         if field_name not in kwargs.keys()]
                    )
                    obj, created = model.objects.update_or_create(
                        defaults=defaults, **kwargs
                    )
            except Exception as exp:
                    print ("Exception message: {} ")
                    print ("Exception type: {} ")
                    print ("Exception args: {} ".format(
                            exp.message, type(exp).__name__, exp.args
                        ))

        for record in filtered_records:
            _process_record(record)
            processed += 1
        return processed
