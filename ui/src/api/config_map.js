import request from '@/utils/request'

export function listConfigMaps(cluster) {
  return request({
    url: `config_map/${cluster}`,
    method: 'get',
  })
}

export function getConfigMap(cluster, namespace, name, output='') {
  return request({
    url: `config_map/${cluster}/${namespace}`,
    method: 'get',
    params: { output, name }
  })
}