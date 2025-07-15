from decimal import Decimal
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import BaseModel, ValidationError

from application.usecase.deals.update_deal import UpdateDealUseCase
from infra.http.controller import AbstractHttpController


class UpdateDealSchema(BaseModel):
    deal_id: int
    title: str | None = None
    distributor_id: int | None = None
    tags: list[int] | None = None
    value: Decimal | None = None


class UpdateDealController(AbstractHttpController):
    def __init__(self, usecase: UpdateDealUseCase) -> None:
        super().__init__(schema=UpdateDealSchema)
        self.usecase = usecase

    def handle(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        try:
            data = self.validate(
                request.POST.dict() if request.method == "POST" else request.GET.dict()
            )
        except ValidationError as e:
            return JsonResponse({"errors": e.errors()}, status=400)
        deal = self.usecase.execute(
            deal_id=data.deal_id,
            title=data.title,
            distributor_id=data.distributor_id,
            tags=data.tags,
            value=data.value,
        )
        if deal is None:
            return JsonResponse({"error": "Deal not found"}, status=404)
        return JsonResponse({"id": deal.id, "title": deal.title})
