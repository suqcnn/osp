<template>
  <div>
    <div class="dashboard-container">
      <el-row :gutter="20" style="margin-bottom: 10px;" class="row-class">
        <el-col :span="24">
          <div class="border-class">
            <div style="margin: 5px 0px 10px;">集群状态</div>
            <el-row :gutter="5">
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Cluster Version</div>
                  <div style="text-align: center; padding-top: 55px; font-size: 20px;">{{ cluster_detail.cluster_version }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 67px;">
                  <div style="text-align: center; font-size: 13px">CPU</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.cluster_cpu }}</div>
                </el-card>
                <el-card shadow="never" style="height: 67px; margin-top: 6px;">
                  <div style="text-align: center; font-size: 13px;">Memory</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.cluster_memory }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Node</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.node_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Namespace</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.namespace_num }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="10" style="margin-bottom: 10px;" class="row-class">
        <el-col :span="12">
          <div class="border-class">
            <div style="margin: 5px 0px 10px;">应用状态</div>
            <el-row :gutter="5">
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Pod</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.pod_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 64px; color: #409EFF; margin-top: 3px;">
                  <div style="text-align: center; font-size: 13px">Running</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.pod_running_num }}</div>
                </el-card>
                <el-card shadow="never" style="height: 64px; margin-top: 6px; color: #E6A23C;">
                  <div style="text-align: center; font-size: 13px;">Pending</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.pod_pending_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 64px; color: #67C23A; margin-top: 3px;">
                  <div style="text-align: center; font-size: 13px">Succeeded</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.pod_succeeded_num }}</div>
                </el-card>
                <el-card shadow="never" style="height: 64px; margin-top: 6px; color: #F56C6C">
                  <div style="text-align: center; font-size: 13px;">Failed</div>
                  <div style="text-align: center; padding-top: 10px;">{{ cluster_detail.pod_failed_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px; font-size: 13px;">Deployment</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.deployment_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px; font-size: 13px;">StatefulSet</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.statefulset_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px; font-size: 13px;">DaemonSet</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.daemonset_num }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-col>

        <el-col :span="4">
          <div class="border-class">
            <div style="margin: 5px 0px 10px;">网络状态</div>
            <el-row :gutter="5">
              
              <el-col :span="12">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Service</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.service_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Ingress</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.ingress_num }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-col>

        <el-col :span="8">
          <div class="border-class">
            <div style="margin: 5px 0px 10px;">存储状态</div>
            <el-row :gutter="5">
              <el-col :span="6">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">Storage Class</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.storageclass_num }}</div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-row :gutter="5" style="margin-bottom: 6px; margin-top: 3px;">
                  <el-col :span="12">
                    <el-card shadow="never" style="height: 45px; color: #409EFF;">
                      <div style="text-align: center; font-size: 13px; margin-top: -3px;">Available</div>
                      <div style="text-align: center; padding-top: 1px;">{{ cluster_detail.pv_available_num }}</div>
                    </el-card>
                    <el-card shadow="never" style="height: 45px; color: #67C23A; margin-top: 6px;">
                      <div style="text-align: center; font-size: 13px; margin-top: -3px;">Bound</div>
                      <div style="text-align: center; padding-top: 1px;">{{ cluster_detail.pv_bound_num }}</div>
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card shadow="never" style="height: 45px; color: #E6A23C;">
                      <div style="text-align: center; font-size: 13px; margin-top: -3px;">Released</div>
                      <div style="text-align: center; padding-top: 1px;">{{ cluster_detail.pv_released_num }}</div>
                    </el-card>
                    <el-card shadow="never" style="height: 45px; color: #F56C6C; margin-top: 6px;">
                      <div style="text-align: center; font-size: 13px; margin-top: -3px;">Failed</div>
                      <div style="text-align: center; padding-top: 1px;">{{ cluster_detail.pv_failed_num }}</div>
                    </el-card>
                  </el-col>
                </el-row>
                <el-card shadow="never" style="height: 30px">
                  <div style="text-align: center; margin-top: -5px;">
                    <span style="float: left; margin-left: 30px;">PV</span>
                    <span style="float: right; margin-right: 30px;">{{ cluster_detail.pv_num }}</span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="never" style="height: 140px">
                  <div style="text-align: center; height: 20px;">PVC</div>
                  <div style="text-align: center; padding-top: 59px;">{{ cluster_detail.pvc_num }}</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>

      <el-row>
        <div class="border-class event-class">
          <div style="margin: 5px 0px 10px;">事件</div>
          <!-- <div style="margin: auto; text-align: center; color: #909399;">暂无事件</div> -->
          <el-timeline>
            <template v-for="e of events">
              <el-timeline-item :key="e.uid" :timestamp="e.event_time" placement="top">
                <el-card shadow="never">
                  <p class="event-title">{{ e.object.kind }}/{{ e.object.name }}</p>
                  <p class="event-body">{{ e.message }}</p>
                </el-card>
              </el-timeline-item>
            </template>
            <!-- <el-timeline-item timestamp="2020-10-19T15:00:19Z" placement="top">
            <el-card shadow="never">
                <p class="event-title">HorizontalPodAutoscaler/nginx-deployment</p>
                <p class="event-body">missing request for cpu</p>
            </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="2020-10-19T14:59:28Z" placement="top">
            <el-card shadow="never">
                <p class="event-title">PersistentVolumeClaim/test-pvc2</p>
                <p class="event-body">waiting for first consumer to be created before binding</p>
            </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="2020-10-19T14:59:28Z" placement="top">
            <el-card shadow="never">
                <p class="event-title">PersistentVolumeClaim/test-ttt</p>
                <p class="event-body">no persistent volumes available for this claim and no storage class is set</p>
            </el-card>
            </el-timeline-item> -->
          </el-timeline>
        </div>
      </el-row>
    </div>
  </div>
</template>

<script>
import { clusterDetail } from '@/api/cluster'
import { listEvents } from '@/api/event'

export default {
  name: 'cluster',
  data() {
    return {
      cluster_detail: {},
      originEvents: [],
    }
  },
  components: {
  },
  created() {
    this.fetchData()
  },
  computed: {
    events: function() {
      let dlist = []
      for (let p of this.originEvents) {
        // if (this.search_ns.length > 0 && this.search_ns.indexOf(p.namespace) < 0) continue
        // if (this.search_name && !p.name.includes(this.search_name)) continue
    
        dlist.push(p)
      }
      dlist.sort((a, b) => {
        return a.event_time < b.event_time ? 1 : -1
      })
      return dlist
    },
  },
  methods: {
    fetchData: function() {
      this.loading = true
      this.originCronJobs = []
      const cluster = this.$store.state.cluster
      if (cluster) {
        clusterDetail(cluster).then(response => {
          this.loading = false
          this.cluster_detail = response.data
          console.log(this.cluster_detail)
        }).catch(() => {
          this.loading = false
        })
        listEvents(cluster).then(response => {
          this.loading = false
          this.originEvents = response.data
        }).catch(() => {
          this.loading = false
        })
      } else {
        this.loading = false
        Message.error("获取集群异常，请刷新重试")
      }
    },
  }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/variables.scss";
.border-class {
    border: 1px solid #EBEEF5;
    padding: 5px 10px 10px;

    .event-title {
        font-size: 14px;
        font-weight: 400;
        color: #1f2f3d;
    }
    .event-body {
        font-size: 14px;
        color: #5e6d82;
    }
}
</style>
<style>
.row-class .el-card__body {
    padding: 10px 5px;
    /* height: 100px; */
}
.event-class .el-card__body {
    padding: 5px 20px;
    /* height: 100px; */
}
</style>