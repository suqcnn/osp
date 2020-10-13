import request from '@/utils/request'

export function listStorageClass(cluster) {
  return request({
    url: `storage_class/${cluster}`,
    method: 'get',
  })
}

export function getStorageClass(cluster, name, output='') {
  return request({
    url: `storage_class/${cluster}/${name}`,
    method: 'get',
    params: { output }
  })
}