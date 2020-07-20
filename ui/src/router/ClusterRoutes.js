/* Layout */
import Layout from '@/layout'

const Routes = [
  {
    path: '/cluster/:name',
    component: Layout,
    // redirect: '/dashboard',
    children: [
    {
      path: '',
      name: 'cluster',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '集群', icon: 'cluster' }
    }]
  },

  {
    path: '/cluster/:name/node',
    component: Layout,
    children: [{
      path: '',
      name: 'node',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '节点', icon: 'node' }
    }]
  },
    
  {
    path: '/cluster/:name/workloads',
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
    path: '/cluster/:name/configuration',
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
    path: '/cluster/:name/network',
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
    path: '/cluster/:name/storage',
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
    path: '/cluster/:name/namespace',
    component: Layout,
    children: [{
        path: '',
        name: 'namespace',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '命名空间', icon: 'namespace' }
    }]
  },
]

export default Routes
