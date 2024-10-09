def apply_filters_users(queryset, request):
    filter_params = {
        'is_student': request.query_params.get("is_student"),
        'is_driver': request.query_params.get("is_driver"),
        'studentprofile__institution__acronym': request.query_params.get("institution"),
        'studentprofile__sex': request.query_params.get("sex"),
        'studentprofile__status': request.query_params.get("status"),
        'studentprofile__teaching_level': request.query_params.get("teaching_level"),
    }

    filter_params = {k: v for k, v in filter_params.items() if v is not None}

    queryset = queryset.filter(**filter_params)

    return queryset
