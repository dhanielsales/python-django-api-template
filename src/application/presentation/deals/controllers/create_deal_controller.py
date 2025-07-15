from decimal import Decimal
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import BaseModel

from application.usecase.deals.create_deal import CreateDealUseCase
from infra.http.controller import AbstractHttpController


class CreateDealSchema(BaseModel):
    """Pydantic schema for creating a deal."""

    title: str
    company_id: int
    value: Decimal
    tags: list[int] | None = None
    distributor_id: int | None = None


class CreateDealController(AbstractHttpController[CreateDealSchema]):
    """Controller for creating a deal."""

    def __init__(self, usecase: CreateDealUseCase) -> None:
        """Initialize with the create deal use case."""
        super().__init__(schema=CreateDealSchema)
        self.usecase = usecase

    def perform(
        self,
        request: HttpRequest,
        validated: CreateDealSchema | None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """Perform the HTTP request to create a deal after validation."""
        if validated is None:
            return JsonResponse({"error": "Invalid data"}, status=400)
        deal = self.usecase.execute(
            title=validated.title,
            company_id=validated.company_id,
            value=validated.value,
            tags=validated.tags,
            distributor_id=validated.distributor_id,
        )
        return JsonResponse({"id": deal.id, "title": deal.title})
