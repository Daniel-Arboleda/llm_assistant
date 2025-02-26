from django.urls import path
from api.views import HealthCheckView, OrchestrateRequestView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('orchestrate/', OrchestrateRequestView.as_view(), name='orchestrate-request'),
]
