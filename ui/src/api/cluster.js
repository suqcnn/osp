import request from '@/utils/request'

export function listCluster() {
  return request({
    url: '/cluster',
    method: 'get',
  })
}
