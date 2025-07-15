from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import BaseModel

from application.usecase.deals.delete_deal import DeleteDealUseCase
from infra.http.controller import AbstractHttpController


class DeleteDealController(AbstractHttpController):
    def __init__(self, usecase: DeleteDealUseCase) -> None:
        super().__init__()
        self.usecase = usecase

    def perform(
        self,
        request: HttpRequest,
        validated: BaseModel | None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        deal_id = kwargs.get("deal_id")
        if deal_id is None:
            return JsonResponse({"error": "Missing deal_id in URL"}, status=400)
        success = self.usecase.execute(deal_id=deal_id)
        if not success:
            return JsonResponse({"error": "Deal not found"}, status=404)
        return JsonResponse({"success": True})
