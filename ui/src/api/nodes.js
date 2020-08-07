import request from '@/utils/request'

export function listNodes(cluster) {
  return request({
    url: `nodes/${cluster}`,
    method: 'get',
  })
}
