import math

from rest_framework.filters import BaseFilterBackend


def calculateDistance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))
    )


class CustomDistanceFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        alluser = queryset
        new_queryset = []
        distparam = request.GET.get('distance')
        if distparam and bool(int(distparam)):
            for user in alluser:
                current_user_long = request.user.longitude
                current_user_lat = request.user.latitude
                alluser_long = user.longitude
                alluser_lat = user.latitude
                distance = calculateDistance(current_user_lat, current_user_long, alluser_lat, alluser_long,)
                if distance < int(distparam):
                    new_queryset.append(user)
            return new_queryset
        return queryset
