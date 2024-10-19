def apply_filters_bus_list(queryset, request):
    filter_params = {
        "list_date": request.query_params.get("list_date"),
        "shift": request.query_params.get("shift"),
        "type_creation": request.query_params.get("type_creation"),
        "is_enable": request.query_params.get("is_enable"),
    }

    filter_params = {k: v for k, v in filter_params.items() if v is not None}
    queryset = queryset.filter(**filter_params)

    return queryset
