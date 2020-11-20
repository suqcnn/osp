import request from '@/utils/request'

export function listStorageClass(cluster) {
  return request({
    url: `storageclass/${cluster}`,
    method: 'get',
  })
}

export function getStorageClass(cluster, name, output='') {
  return request({
    url: `storageclass/${cluster}/${name}`,
    method: 'get',
    params: { output }
  })
}