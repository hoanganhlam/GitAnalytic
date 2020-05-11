import requests
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyC1Oag_e1x8FECR7ESzNouS7kUENzKHE2s')


def google_map_geo_coding(search):
    if search:
        # Geocoding an address
        results = gmaps.geocode(search, language="en")
        return results
    return None


def reverse_geocode_geo_coding(location):
    if location:
        # Geocoding an address
        results = gmaps.reverse_geocode(location, language="en")
        return results
    return None


def google_map_autocomplete(search):
    if search:
        # Geocoding an address
        results = gmaps.places_autocomplete(search, language="en")
        return results
    return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_inner(array, array2):
    for i in array:
        if i in array2:
            return True
    return False


def get_address(search):
    response = gmaps.places(query=search)
    return response


def get_place_photos(queries):
    photo_reference = queries.get('search')
    response = gmaps.places_photo(photo_reference=photo_reference, max_width=1000, max_height=1000)
    print(response)
    return response


def get_places_nearby(queries):
    search = queries.get('search')
    page_token = queries.get('page_token')
    response = gmaps.places_nearby(location=search, radius=1500, page_token=page_token)
    return response


def get_place(ids):
    return gmaps.place(ids, language="en")
