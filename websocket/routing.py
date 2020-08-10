from django.urls import path, re_path

from websocket.api.consumer import ApiConsumer, ExecConsumer, LogConsumer
from websocket.kubernetes.consumer import KubeConsumer

websocket_urlpatterns = [
    path('osp/kube/connect', KubeConsumer),
    path('osp/api/connect', ApiConsumer),
    re_path('osp/api/exec/(?P<cluster>[^/.]+)/(?P<namespace>[^/.]+)/(?P<pod>[^/.]+)', ExecConsumer),
    re_path('osp/api/log/(?P<cluster>[^/.]+)/(?P<namespace>[^/.]+)/(?P<pod>[^/.]+)', LogConsumer),
]
