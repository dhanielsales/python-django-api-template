from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from django.http import HttpRequest, HttpResponse
from pydantic import BaseModel, ValidationError
from rest_framework import status

# Type variable for the Pydantic schema used in the controller
SchemaT = TypeVar("SchemaT", bound=BaseModel, default=BaseModel)


class AbstractHttpController(Generic[SchemaT], ABC):
    """Abstract base class for HTTP controllers."""

    def __init__(self, schema: type[SchemaT] | None = None) -> None:
        """Initialize the controller with an optional Pydantic schema."""
        self.schema = schema

    @abstractmethod
    def perform(
        self,
        request: HttpRequest,
        validated: SchemaT | None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """Perform the HTTP request after validation. Must be implemented by subclasses.

        Signature matches Django view, with validated data.
        """
        pass

    def handle(
        self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        """Handle the HTTP request: validate input, then call perform."""
        data = request.POST.dict()
        validated: SchemaT | None = None
        if self.schema is not None:
            try:
                validated = self.schema.model_validate(data)
            except ValidationError as e:
                from django.http import JsonResponse

                return JsonResponse(
                    {"errors": e.errors()}, status=status.HTTP_400_BAD_REQUEST
                )
        return self.perform(request, validated, *args, **kwargs)

    def validate(self, data: dict[str, object]) -> SchemaT | None:
        """Validate the input data using the provided Pydantic schema.

        Raises ValidationError if validation fails.
        """
        if self.schema is None:
            return None
        if hasattr(self.schema, "model_validate"):
            return self.schema.model_validate(data)
        return self.schema(**data)
