import request from '@/utils/request'

export function listPods(cluster) {
  return request({
    url: `pods/${cluster}`,
    method: 'get',
  })
}

export function getPod(cluster, namespace, name, output='') {
  return request({
    url: `pods/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function deletePods(cluster, data) {
  return request({
    url: `pods/${cluster}/delete`,
    method: 'post',
    data: data
  })
}

export function updatePod(cluster, namespace, name, yaml) {
  return request({
    url: `pods/${cluster}/${namespace}/${name}`,
    method: 'post',
    data: { yaml }
  })
}
