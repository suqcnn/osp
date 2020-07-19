import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
//   {
//     path: '/login',
//     component: () => import('@/views/login/index'),
//     hidden: true
//   },
  
//   {
//     path: '/404',
//     component: () => import('@/views/404'),
//     hidden: true
//   },
  
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'cluster',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '集群', icon: 'cluster' }
    }]
  },

  {
    path: '/node',
    component: Layout,
    children: [{
      path: 'node',
      name: 'Node',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '节点', icon: 'node' }
    }]
  },
  
  {
    path: '/workloads',
    component: Layout,
    redirect: '/workloads/detail',
    name: 'workloads',
    meta: { title: '工作负载', icon: 'workloads' },
    children: [
      {
        path: 'detail',
        name: 'detail',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '概览' }
      },
      {
        path: 'pods',
        name: 'pods',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '容器组' }
      },
      {
        path: 'deployments',
        name: 'deployments',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '无状态' }
      },
      {
        path: 'statefulsets',
        name: 'statefulsets',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '有状态' }
      },
      {
        path: 'daemonsets',
        name: 'daemonsets',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '守护进程集' }
      },
      {
        path: 'job',
        name: 'job',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '任务' }
      },
      {
        path: 'cronjob',
        name: 'cronjob',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '定时任务' }
      }
    ]
  },
  
  {
    path: '/configuration',
    component: Layout,
    redirect: '/configuration/configmaps',
    name: 'configuration',
    meta: { title: '应用配置', icon: 'configuration' },
    children: [
      {
        path: 'configmaps',
        name: 'configmaps',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '配置项' }
      },
      {
        path: 'secrets',
        name: 'secrets',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '保密字典' }
      },
      {
        path: 'hpa',
        name: 'hpa',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '水平扩缩容' }
      },
    ]
  },
  
  {
    path: '/network',
    component: Layout,
    redirect: '/network/services',
    name: 'network',
    meta: { title: '网络', icon: 'network' },
    children: [
      {
        path: 'services',
        name: 'services',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '服务' }
      },
      {
        path: 'ingress',
        name: 'ingress',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '路由' }
      },
      {
        path: 'networkpolicies',
        name: 'networkpolicies',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '网络策略' }
      },
    ]
  },
  
  {
    path: '/storage',
    component: Layout,
    redirect: '/storage/pvc',
    name: 'storage',
    meta: { title: '存储', icon: 'storage' },
    children: [
      {
        path: 'pvc',
        name: 'pvc',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '存储声明' }
      },
      {
        path: 'pv',
        name: 'pv',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '存储卷' }
      },
      {
        path: 'storageclass',
        name: 'storageclass',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '存储类' }
      },
    ]
  },

  {
    path: '/namespace',
    component: Layout,
    children: [{
      path: 'namespace',
      name: 'namespace',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '命名空间', icon: 'namespace' }
    }]
  },
]

const createRouter = () => new Router({
    // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})
  
const router = createRouter()
  
// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}
  
export default router
