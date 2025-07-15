from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.usecase.deals.create_deal import CreateDealUseCase
from application.usecase.deals.delete_deal import DeleteDealUseCase
from application.usecase.deals.get_all_deals import GetAllDealsUseCase
from application.usecase.deals.get_deal_by_id import GetDealByIdUseCase
from application.usecase.deals.update_deal import UpdateDealUseCase
from infra.db.deal.db_repository import DealRepositoryDB

from .serializers import (
    DealCreateSerializer,
    DealIdSerializer,
    DealSerializer,
    DealUpdateSerializer,
)

# Instantiate the repository
deal_repository = DealRepositoryDB()


class DealListCreateView(APIView):
    """API view for listing all deals and creating a new deal."""

    list_usecase: GetAllDealsUseCase = GetAllDealsUseCase(deal_repository)
    create_usecase: CreateDealUseCase = CreateDealUseCase(deal_repository)

    def get(self, request: Request) -> Response:
        """List all deals."""
        deals = self.list_usecase.execute()
        return Response({"deals": [DealSerializer(d).data for d in deals]})  # type: ignore

    def post(self, request: Request) -> Response:
        """Create a new deal."""
        serializer = DealCreateSerializer(data=request.data)
        if serializer.is_valid():
            deal = self.create_usecase.execute(**serializer.validated_data)
            return Response(
                DealSerializer(deal).data,  # type: ignore
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,  # type: ignore
            status=status.HTTP_400_BAD_REQUEST,
        )


class DealDetailView(APIView):
    """API view for retrieving, updating, and deleting a deal by id."""

    get_usecase: GetDealByIdUseCase = GetDealByIdUseCase(deal_repository)
    update_usecase: UpdateDealUseCase = UpdateDealUseCase(deal_repository)
    delete_usecase: DeleteDealUseCase = DeleteDealUseCase(deal_repository)

    def get(self, request: Request, deal_id: int) -> Response:
        """Retrieve a deal by id."""
        serializer = DealIdSerializer(data={"deal_id": deal_id})
        if serializer.is_valid():
            deal = self.get_usecase.execute(deal_id=serializer.validated_data["deal_id"])
            if deal is None:
                return Response(
                    {"error": "Deal not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(DealSerializer(deal).data)  # type: ignore
        return Response(
            serializer.errors,  # type: ignore
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request: Request, deal_id: int) -> Response:
        """Update a deal by id."""
        serializer = DealUpdateSerializer(data={**request.data, "deal_id": deal_id})
        if serializer.is_valid():
            deal = self.update_usecase.execute(**serializer.validated_data)
            if deal is None:
                return Response(
                    {"error": "Deal not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(DealSerializer(deal).data)  # type: ignore
        return Response(
            serializer.errors,  # type: ignore
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request: Request, deal_id: int) -> Response:
        """Delete a deal by id."""
        serializer = DealIdSerializer(data={"deal_id": deal_id})
        if serializer.is_valid():
            success = self.delete_usecase.execute(
                deal_id=serializer.validated_data["deal_id"]
            )
            if not success:
                return Response(
                    {"error": "Deal not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({"success": True})
        return Response(
            serializer.errors,  # type: ignore
            status=status.HTTP_400_BAD_REQUEST,
        )
