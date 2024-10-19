from django.db.models import Q


def apply_search(queryset, search_query):
    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )

    return queryset
