from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse

from application.usecase.deals.get_all_deals import GetAllDealsUseCase
from infra.http.controller import AbstractHttpController


class GetAllDealsController(AbstractHttpController):
    def __init__(self, usecase: GetAllDealsUseCase) -> None:
        super().__init__()
        self.usecase = usecase

    def handle(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        deals = self.usecase.execute()
        return JsonResponse({"deals": [{"id": d.id, "title": d.title} for d in deals]})
