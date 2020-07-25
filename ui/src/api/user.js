import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/token',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

export function adminSet(data) {
  return request({
    url: '/user/admin',
    method: 'post',
    data
  })
}

export function hasAdmin() {
  return request({
    url: '/has_admin',
    method: 'get',
  })
}
