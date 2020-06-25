from request.middleware import RequestMiddleware


class StatisticMiddleware(RequestMiddleware):
    def process_response(self, request, response):
        if request.META.get("HTTP_ACCEPT_LANGUAGE", "") == "":
            return response
        return super().process_response(request, response)
