import request from '@/utils/request'

export function listCluster() {
  return request({
    url: '/cluster',
    method: 'get',
  })
}

export function createCluster(data) {
  return request({
    url: '/cluster',
    method: 'post',
    data,
  })
}

export function clusterDetail(cluster) {
  return request({
    url: `/cluster/${cluster}/detail`,
    method: 'get',
  })
}
