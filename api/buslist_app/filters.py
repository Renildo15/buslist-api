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
    is_viewed = boolean_check(viewed)

    filter_params = {
        "buslist": request.query_params.get("buslist"),
        "viewed": is_viewed,
    }

    filter_params = {k: v for k, v in filter_params.items() if v is not None}
    queryset = queryset.filter(**filter_params)

    return queryset


def apply_filters_students(queryset, request):

    student_return = request.query_params.get("return")
    is_return = boolean_check(student_return)
    institution_id = request.query_params.get("institution")

    filter_params = {}

    if is_return is not None:
        filter_params["is_return"] = is_return
    if institution_id:
        filter_params["student__studentprofile__institution_id"] = institution_id
    queryset = queryset.filter(**filter_params)

    return queryset


def boolean_check(boolean):
    if boolean is not None and boolean == "true":
        return True
    elif boolean is not None and boolean == "false":
        return False
    return None
