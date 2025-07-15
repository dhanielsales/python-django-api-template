from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse

from infra.http.controller import AbstractHttpController


class CreateDealController(AbstractHttpController):
    """Controller for creating a deal."""

    def handle(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        """Handle the HTTP request to create a deal."""
        # TODO: Implement the logic for creating a deal
        return JsonResponse(
            {"message": "CreateDealController not implemented"}, status=501
        )
