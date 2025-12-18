from django.http import HttpResponse
from django.views import View
from pathlib import Path


class FrontendView(View):
    """Serves the frontend HTML file"""

    def get(self, request):
        frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        with open(frontend_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HttpResponse(html_content, content_type="text/html")

