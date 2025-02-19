from django.db.models import Q


def apply_search(queryset, search_query):
    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )

    return queryset


def apply_search_notices(queryset, search_query):
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    return queryset


def apply_search_students(queryset, search_query):
    if search_query:
        queryset = queryset.filter(
            Q(student__first_name__icontains=search_query)
            | Q(student__username__icontains=search_query)
        )
    return queryset
