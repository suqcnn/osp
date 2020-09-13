<template>
  <div>
    <clusterbar :titleName="titleName" :delFunc="deleteServices" :editFunc="getServiceYaml"/>
    <div class="dashboard-container" v-loading="loading">

      <el-form label-position="left" class="pod-item" label-width="120px">
        <el-form-item label="名称">
          <span>{{ service.name }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ service.created }}</span>
        </el-form-item>
        <el-form-item label="命名空间">
          <span>{{ service.namespace }}</span>
        </el-form-item>
        <el-form-item label="类型">
          <span>{{ service.type }}</span>
        </el-form-item>
        <el-form-item label="Cluster IP">
          <span>{{ service.cluster_ip }}</span>
        </el-form-item>
        <el-form-item label="端口">
          <template v-if="service.ports && service.ports.length > 0">
            <span>{{ getPortsDisplay(service.ports) }}</span>
          </template>
        </el-form-item>
        <el-form-item label="Endpoints">
          <template v-for="e of endpoints">
            <span :key="e.name">{{ endpointsAddresses(e.subsets) }}</span>
          </template>
        </el-form-item>
        <el-form-item label="会话亲和">
          <span>{{ service.session_affinity }}</span>
        </el-form-item>
        <el-form-item label="选择器">
          <template v-if="service.selector">
            <span v-for="(val, key) in service.selector" :key="key" class="back-class">
              {{ key + ': ' + val }} <br/>
            </span>
          </template>
        </el-form-item>
        <el-form-item label="标签">
          <span v-if="!service.labels">——</span>
          <template v-else v-for="(val, key) in service.labels" >
            <span :key="key" class="back-class">{{key}}: {{val}} <br/></span>
          </template>
        </el-form-item>
        <!-- <el-form-item label="注解">
          <span v-if="!service.annotations">——</span>
          
          <template v-else v-for="(val, key) in service.annotations">
            <span :key="key">{{key}}: {{val}}<br/></span>
          </template>
        </el-form-item> -->
      </el-form>
      
      <el-collapse class="podCollapse" :value="['events']">
        <el-collapse-item title="Events" name="events">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
          <div class="msgClass">
            <el-table
              :data="serviceEvents"
              class="table-fix"
              tooltip-effect="dark"
              style="width: 100%"
              v-loading="eventLoading"
              :cell-style="cellStyle"
              :default-sort = "{prop: 'event_time', order: 'descending'}"
              >
              <el-table-column
                prop="type"
                label="类型"
                min-width="25"
                show-overflow-tooltip>
              </el-table-column>
              <el-table-column
                prop="object"
                label="对象"
                min-width="55"
                show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.object.kind }}/{{ scope.row.object.name }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                prop="reason"
                label="原因"
                min-width="50"
                show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.reason ? scope.row.reason : "——" }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                prop="message"
                label="信息"
                min-width="120"
                show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.message ? scope.row.message : "——" }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                prop="event_time"
                label="触发时间"
                min-width="50"
                show-overflow-tooltip>
              </el-table-column>
            </el-table>
          </div>
        </el-collapse-item>
      </el-collapse>

      <el-dialog title="编辑" :visible.sync="yamlDialog" :close-on-click-modal="false" width="60%" top="55px">
        <yaml v-if="yamlDialog" v-model="yamlValue" :loading="yamlLoading"></yaml>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="yamlDialog = false" size="small">取 消</el-button>
          <el-button plain @click="updateService()" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getService, deleteServices, updateService } from '@/api/service'
import { listEndpoints } from '@/api/endpoints'
import { listEvents, buildEvent } from '@/api/event'
// import { listPods, containerClass, buildPods, podMatch, deletePods } from '@/api/pods'
import { Message } from 'element-ui'
import { Terminal } from '@/views/components'
import { Log } from '@/views/components'

