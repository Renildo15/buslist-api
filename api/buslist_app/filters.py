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

def apply_filters_notice(queryset, request):

    viewed = request.query_params.get("viewed")
    is_viewed = is_viewed_check(viewed)
    

    filter_params = {
        "buslist": request.query_params.get("buslist"),
        "viewed": is_viewed,
    }

    filter_params = {k: v for k, v in filter_params.items() if v is not None}
    queryset = queryset.filter(**filter_params)

    return queryset

def is_viewed_check(viewed):
    if viewed is not None and viewed == "true":
        return True
    elif viewed is not None and viewed == "false":
        return False
    return None