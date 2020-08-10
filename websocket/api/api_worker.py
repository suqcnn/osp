import json
import logging
import threading
from queue import Queue

from service.kuberesource.watch import WatchResource
from service.middlemessage import MiddleMessage

logger = logging.getLogger(__name__)


class ApiWorker(threading.Thread):

    def __init__(self, ws, *args, **kwargs):
        self.queue = Queue(maxsize=1000)
        self.ws = ws
        self.has_stopped = False
        self.cluster_worker = ClusterWorker(ws)
        super().__init__(*args, **kwargs)

    def put_ws_action(self, data):
        self.queue.put(data)

    def run(self):
        try:
            while not self.has_stopped:
                data = self.queue.get()
                if data != 0 and isinstance(data, dict):
                    if data.get('action') == 'watchCluster':
                        cluster = data.get('params').get('cluster')
                        if self.cluster_worker.is_alive():
                            self.cluster_worker.stop()
                        self.cluster_worker.set_cluster(cluster)
                        self.cluster_worker.start()
        except Exception as exc:
            logger.error("run worker error: %s" % exc, exc_info=True)
        logger.info('api worker stopped')

    def stop(self):
        self.cluster_worker.stop()
        self.has_stopped = True
        self.put_stop()
        logger.info('api worker stopped success')

    def put_stop(self):
        self.queue.put(0)


class ClusterWorker(threading.Thread):

    def __init__(self, ws, cluster='', *args, **kwargs):
        self.ws = ws
        self.cluster = cluster
        self.has_stopped = False
        self.middle_message = MiddleMessage()
        super().__init__(*args, **kwargs)

    def set_cluster(self, cluster):
        self.cluster = cluster

    def run(self):
        if self.cluster:
            watch_resource = WatchResource(self.cluster)
            res = watch_resource.open_watch()
            if res.is_success():
                while not self.has_stopped:
                    try:
                        for res in self.middle_message.get_watch(self.cluster):
                            try:
                                self.ws.send(json.dumps(res))
                            except Exception as exc:
                                logger.error('send request error: %s' % exc, exc_info=True)
                    except Exception as exc:
                        if not self.stop:
                            logger.error('get request error: %s' % exc, exc_info=True)
                            self.middle_message.close_pubsub()
            else:
                self.ws.send(json.dumps(res.to_json()))
        logger.info('cluster handler stopped')

    def stop(self):
        self.has_stopped = True
        self.middle_message.close_pubsub()
        if self.cluster:
            watch_resource = WatchResource(self.cluster)
            watch_resource.close_watch()
        logger.info("cluster worker stopped success")
