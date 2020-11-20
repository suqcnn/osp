import request from '@/utils/request'

export function listPersistentVolumeClaim(cluster) {
  return request({
    url: `pvc/${cluster}`,
    method: 'get',
  })
}

export function getPersistentVolumeClaim(cluster, namespace, name, output='') {
  return request({
    url: `pvc/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function updatePersistentVolumeClaim(cluster, namespace, name, yaml) {
  return request({
    url: `pvc/${cluster}/${namespace}/${name}`,
    method: 'post',
    data: { yaml }
  })
}