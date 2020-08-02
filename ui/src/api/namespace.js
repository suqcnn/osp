import request from '@/utils/request'

export function listNamespace(cluster) {
  return request({
    url: `namespace/${cluster}`,
    method: 'get',
  })
}
