from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class HomeDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "title": "Witaj w Nerdiary API",
            "description": "Backend dla projektu zadesignowany pod frontend w Reactie.",
            "features": [
                "Bezpieczne wpisy",
                "Automatyczne API",
                "Dokumentacja Swagger"
            ]
        })