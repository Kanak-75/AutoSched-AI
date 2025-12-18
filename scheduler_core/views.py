from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from autosched_backend.settings import TIME_ZONE  # type: ignore
from backend.service import handle_natural_language_request
from scheduler_core.apps import scheduler


class ScheduleView(APIView):
    """
    POST /api/schedule/
    Body: { "text": "<natural language or JSON string for ScheduleRequest>" }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        natural_text = request.data.get("text")
        if not natural_text:
            return Response(
                {"error": "text field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule = handle_natural_language_request(natural_text, scheduler)

        return Response(schedule.model_dump(), status=status.HTTP_201_CREATED)


