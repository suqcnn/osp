/* Layout */
import Layout from '@/layout'

const Routes = [{
  path: '/settings/cluster',
  component: Layout,
  // redirect: '/dashboard',
  children: [{
      path: '',
      name: 'settinsCluster',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '集群管理', icon: 'settings_cluster', 'side': 'settings' }
    }]
  },
]

export default Routes
