import request from '@/utils/request'

export function listPods(cluster) {
  return request({
    url: `pods/${cluster}`,
    method: 'get',
  })
}

export function getPod(cluster, namespace, name) {
  return request({
    url: `pods/${cluster}/${namespace}/${name}`,
    method: 'get',
  })
}
