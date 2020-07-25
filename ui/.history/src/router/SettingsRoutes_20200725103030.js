/* Layout */
import Layout from '@/layout'

const Routes = [
  {
    path: 'overview',
    name: 'overview',
    component: () => import('@/views/overview'),
    meta: { title: '总览', icon: 'overview', 'group': 'settings' }
  },
  {
    path: 'cluster',
    name: 'settinsCluster',
    component: () => import('@/views/dashboard/index'),
    meta: { title: '集群管理', icon: 'settings_cluster', 'group': 'settings' }
  },
]

const settingsRoutes = [{
  path: 'settings',
  component: Layout,
  hidden: true,
  children: Routes
}]

export default settingsRoutes
