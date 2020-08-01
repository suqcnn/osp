<template>
  <div>
    <clusterbar titleName="Pod" :nsFunc="nsSearch" :nameFunc="nameSearch" />
    <div class="dashboard-container">
      <!-- <div class="dashboard-text"></div> -->
      <el-table
        ref="multipleTable"
        :data="pods"
        class="table-fix"
        tooltip-effect="dark"
        :max-height="maxHeight"
        style="width: 100%"
        v-loading="loading"
        :default-sort = "{prop: 'name'}"
        >
        <el-table-column
          type="selection"
          width="45">
        </el-table-column>
        <el-table-column
          prop="name"
          label="名称"
          min-width="200"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="namespace"
          label="命名空间"
          min-width="100"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="containerNum"
          label="容器"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="restarts"
          label="重启"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="controlled"
          label="控制器"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="qos"
          label="QoS"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="created"
          label="时长"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          show-overflow-tooltip>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { listPods } from '@/api/pods'
import { Message } from 'element-ui'

export default {
  name: 'Pod',
  components: {
    Clusterbar
  },
  data() {
      return {
        maxHeight: window.innerHeight - 150,
        loading: true,
        originPods: [],
        search_ns: [],
        search_name: '',
      }
  },
  created() {
    this.fetchData()
  },
  mounted() {
    const that = this
    // let heightStyle = that.$refs.tableCot.offsetHeight
    // that.maxHeight = heightStyle
    window.onresize = () => {
      return (() => {
        let heightStyle = window.innerHeight - 150
        console.log(heightStyle)
        that.maxHeight = heightStyle
      })()
    }
  },
  watch: {
    podsWatch: function (newObj) {
      console.log("watch pod obj", newObj)
      if (newObj) {
        let newUid = newObj.resource.metadata.uid
        let newRv = newObj.resource.metadata.resourceVersion
        if (newObj.event === 'add') {
          this.originPods.push(this.buildPods(newObj.resource))
        } else if (newObj.event === 'update') {
          for (let i in this.originPods) {
            let p = this.originPods[i]
            if (p.uid === newUid && p.resource_version < newRv) {
              let newPod = this.buildPods(newObj.resource)
              this.$set(this.originPods, i, newPod)
              console.log(newPod.status)
              break
            }
          }
        } else if (newObj.event === 'delete') {
          this.originPods = this.originPods.filter(( { uid } ) => uid !== newUid)
        }
      }
    }
  },
  computed: {
    pods: function() {
      let plist = []
      for (let p of this.originPods) {
        if (this.search_ns.length > 0 && this.search_ns.indexOf(p.namespace) < 0) continue
        if (this.search_name && !p.name.includes(this.search_name)) continue
        p['containerNum'] = p.containers.length
        if (p.init_containers){
          p['containerNum'] += p.init_containers.length
        }
        p['restarts'] = 0
        for (let c of p.containers) {
          if (c.restarts > p['restarts']) {
            p['restarts'] = c.restarts
          }
        }
        plist.push(p)
      }
      return plist
    },
    podsWatch: function() {
      return this.$store.getters["ws/podWatch"]
    }
  },
  methods: {
    fetchData: function() {
      this.loading = true
      this.originPods = []
      const cluster = this.$store.state.cluster
      if (cluster) {
        listPods(cluster).then(response => {
          this.loading = false
          this.originPods = response.data
        }).catch(() => {
          this.loading = false
        })
      } else {
        this.loading = false
        Message.error("获取集群异常，请刷新重试")
      }
    },
    nsSearch: function(vals) {
      this.search_ns = []
      for(let ns of vals) {
        this.search_ns.push(ns)
      }
    },
    nameSearch: function(val) {
      console.log(val)
      this.search_name = val
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
    }
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

    .scrollbar-wrapper {
      overflow-x: hidden !important;
    }
    .el-scrollbar__bar.is-vertical {
      right: 0px;
    }

    .el-scrollbar {
      height: 100%;
    }
</style>
