from django.urls import path

from websocket.api.consumer import ApiConsumer
from websocket.kubernetes.consumer import KubeConsumer

websocket_urlpatterns = [
    path('osp/kube/connect', KubeConsumer),
    path('osp/api/connect', ApiConsumer),
]
