from .models import Attendee, ConferenceVO, AccountVO
from common.json import ModelEncoder


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {"conference": ConferenceVODetailEncoder()}

    def get_extra_data(self, o):
        count_objects = AccountVO.objects.filter(email=o.email).count()
        result = {}
        if count_objects > 0:
            result = {"has_account": True}
        else:
            result = {"has_account": False}
        return result