export default {
  name: 'ServiceDetail',
  components: {
    Clusterbar,
    Terminal,
    Log,
    Yaml
  },
  data() {
    return {
      logContainerShow: false,
      termContainerShow: false,
      yamlDialog: false,
      yamlValue: "",
      yamlLoading: true,
      logDialog: false,
      terminalDialog: false,
      cellStyle: {border: 0},
      loading: true,
      originService: undefined,
      // pods: [],
      endpoints: [],
      selectContainer: '',
      selectPodName: '',
      serviceEvents: [],
      eventLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    serviceWatch: function (newObj) {
      if (newObj && this.originService) {
        let newUid = newObj.resource.metadata.uid
        if (newUid !== this.service.uid) {
          return
        }
        let newRv = newObj.resource.metadata.resourceVersion
        if (this.service.resource_version < newRv) {
          this.originService = newObj.resource
        }
      }
    },
    eventWatch: function (newObj) {
      if (newObj && this.originService) {
        let event = newObj.resource
        if (event.involvedObject.namespace !== this.service.namespace) return
        if (event.involvedObject.uid !== this.service.uid) return
        let newUid = newObj.resource.metadata.uid
        if (newObj.event === 'add') {
          this.serviceEvents.push(buildEvent(event))
        } else if (newObj.event == 'update') {
          let newRv = newObj.resource.metadata.resourceVersion
          for (let i in this.serviceEvents) {
            let d = this.serviceEvents[i]
            if (d.uid === newUid) {
              if (d.resource_version < newRv){
                let newEvent = buildEvent(newObj.resource)
                this.$set(this.serviceEvents, i, newEvent)
              }
              break
            }
          }
        } else if (newObj.event === 'delete') {
          this.serviceEvents = this.serviceEvents.filter(( { uid } ) => uid !== newUid)
        }
      }
    },
    // podsWatch: function (newObj) {
    //   if (newObj && this.originService) {
    //     let isPodMatch = podMatch(this.originService.spec.selector, newObj.resource.metadata.labels)
    //     if (isPodMatch) {
    //       let newUid = newObj.resource.metadata.uid
    //       let newRv = newObj.resource.metadata.resourceVersion
    //       if (newObj.event === 'add') {
    //         this.pods.push(buildPods(newObj.resource))
    //       } else if (newObj.event === 'update') {
    //         for (let i in this.pods) {
    //           let p = this.pods[i]
    //           if (p.uid === newUid && p.resource_version < newRv) {
    //             let newPod = buildPods(newObj.resource)
    //             this.$set(this.pods, i, newPod)
    //             break
    //           }
    //         }
    //       } else if (newObj.event === 'delete') {
    //         this.pods = this.pods.filter(( { uid } ) => uid !== newUid)
    //       }
    //     }
    //   }
    // }
  },
  computed: {
    titleName: function() {
      return ['Services', this.serviceName]
    },
    serviceName: function() {
      return this.$route.params ? this.$route.params.serviceName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    service: function() {
      let p = this.buildService(this.originService)
      return p
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    serviceWatch: function() {
      return this.$store.getters["ws/servicesWatch"]
    },
    eventWatch: function() {
      return this.$store.getters["ws/eventWatch"]
    },
    // podsWatch: function() {
    //   return this.$store.getters["ws/podWatch"]
    // }
  },
  methods: {
    fetchData: function() {
      this.originService = null
      this.serviceEvents = []
      this.loading = true
      this.eventLoading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.namespace) {
        Message.error("获取命名空间参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.serviceName) {
        Message.error("获取Service名称参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      getService(cluster, this.namespace, this.serviceName).then(response => {
        // this.loading = false
        this.originService = response.data
        listEndpoints(cluster, this.namespace, this.serviceName).then(response => {
          this.loading = false
          this.endpoints = response.data
        }).catch(() => {
          this.loading = false
        })

        listEvents(cluster, this.originService.metadata.uid).then(response => {
          this.eventLoading = false
          if (response.data) {
            this.serviceEvents = response.data.length > 0 ? response.data : []
          }
        }).catch(() => {
          this.eventLoading = false
        })
      }).catch(() => {
        this.loading = false
        this.eventLoading = false
      })
    },
    buildService: function(service) {
      if (!service) return {}
      let p = {
        uid: service.metadata.uid,
        namespace: service.metadata.namespace,
        name: service.metadata.name,
        type: service.spec.type,
        cluster_ip: service.spec.clusterIP,
        ports: service.spec.ports,
        external_ip: service.spec.externalIPs,
        session_affinity: service.spec.sessionAffinity,
        resource_version: service.metadata.resourceVersion,
        selector: service.spec.selector,
        created: service.metadata.creationTimestamp,
        labels: service.metadata.labels,
        annotations: service.metadata.annotations,
      }
      return p
    },
    toogleExpand: function(row) {
      let $table = this.$refs.table;
      $table.toggleRowExpansion(row)
    },
    deleteServices: function() {
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      if ( !this.service ) {
        Message.error("获取Service参数异常，请刷新重试")
      }
      let services = [{
        namespace: this.service.namespace,
        name: this.service.name,
      }]
      let params = {
        resources: services
      }
      deleteServices(cluster, params).then(() => {
        Message.success("删除成功")
      }).catch(() => {
        // console.log(e)
      })
    },
    getServiceYaml: function() {
      if (!this.service) {
        Message.error("获取Service参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      this.yamlValue = ""
      this.yamlDialog = true
      this.yamlLoading = true
      getService(cluster, this.service.namespace, this.service.name, "yaml").then(response => {
        this.yamlLoading = false
        this.yamlValue = response.data
      }).catch(() => {
        this.yamlLoading = false
      })
    },
    updateService: function() {
      if (!this.service) {
        Message.error("获取Service参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      console.log(this.yamlValue)
      updateService(cluster, this.service.namespace, this.service.name, this.yamlValue).then(() => {
        Message.success("更新成功")
      }).catch(() => {
        // console.log(e) 
      })
    },
    containerClass: function(status) {
      return containerClass(status)
    },
    namePodClick: function(namespace, name) {
      this.$router.push({name: 'podsDetail', params: {namespace: namespace, podName: name}})
    },
    deletePods: function(pods) {
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      if ( pods.length <= 0 ){
        Message.error("请选择要删除的Pod")
        return
      }
      let params = {
        resources: pods
      }
      deletePods(cluster, params).then(() => {
        Message.success("删除成功")
      }).catch(() => {
        // console.log(e)
      })
    },
    getPortsDisplay(ports) {
      if (!ports) return ''
      var pd = []
      for (let p of ports) {
        var pds = p.port
        if (p.nodePort) {
          pds += ':' + p.nodePort
        }
        pds += '/' + p.protocol
        pd.push(pds)
      }
      return pd.join(',')
    },
    endpointsAddresses(subsets) {
      if (!subsets) return ''
      let as = []
      for(let s of subsets) {
        for(let a of s.addresses) {
          if(s.ports) {
            for(let e of s.ports) {
              as.push(a.ip + ':' + e.port)
            }
          } else {
            as.push(a.ip)
          }
        }
      }
      return as.join(',')
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
.name-class {
  cursor: pointer;
}
.name-class:hover {
  color: #409EFF;
}
.download {
  // width: 70px;
  // height: 40px;
  position: relative;

  .download-right {
    position: absolute;
    right: 70px;
    top: 0px;
    background: #FFF;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
    border: 1px solid #EBEEF5;
    .download-item {
      display: inline-block;
      margin-right: -8px;
      white-space: nowrap;
      width: auto;
      padding: 0px 12px;
      cursor: pointer;
      color: #606266;
      .item-txt {
        flex: 1;
        display: flex;
        // flex-wrap: nowrap;
        align-items:center;
        font-size: 14px;
      }
    }
    .download-item:hover {
      // background: #1f2326;
      color: #66b1ff;
      // border-radius: 6px;
    }
  }
}
</style>

<style>
/* .el-table__expand-icon {
  display: none;
} */
.el-table__expanded-cell[class*=cell] {
  padding-top: 5px;
}
.table-expand {
  font-size: 0;
}
.table-expand label {
  width: 90px;
  color: #99a9bf;
  font-weight: 400;
}
.table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 100%;
}
/* 
.item-class {
  padding: 20px 20px 20px 5px;
  font-size: 0;
}

.item-class  */

.pod-item {
  padding: 5px 20px 10px 15px;
  font-size: 14px;
}
.pod-item label {
  /* width: 120px; */
  color: #99a9bf;
  font-weight: 400;
  /* display: inline-block; */
}
.pod-item .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  /* width: 50%; */
}
/* .pod-item .el-form-item__content{
  float: left;
} */
.pod-item span {
  color: #606266;
}
/* .el-collapse {
  border-top: 0px;
} */
.title-class {
  margin-left: 5px;
  color: #606266;
  font-size: 13px;
}
.podCollapse .el-collapse-item__content {
  padding: 0px 10px 15px;
  /* font-size: 13px; */
}
.el-dialog__body {
  padding-top: 5px;
}
.msgClass {
  margin: 0px 25px;
}
.msgClass .el-table::before {
  height: 0px;
}
</style>
