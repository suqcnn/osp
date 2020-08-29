import request from '@/utils/request'

export function listConfigMaps(cluster) {
  return request({
    url: `config_map/${cluster}`,
    method: 'get',
  })
}

