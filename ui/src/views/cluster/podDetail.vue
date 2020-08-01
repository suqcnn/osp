<template>
  <div>
    <clusterbar :titleName="titleName" />
    <div class="dashboard-container">
      <!-- <div class="dashboard-text"></div> -->
      <el-table
        :data="pod.containers"
        class="table-fix"
        tooltip-effect="dark"
        style="width: 100%"
        v-loading="loading"
        :default-sort = "{prop: 'name'}"
        >
        <el-table-column
          prop="name"
          label="名称"
          min-width="200"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="image"
          label="镜像"
          min-width="100"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="restarts"
          label="重启"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          label=""
          show-overflow-tooltip
          min-width="40">
          <template slot-scope="scope">
            <!-- <el-link :underline="false"
              @click.native.prevent="deleteRow(scope.$index, tableData)">
              <svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" />
            </el-link> -->
            <el-dropdown size="medium" >
              <el-link :underline="false"><svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" /></el-link>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native.prevent="deleteRow(scope.$index, tableData)">日志</el-dropdown-item>
                <el-dropdown-item>终端</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { getPod } from '@/api/pods'
import { Message } from 'element-ui'

export default {
  name: 'PodDetail',
  components: {
    Clusterbar
  },
  data() {
    return {
      loading: true,
      originPod: [],
    }
  },
  created() {
    this.fetchData()
  },
  computed: {
    titleName: function() {
      return ['Pods', this.podName]
    },
    podName: function() {
      return this.$route.params ? this.$route.params.podName : ''

    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    pod: function() {
      return {
        containers: [{
          name: "test",
          image: "centos",
          restarts: 2,
          create_time: "2020-08-01 20:27:32",
          status: "running"
        }]
      }
    },
  },
  methods: {
    fetchData: function() {
      this.originPods = []
      this.loading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        this.loading = false
        return
      }
      if (!this.namespace) {
        Message.error("获取命名空间参数异常，请刷新重试")
        this.loading = false
        return
      }
      if (!this.podName) {
        Message.error("获取Pod名称参数异常，请刷新重试")
        this.loading = false
        return
      }
      getPod(cluster, this.namespace, this.podName).then(response => {
        this.loading = false
        this.originPod = response.data
      }).catch(() => {
        this.loading = false
      })
    },
    buildPods: function(pod) {
      if (!pod) return
      let containers = []
      for (let c of pod.spec.containers) {
        let bc = this.buildContainer(c, pod.status.containerStatuses)
        console.log(bc)
        containers.push(bc)
      }
      let init_containers = []
      if (pod.spec.initContainers) {
        for (let c of pod.spec.initContainers) {
          init_containers.push(this.buildContainer(c, pod.status.containerStatuses))
        }
      }
      let controlled = ''
      if (pod.metadata.ownerReferences.length > 0) {
        controlled = pod.metadata.ownerReferences[0].kind
      }
      let p = {
        uid: pod.metadata.uid,
        name: pod.metadata.name,
        namespace: pod.metadata.namespace,
        containers: containers,
        init_containers: init_containers,
        controlled: controlled,
        qos: pod.status.qosClass,
        status: pod.status.phase,
        ip: pod.status.podIP,
        created: pod.metadata.creationTimestamp,
        node_name: pod.spec.nodeName,
        resource_version: pod.metadata.resourceVersion,
      }
      console.log(p)
      return p
    },
    buildContainer: function(container, statuses) {
      if (!container) return {}
      if (!statuses) return {}
      let c = {name: container.name, status: 'unknown', restarts: 0}
      for (let s of statuses) {
        if (s.name == container.name) {
          c.restarts = s.restartCount
          if (s.state.running) c.status = 'running'
          else if (s.state.terminated) c.status = 'terminated'
          else if (s.state.waiting) c.status = 'waiting'
          c.ready = s.ready
          break
        }
      }
      return c
    },
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 10px 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }

  .table-fix {
    height: calc(100% - 100px);
  }
}

</style>
