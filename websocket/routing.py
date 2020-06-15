from django.urls import path
from websocket.kubernetes.consumer import KubeConsumer

websocket_urlpatterns = [
    path('osp/kube/connect', KubeConsumer),
]
