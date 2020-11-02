import request from '@/utils/request'

export function listConfigMaps(cluster) {
  return request({
    url: `config_map/${cluster}`,
    method: 'get',
  })
}

export function getConfigMap(cluster, namespace, name, output='') {
  return request({
    url: `config_map/${cluster}/${namespace}/${name}`,
    method: 'get',
    params: { output }
  })
}

export function updateConfigMap(cluster, namespace, name, yaml) {
  return request({
    url: `config_map/${cluster}/update_config_map`,
    method: 'post',
    data: { yaml, name, namespace }
  })
}