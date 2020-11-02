<template>
  <div>
    <clusterbar :titleName="titleName" :delFunc="deleteIngresses" :editFunc="getIngressYaml"/>
    <div class="dashboard-container" v-loading="loading">

      <el-form label-position="left" class="pod-item" label-width="120px">
        <el-form-item label="名称">
          <span>{{ ingress.name }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ ingress.created }}</span>
        </el-form-item>
        <el-form-item label="命名空间">
          <span>{{ ingress.namespace }}</span>
        </el-form-item>
        <el-form-item v-if="ingress.backend" label="默认后端">
          <span>{{ ingress.backend.serviceName + ':' + ingress.backend.servicePort }}</span>
        </el-form-item>
        <el-form-item label="标签">
          <span v-if="!ingress.labels">—</span>
          <template v-else v-for="(val, key) in ingress.labels" >
            <span :key="key" class="back-class">{{key}}: {{val}} <br/></span>
          </template>
        </el-form-item>
        <el-form-item label="注解">
          <span v-if="!ingress.annotations">—</span>
          
          <template v-else v-for="(val, key) in ingress.annotations">
            <span :key="key">{{key}}: {{val}}<br/></span>
          </template>
        </el-form-item>
      </el-form>
      
      <el-collapse class="podCollapse" :value="['rules', 'events']">
        <el-collapse-item title="Rules" name="rules">
          <template slot="title">
            <span class="title-class">Rules</span>
          </template>
          <div class="msgClass">
            <div v-for="r of ingress.rules" :key="r.host">
              <div><span style="color: #606266"><b>访问域名： {{ r.host }}</b></span></div>
              <el-table v-if="r.http"
                :data="r.http.paths"
                class="table-fix"
                tooltip-effect="dark"
                style="width: 100%"
                v-loading="eventLoading"
                :cell-style="cellStyle"
                :default-sort = "{prop: 'event_time', order: 'descending'}"
                >
                <el-table-column
                  prop="path"
                  label="路径"
                  min-width="25"
                  show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-if="scope.row.path">
                      {{ scope.row.path }}
                    </span>
                    <span v-else>—</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="backend"
                  label="服务后端"
                  min-width="55"
                  show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span>
                      {{ scope.row.backend.serviceName }}:{{ scope.row.backend.servicePort }}
                    </span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="Events" name="events">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
          <div class="msgClass">
            <el-table
              v-if="ingressEvents && ingressEvents.length > 0"
              :data="ingressEvents"
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
            <div v-else style="color: #909399; text-align: center">暂无数据</div>
          </div>
        </el-collapse-item>
      </el-collapse>

      <el-dialog title="编辑" :visible.sync="yamlDialog" :close-on-click-modal="false" width="60%" top="55px">
        <yaml v-if="yamlDialog" v-model="yamlValue" :loading="yamlLoading"></yaml>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="yamlDialog = false" size="small">取 消</el-button>
          <el-button plain @click="updateIngress()" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getIngress, deleteIngresses, updateIngress } from '@/api/ingress'
// import { listEndpoints } from '@/api/endpoints'
import { listEvents, buildEvent } from '@/api/event'
// import { listPods, containerClass, buildPods, podMatch, deletePods } from '@/api/pods'
import { Message } from 'element-ui'

export default {
  name: 'IngressDetail',
  components: {
    Clusterbar,
    Yaml
  },
  data() {
    return {
      cellStyle: {border: 0},
      yamlDialog: false,
      yamlValue: "",
      yamlLoading: true,
      loading: true,
      originIngress: undefined,
      endpoints: [],
      ingressEvents: [],
      eventLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    ingressWatch: function (newObj) {
      if (newObj && this.originIngress) {
        let newUid = newObj.resource.metadata.uid
        if (newUid !== this.ingress.uid) {
          return
        }
        let newRv = newObj.resource.metadata.resourceVersion
        if (this.ingress.resource_version < newRv) {
          this.originIngress = newObj.resource
        }
      }
    },
    eventWatch: function (newObj) {
      if (newObj && this.originIngress) {
        let event = newObj.resource
        if (event.involvedObject.namespace !== this.ingress.namespace) return
        if (event.involvedObject.uid !== this.ingress.uid) return
        let newUid = newObj.resource.metadata.uid
        if (newObj.event === 'add') {
          this.ingressEvents.push(buildEvent(event))
        } else if (newObj.event == 'update') {
          let newRv = newObj.resource.metadata.resourceVersion
          for (let i in this.ingressEvents) {
            let d = this.ingressEvents[i]
            if (d.uid === newUid) {
              if (d.resource_version < newRv){
                let newEvent = buildEvent(newObj.resource)
                this.$set(this.ingressEvents, i, newEvent)
              }
              break
            }
          }
        } else if (newObj.event === 'delete') {
          this.ingressEvents = this.ingressEvents.filter(( { uid } ) => uid !== newUid)
        }
      }
    },
  },
  computed: {
    titleName: function() {
      return ['Ingresses', this.ingressName]
    },
    ingressName: function() {
      return this.$route.params ? this.$route.params.ingressName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    ingress: function() {
      let p = this.buildIngress(this.originIngress)
      return p
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    ingressWatch: function() {
      return this.$store.getters["ws/ingressesWatch"]
    },
    eventWatch: function() {
      return this.$store.getters["ws/eventWatch"]
    },
  },
  methods: {
    fetchData: function() {
      this.originIngress = null
      this.ingressEvents = []
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
      if (!this.ingressName) {
        Message.error("获取Ingress名称参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      getIngress(cluster, this.namespace, this.ingressName).then(response => {
        // this.loading = false
        this.originIngress = response.data
        this.loading = false

        listEvents(cluster, this.originIngress.metadata.uid).then(response => {
          this.eventLoading = false
          if (response.data) {
            this.ingressEvents = response.data.length > 0 ? response.data : []
          }
        }).catch(() => {
          this.eventLoading = false
        })
      }).catch(() => {
        this.loading = false
        this.eventLoading = false
      })
    },
    buildIngress: function(ingress) {
      if (!ingress) return {}
      let p = {
        uid: ingress.metadata.uid,
        namespace: ingress.metadata.namespace,
        name: ingress.metadata.name,
        backend: ingress.spec.backend,
        tls: ingress.spec.tls,
        rules: ingress.spec.rules,
        resource_version: ingress.metadata.resourceVersion,
        created: ingress.metadata.creationTimestamp,
        labels: ingress.metadata.labels,
        annotations: ingress.metadata.annotations,
      }
      return p
    },
    deleteIngresses: function() {
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      if ( !this.ingress ) {
        Message.error("获取Ingress参数异常，请刷新重试")
      }
      let ingresses = [{
        namespace: this.ingress.namespace,
        name: this.ingress.name,
      }]
      let params = {
        resources: ingresses
      }
      deleteIngresses(cluster, params).then(() => {
        Message.success("删除成功")
      }).catch(() => {
        // console.log(e)
      })
    },
    getIngressYaml: function() {
      if (!this.ingress) {
        Message.error("获取Ingress参数异常，请刷新重试")
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
      getIngress(cluster, this.ingress.namespace, this.ingress.name, "yaml").then(response => {
        this.yamlLoading = false
        this.yamlValue = response.data
      }).catch(() => {
        this.yamlLoading = false
      })
    },
    updateIngress: function() {
      if (!this.ingress) {
        Message.error("获取Ingress参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      console.log(this.yamlValue)
      updateIngress(cluster, this.ingress.namespace, this.ingress.name, this.yamlValue).then(() => {
        Message.success("更新成功")
      }).catch(() => {
        // console.log(e) 
      })
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
