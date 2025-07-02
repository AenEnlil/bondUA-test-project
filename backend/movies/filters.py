from django_filters import rest_framework as filters


class MovieFilter(filters.FilterSet):
    release_year = filters.NumberFilter()
    director = filters.NumberFilter(method='person_role_filter')
    actor = filters.NumberFilter(method='person_role_filter')

    def person_role_filter(self, queryset, role: str, person_id: int):
        return queryset.filter(movieperson__person_id=person_id, movieperson__role=role)
