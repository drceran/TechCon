from .models import Presentation
from common.json import ModelEncoder

# These classes- I copy pasted to the presentations/api_views. So I do not need this anymore, actually.
class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
    ]


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference",
    ]
