from django.http import JsonResponse
from events.encoders import (
    LocationListEncoder,
    LocationDetailEncoder,
    ConferenceListEncoder,
    ConferenceDetailEncoder,
)
from .models import Conference, Location
from django.views.decorators.http import require_http_methods
import json
from events.models import State
from .acls import get_photo, get_weather_data


@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    """
    Lists the conference names and the link to the conference.
    Returns a dictionary with a single key "conferences" which
    is a list of conference names and URLS. Each entry in the list
    is a dictionary that contains the name of the conference and
    the link to the conference's information.
    {
        "conferences": [
            {
                "name": conference's name,
                "href": URL to the conference,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            conferences,
            encoder=ConferenceListEncoder,
            safe=False,
        )
    elif request.method == "POST":
        content = json.loads(request.body)
        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_conference(request, id):
    """
    Returns the details for the Conference model specified
    by the id parameter.

    This should return a dictionary with the name, starts,
    ends, description, created, updated, max_presentations,
    max_attendees, and a dictionary for the location containing
    its name and href.

    {
        "name": the conference's name,
        "starts": the date/time when the conference starts,
        "ends": the date/time when the conference ends,
        "description": the description of the conference,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "max_presentations": the maximum number of presentations,
        "max_attendees": the maximum number of attendees,
        "location": {
            "name": the name of the location,
            "href": the URL for the location,
        }
    }
    """
    if request.method == "GET":
        conference = Conference.objects.get(id=id)
        weather_data_object = get_weather_data(
            conference.location.city, conference.location.state.name
        )
        return JsonResponse(
            {"conference": conference, "weather": weather_data_object},
            encoder=ConferenceDetailEncoder,
            safe=False,
        )

    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    elif request.method == "PUT":
        content = json.loads(request.body)
        Conference.objects.filter(id=id).update(**content)
        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    """
    Lists the location names and the link to the location.
    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.
    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """
    # response = []
    # locations = Conference.objects.all()
    # for location in locations:
    #     response.append(
    #         {
    #             "name": location.name,
    #             "href": location.get_api_url(),
    #         }
    #     )
    #   return JsonResponse({"locations": response})
    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations},
            encoder=LocationListEncoder,
        )
    else:
        content = json.loads(request.body)
        # Update your code to look up the State
        #  based on the value in the content dictionary in the "state" key.
        # Then, assign it back to the dictionary.
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
            # get photo buraya geliyor

        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid State abbreviation"},
                status=400,
            )
        photo = get_photo(content["city"], content["state"].abbreviation)
        content.update(photo)

        location = Location.objects.create(**content)
        return JsonResponse(
            {"locations": location},
            encoder=LocationDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, id):
    """
    Returns the details for the Location model specified
    by the id parameter.
    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.
    # Burada state abbreviation i donmeni istiyor.
    # state i degil (turu State class i)
    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        # Python custom class lari (senin models te
         olusturdugun class lari) nasil JSON a donusturecegini henuz bilmiyor.
        location.state yazinca, oradaki statein turu State class i.
        O nedenle JSON class i str e donusturmuyor.
        "state": the two-letter abbreviation for the state,
    }
    """
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    # Convert the submitted JSON-formatted string into a dictionary.
    # Convert the state abbreviation into a State, if it exists.
    # Use that dictionary to update the existing Location.
    # Return the updated Location object.
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
    # weather = get_weather_data(content)


#    photo = get_photo(content["city"], content["state"].abbreviation)
#         content.update(photo)
