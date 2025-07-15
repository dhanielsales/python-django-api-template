from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import BaseModel, ValidationError

from application.usecase.deals.get_deal_by_id import GetDealByIdUseCase
from infra.http.controller import AbstractHttpController


class GetDealByIdSchema(BaseModel):
    deal_id: int


class GetDealByIdController(AbstractHttpController):
    def __init__(self, usecase: GetDealByIdUseCase) -> None:
        super().__init__(schema=GetDealByIdSchema)
        self.usecase = usecase

    def handle(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        try:
            data = self.validate(request.GET.dict())
        except ValidationError as e:
            return JsonResponse({"errors": e.errors()}, status=400)
        deal = self.usecase.execute(deal_id=data.deal_id)
        if deal is None:
            return JsonResponse({"error": "Deal not found"}, status=404)
        return JsonResponse({"id": deal.id, "title": deal.title})
