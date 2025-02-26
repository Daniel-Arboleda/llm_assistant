from django.http import JsonResponse
from django.views import View

# Vista de prueba
class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({"status": "ok", "message": "Orchestrator API is running"}, status=200)

# Vista de orquestación (ejemplo)
class OrchestrateRequestView(View):
    def get(self, request):
        # Aquí puedes hacer una solicitud a otro microservicio (ejemplo)
        response_data = {"message": "Orchestrator received the request and is processing"}
        return JsonResponse(response_data, status=200)
