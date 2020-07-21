/* Layout */
import Layout from '@/layout'

const Routes = [
  {
    path: 'cluster',
    name: 'settinsCluster',
    component: () => import('@/views/dashboard/index'),
    meta: { title: '集群管理', icon: 'settings_cluster', 'group': 'settings' }
  },
]

const settingsRoutes = [{
  path: '/settings',
  component: Layout,
  hidden: true,
  children: Routes
}]

export default settingsRoutes
