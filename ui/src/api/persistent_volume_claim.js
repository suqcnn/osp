import request from '@/utils/request'

export function listPersistentVolumeClaim(cluster) {
  return request({
    url: `persistent_volume_claim/${cluster}`,
    method: 'get',
  })
}

export function getPersistentVolumeClaim(cluster, namespace, name, output='') {
  return request({
    url: `persistent_volume_claim/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function updatePersistentVolumeClaim(cluster, namespace, name, yaml) {
  return request({
    url: `persistent_volume_claim/${cluster}/${namespace}/${name}`,
    method: 'post',
    data: { yaml }
  })
}