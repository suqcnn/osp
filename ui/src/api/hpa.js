import request from '@/utils/request'

export function listHpas(cluster) {
  return request({
    url: `hpa/${cluster}`,
    method: 'get',
  })
}

export function getHpa(cluster, namespace, name, output='') {
  return request({
    url: `hpa/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function updateHpa(cluster, namespace, name, yaml) {
  return request({
    url: `hpa/${cluster}/update_hpa`,
    method: 'post',
    data: { yaml, name, namespace }
  })
}