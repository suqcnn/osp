import request from '@/utils/request'

export function listPersistentVolume(cluster) {
  return request({
    url: `persistent_volume/${cluster}`,
    method: 'get',
  })
}

export function getPersistentVolume(cluster, namespace, name, output='') {
  return request({
    url: `persistent_volume/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}