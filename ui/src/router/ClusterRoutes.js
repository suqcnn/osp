/* Layout */
import Layout from '@/layout'
import { Noop } from '@/layout/components'

const Routes = [
  {
    path: '',
    name: 'cluster',
    component: () => import('@/views/cluster/cluster'),
    meta: { title: '集群', icon: 'cluster', group: 'cluster' },
  },

  {
    path: 'node',
    name: 'node',
    component: () => import('@/views/cluster/node'),
    meta: { title: '节点', icon: 'node', group: 'cluster' },
  },

  {
    path: 'workloads',
    component: Noop,
    name: 'workloads',
    meta: { title: '工作负载', icon: 'workloads', group: 'cluster' },
    children: [
      {
        path: 'detail',
        name: 'detail',
        component: () => import('@/views/dashboard/index'),
        meta: { title: '概览', group: 'cluster' },
      },
      {
        path: 'pods',
        name: 'pods',
        component: () => import('@/views/cluster/pod'),
        meta: { title: '容器组', group: 'cluster' },
      },
      {
        path: 'pods/:namespace/:podName',
        name: 'podsDetail',
        hidden: true,
        component: () => import('@/views/cluster/podDetail'),
        meta: { title: '容器组', group: 'cluster', sideName: 'pods' },
      },
      {
        path: 'deployments',
        name: 'deployments',
        component: () => import('@/views/cluster/deployment'),
        meta: { title: '无状态', group: 'cluster' },
      },
      {
        path: 'deployments/:namespace/:deploymentName',
        name: 'deploymentDetail',
        hidden: true,
        component: () => import('@/views/cluster/deploymentDetail'),
        meta: { title: '无状态', group: 'cluster', sideName: 'deployments' },
      },
      {
        path: 'statefulsets',
        name: 'statefulsets',
        component: () => import('@/views/cluster/statefulset'),
        meta: { title: '有状态', group: 'cluster' }
      },
      {
        path: 'statefulsets/:namespace/:statefulsetName',
        name: 'statefulsetDetail',
        hidden: true,
        component: () => import('@/views/cluster/statefulsetDetail'),
        meta: { title: '有状态', group: 'cluster', sideName: "statefulsets" }
      },
      {
        path: 'daemonsets',
        name: 'daemonsets',
        component: () => import('@/views/cluster/daemonset'),
        meta: { title: '守护进程集', group: 'cluster' }
      },
      {
        path: 'daemonsets/:namespace/:daemonsetName',
        name: 'daemonsetDetail',
        hidden: true,
        component: () => import('@/views/cluster/daemonsetDetail'),
        meta: { title: '守护进程集', group: 'cluster', sideName: "daemonsets" }
      },
      {
        path: 'job',
        name: 'job',
        component: () => import('@/views/cluster/job'),
        meta: { title: '任务', group: 'cluster' },
      },
      {
        path: 'job/:namespace/:jobName',
        name: 'jobDetail',
        hidden: true,
        component: () => import('@/views/cluster/jobDetail'),
        meta: { title: '任务', group: 'cluster', sideName: "job" }
      },
      {
        path: 'cronjob',
        name: 'cronjob',
        component: () => import('@/views/cluster/cronjob'),
        meta: { title: '定时任务', group: 'cluster' }
      },
      {
        path: 'cronjob/:namespace/:cronjobName',
        name: 'cronjobDetail',
        hidden: true,
        component: () => import('@/views/cluster/cronjobDetail'),
        meta: { title: '定时任务', group: 'cluster', sideName: "cronjob" }
      },
    ]
  },

  {
    path: 'configuration',
    component: Noop,
    name: 'configuration',
    meta: { title: '应用配置', icon: 'configuration', group: 'cluster' },
    children: [
      {
        path: 'configmaps',
        name: 'configmaps',
        component: () => import('@/views/cluster/configMap'),
        meta: { title: '配置项', group: 'cluster' },
      },
      {
        path: 'configmaps/:namespace/:configMapName',
        name: 'configMapDetail',
        hidden: true,
        component: () => import('@/views/cluster/configMapDetail'),
        meta: { title: '配置项', group: 'cluster', sideName: 'configmaps' },
      },
      {
        path: 'secrets',
        name: 'secrets',
        component: () => import('@/views/cluster/secret'),
        meta: { title: '保密字典', group: 'cluster' },
      },
      {
        path: 'secrets/:namespace/:secretName',
        name: 'secretDetail',
        hidden: true,
        component: () => import('@/views/cluster/secretDetail'),
        meta: { title: '配置项', group: 'cluster', sideName: 'secrets' },
      },
      {
        path: 'hpa',
        name: 'hpa',
        component: () => import('@/views/cluster/hpa'),
        meta: { title: '水平扩缩容', group: 'cluster' },
      },
    ],
  },

  {
    path: 'network',
    component: Noop,
    name: 'network',
    meta: { title: '网络', icon: 'network', group: 'cluster' },
    children: [
      {
        path: 'services',
        name: 'services',
        component: () => import('@/views/cluster/service'),
        meta: { title: '服务', group: 'cluster' },
      },
      {
        path: 'services/:namespace/:serviceName',
        name: 'serviceDetail',
        hidden: true,
        component: () => import('@/views/cluster/serviceDetail'),
        meta: { title: '服务', group: 'cluster', sideName: 'services' },
      },
      {
        path: 'ingress',
        name: 'ingress',
        component: () => import('@/views/cluster/ingress'),
        meta: { title: '路由', group: 'cluster' },
      },
      {
        path: 'ingress/:namespace/:ingressName',
        name: 'ingressDetail',
        hidden: true,
        component: () => import('@/views/cluster/ingressDetail'),
        meta: { title: '路由', group: 'cluster', sideName: 'ingress' },
      },
      {
        path: 'networkpolicies',
        name: 'networkpolicies',
        component: () => import('@/views/cluster/networkpolicy'),
        meta: { title: '网络策略', group: 'cluster' },
      },
    ],
  },

  {
    path: 'storage',
    component: Noop,
    name: 'storage',
    meta: { title: '存储', icon: 'storage', group: 'cluster' },
    children: [
      {
        path: 'pvc',
        name: 'pvc',
        component: () => import('@/views/cluster/persistentVolumeClaim'),
        meta: { title: '存储声明', group: 'cluster' },
      },
      {
        path: 'pvc/:namespace/:persistentVolumeClaimName',
        name: 'pvcDetail',
        hidden: true,
        component: () => import('@/views/cluster/persistentVolumeClaimDetail'),
        meta: { title: '配置项', group: 'cluster', sideName: 'pvc' },
      },
      {
        path: 'pv',
        name: 'pv',
        component: () => import('@/views/cluster/persistentVolume'),
        meta: { title: '存储卷', group: 'cluster' }
      },
      {
        path: 'pv/:persistentVolumeName',
        name: 'pvDetail',
        hidden: true,
        component: () => import('@/views/cluster/persistentVolumeDetail'),
        meta: { title: '配置项', group: 'cluster', sideName: 'pv' },
      },
      {
        path: 'storageclass',
        name: 'storageclass',
        component: () => import('@/views/cluster/storageClass'),
        meta: { title: '存储类', group: 'cluster' },
      },
    ],
  },

  {
    path: 'namespace',
    name: 'namespace',
    component: () => import('@/views/cluster/namespace'),
    meta: { title: '命名空间', icon: 'namespace', group: 'cluster' },
  },
  {
    path: 'event',
    name: 'event',
    component: () => import('@/views/cluster/event'),
    meta: { title: '事件', icon: 'event', group: 'cluster' },
  },
  {
    path: 'rbac',
    component: Noop,
    name: 'rbac',
    meta: { title: '访问控制', icon: 'security', group: 'cluster' },
    children: [
      {
        path: 'serviceaccount',
        name: 'serviceaccount',
        component: () => import('@/views/cluster/serviceaccount'),
        meta: { title: '服务账户', group: 'cluster' },
      },
      {
        path: 'serviceaccount/:namespace/:serviceaccountName',
        name: 'serviceaccountDetail',
        hidden: true,
        component: () => import('@/views/cluster/serviceaccountDetail'),
        meta: { title: '服务账户', group: 'cluster', sideName: 'serviceaccount' },
      },
      {
        path: 'rolebinding',
        name: 'rolebinding',
        component: () => import('@/views/cluster/rolebinding'),
        meta: { title: '角色绑定', group: 'cluster' },
      },
      {
        path: 'rolebinding/:rolebindingName',
        name: 'clusterrolebindingDetail',
        hidden: true,
        component: () => import('@/views/cluster/rolebindingDetail'),
        meta: { title: '角色绑定', group: 'cluster', sideName: 'rolebinding' },
      },
      {
        path: 'rolebinding/:namespace/:rolebindingName',
        name: 'rolebindingDetail',
        hidden: true,
        component: () => import('@/views/cluster/rolebindingDetail'),
        meta: { title: '角色绑定', group: 'cluster', sideName: 'rolebinding' },
      },
      {
        path: 'role',
        name: 'role',
        component: () => import('@/views/cluster/role'),
        meta: { title: '角色', group: 'cluster' },
      },
      {
        path: 'role/:roleName',
        name: 'clusterroleDetail',
        hidden: true,
        component: () => import('@/views/cluster/roleDetail'),
        meta: { title: '角色绑定', group: 'cluster', sideName: 'role' },
      },
      {
        path: 'role/:namespace/:roleName',
        name: 'roleDetail',
        hidden: true,
        component: () => import('@/views/cluster/roleDetail'),
        meta: { title: '角色绑定', group: 'cluster', sideName: 'role' },
      },
    ]
  },
]

const clusterRoutes = [
  {
    path: 'cluster/:name',
    component: Layout,
    hidden: true,
    children: Routes,
    meta: { group: 'cluster' },
  },
]

export default clusterRoutes
