#!/usr/bin/env python
# coding: utf-8

import logging
from rest_framework import viewsets

from api.views import api_decorator
from service.kuberesource.node import NodeResource

logger = logging.getLogger(__name__)


class NodeViewSet(viewsets.GenericViewSet):

    @api_decorator('List Nodes', serializer_class=None)
    def list(self, req):
        pod_resource = NodeResource(req.get("cluster"))
        res = pod_resource.list()
        if not res.data:
            res.data = []
        return res
