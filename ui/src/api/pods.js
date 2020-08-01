import request from '@/utils/request'

export function listPods(cluster) {
  return request({
    url: `pods/${cluster}`,
    method: 'get',
  })
}
