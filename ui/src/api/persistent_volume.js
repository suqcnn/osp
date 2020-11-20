import request from '@/utils/request'

export function listPersistentVolume(cluster) {
  return request({
    url: `pv/${cluster}`,
    method: 'get',
  })
}

export function getPersistentVolume(cluster, name, output='') {
  return request({
    url: `pv/${cluster}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function updatePersistentVolume(cluster, name, yaml) {
  return request({
    url: `pv/${cluster}/${name}`,
    method: 'post',
    data: { yaml }
  })
}