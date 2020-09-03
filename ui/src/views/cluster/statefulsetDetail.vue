<template>
  <div>
    <clusterbar :titleName="titleName" :delFunc="deleteStatefulSets" :editFunc="getStatefulSetYaml"/>
    <div class="dashboard-container">
      <!-- <div class="dashboard-text"></div> -->
      <el-table
        ref="table"
        :data="pods"
        class="table-fix"
        tooltip-effect="dark"
        style="width: 100%"
        v-loading="loading"
        :cell-style="cellStyle"
        :default-sort = "{prop: 'name'}"
        >
        <el-table-column
          prop="name"
          label="POD名称"
          min-width="150"
          show-overflow-tooltip>
          <template slot-scope="scope">
            <span class="name-class" v-on:click="namePodClick(scope.row.namespace, scope.row.name)">
              {{ scope.row.name }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="containerNum"
          label="容器"
          min-width="45"
          show-overflow-tooltip>
          <template slot-scope="scope">
            <template v-if="scope.row.init_containers">
            <el-tooltip :content="`${c.name} (${c.status})`" placement="top" v-for="c in scope.row.init_containers" :key="c.name">
              <svg-icon style="margin-top: 7px;" :class="containerClass(c.status)" icon-class="square" />
            </el-tooltip>
            </template>
            <el-tooltip :content="`${c.name} (${c.status})`" placement="top" v-for="c in scope.row.containers" :key="c.name">
              <svg-icon style="margin-top: 7px;" :class="containerClass(c.status)" icon-class="square" />
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          prop="restarts"
          label="重启"
          min-width="45"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="node_name"
          label="节点"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="ip"
          label="IP"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="created"
          label="创建时间"
          min-width="100"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          min-width="60"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          label=""
          show-overflow-tooltip
          width="45">
          <template slot-scope="scope">
            <el-dropdown size="medium" >
              <el-link :underline="false"><svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" /></el-link>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native.prevent="namePodClick(scope.row.namespace, scope.row.name)">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="detail" />
                  <span style="margin-left: 5px;">详情</span>
                </el-dropdown-item>
                <div @mouseover="logContainerShow = true;" @mouseout="logContainerShow = false;">
                  <el-dropdown-item @click.native.prevent="selectContainer = scope.row.containers[0].name; selectPodName = scope.row.name; logDialog = true;">
                    <div class="download">
                      <div>
                        <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="log" />
                        <span style="margin-left: 5px;">日志</span>
                      </div>
                      <div class="download-right" v-show="scope.row.containerNum > 1 && logContainerShow">
                        <div class="download-item" v-for="c in scope.row.init_containers" :key="c.name"
                             @click="selectContainer = c.name; selectPodName = scope.row.name; logDialog = true;">
                            {{ c.name }}
                        </div>
                        <div class="download-item" v-for="c in scope.row.containers" :key="c.name"
                             @click="selectContainer = c.name; selectPodName = scope.row.name; logDialog = true;">
                            {{ c.name }}
                        </div>
                      </div>
                    </div>
                  </el-dropdown-item>
                </div>
                <div @mouseover="termContainerShow = true;" @mouseout="termContainerShow = false;">
                  <el-dropdown-item @click.native.prevent="selectContainer = scope.row.containers[0].name; selectPodName = scope.row.name; terminalDialog = true;">
                    <div class="download">
                      <div>
                        <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="terminal" />
                        <span style="margin-left: 5px;">终端</span>
                      </div>
                      <div class="download-right" v-show="scope.row.containers.length > 1 && termContainerShow">
                        <div class="download-item" v-for="c in scope.row.containers" :key="c.name"
                             @click="selectContainer = c.name; selectPodName = scope.row.name; terminalDialog = true;">
                            {{ c.name }}
                        </div>
                      </div>
                    </div>
                  </el-dropdown-item>
                </div>
                <el-dropdown-item @click.native.prevent="deletePods([{namespace: scope.row.namespace, name: scope.row.name}])">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="delete" />
                  <span style="margin-left: 5px;">删除</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

          <el-form label-position="left" inline class="pod-item">
            <el-form-item label="名称">
              <span>{{ statefulset.name }}</span>
            </el-form-item>
            <el-form-item label="创建时间">
              <span>{{ statefulset.created }}</span>
            </el-form-item>
            <el-form-item label="命名空间">
              <span>{{ statefulset.namespace }}</span>
            </el-form-item>
            <el-form-item label="更新策略">
              <span>{{ statefulset.strategy }}</span>
            </el-form-item>
            <el-form-item label="Pod副本">
              <span>{{ statefulset.ready_replicas + "/" + statefulset.status_replicas }}</span>
            </el-form-item>
            <el-form-item label="选择器">
              <span v-if="!statefulset.label_selector">——</span>
              <template v-else v-for="(val, key) in statefulset.label_selector.matchLabels">
                <span :key="key">{{key}}: {{val}}<br/></span>
              </template>
            </el-form-item>
            <el-form-item label="标签">
              <span v-if="!statefulset.labels">——</span>
              <template v-else v-for="(val, key) in statefulset.labels">
                <span :key="key">{{key}}: {{val}}<br/></span>
              </template>
            </el-form-item>
            <el-form-item label="注解">
              <span v-if="!statefulset.annotations">——</span>
              
              <template v-else v-for="(val, key) in statefulset.annotations">
                <span :key="key">{{key}}: {{val}}<br/></span>
              </template>
            </el-form-item>
          </el-form>
        <!-- </el-collapse-item> -->
      <el-collapse class="podCollapse">
        <el-collapse-item title="Conditions" name="conditions">
          <template slot="title">
            <span class="title-class">Conditions</span>
          </template>
          <div class="msgClass">
            <el-table
              :data="statefulset.conditions"
              class="table-fix"
              tooltip-effect="dark"
              style="width: 100%"
              :cell-style="cellStyle"
              :default-sort = "{prop: 'lastProbeTime'}"
              >
              <el-table-column
                prop="type"
                label="类型"
                min-width="30"
                show-overflow-tooltip>
              </el-table-column>
              <el-table-column
                prop="status"
                label="状态"
                min-width="20"
                show-overflow-tooltip>
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
                show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.message ? scope.row.message : "——" }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="触发时间"
                min-width="40"
                show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.lastProbeTime ? scope.row.lastProbeTime : scope.row.lastTransitionTime }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-collapse-item>
        <el-collapse-item title="Events" name="events">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
          <div class="msgClass">
            <el-table
              :data="statefulsetEvents"
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

      <el-dialog title="终端" :visible.sync="terminalDialog" :close-on-click-modal="false" width="80%" top="55px">
        <terminal v-if="terminalDialog" :cluster="cluster" :namespace="namespace" :pod="selectPodName" :container="selectContainer"></terminal>
      </el-dialog>

      <el-dialog title="日志" :visible.sync="logDialog" :close-on-click-modal="false" width="80%" top="55px">
        <log v-if="logDialog" :cluster="cluster" :namespace="namespace" :pod="selectPodName" :container="selectContainer"></log>
      </el-dialog>

      <el-dialog title="编辑" :visible.sync="yamlDialog" :close-on-click-modal="false" width="60%" top="55px">
        <yaml v-if="yamlDialog" v-model="yamlValue" :loading="yamlLoading"></yaml>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="yamlDialog = false" size="small">取 消</el-button>
          <el-button plain @click="updateStatefulSet()" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getStatefulSet, deleteStatefulSets, updateStatefulSet } from '@/api/statefulset'
import { listEvents, buildEvent } from '@/api/event'
import { listPods, containerClass, buildPods, podMatch, deletePods } from '@/api/pods'
import { Message } from 'element-ui'
import { Terminal } from '@/views/components'
import { Log } from '@/views/components'

export default {
  name: 'StatefulSetDetail',
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
      originStatefulset: undefined,
      pods: [],
      selectContainer: '',
      selectPodName: '',
      statefulsetEvents: [],
      eventLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    statefulsetWatch: function (newObj) {
      if (newObj && this.originStatefulset) {
        let newUid = newObj.resource.metadata.uid
        if (newUid !== this.statefulset.uid) {
          return
        }
        let newRv = newObj.resource.metadata.resourceVersion
        if (this.statefulset.resource_version < newRv) {
          this.originStatefulset = newObj.resource
        }
      }
    },
    eventWatch: function (newObj) {
      if (newObj && this.originStatefulset) {
        let event = newObj.resource
        if (event.involvedObject.namespace !== this.statefulset.namespace) return
        if (event.involvedObject.uid !== this.statefulset.uid) return
        let newUid = newObj.resource.metadata.uid
        if (newObj.event === 'add') {
          this.statefulsetEvents.push(buildEvent(event))
        } else if (newObj.event == 'update') {
          let newRv = newObj.resource.metadata.resourceVersion
          for (let i in this.statefulsetEvents) {
            let d = this.statefulsetEvents[i]
            if (d.uid === newUid) {
              if (d.resource_version < newRv){
                let newEvent = buildEvent(newObj.resource)
                this.$set(this.statefulsetEvents, i, newEvent)
              }
              break
            }
          }
        } else if (newObj.event === 'delete') {
          this.statefulsetEvents = this.statefulsetEvents.filter(( { uid } ) => uid !== newUid)
        }
      }
    },
    podsWatch: function (newObj) {
      if (newObj && this.originStatefulset) {
        let isPodMatch = podMatch(this.originStatefulset.spec.selector, newObj.resource.metadata.labels)
        if (isPodMatch) {
          let newUid = newObj.resource.metadata.uid
          let newRv = newObj.resource.metadata.resourceVersion
          if (newObj.event === 'add') {
            this.pods.push(buildPods(newObj.resource))
          } else if (newObj.event === 'update') {
            for (let i in this.pods) {
              let p = this.pods[i]
              if (p.uid === newUid && p.resource_version < newRv) {
                let newPod = buildPods(newObj.resource)
                this.$set(this.pods, i, newPod)
                break
              }
            }
          } else if (newObj.event === 'delete') {
            this.pods = this.pods.filter(( { uid } ) => uid !== newUid)
          }
        }
      }
    }
  },
  computed: {
    titleName: function() {
      return ['StatefulSets', this.statefulsetName]
    },
    statefulsetName: function() {
      return this.$route.params ? this.$route.params.statefulsetName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    statefulset: function() {
      let p = this.buildStatefulSet(this.originStatefulset)
      return p
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    statefulsetWatch: function() {
      return this.$store.getters["ws/statefulsetWatch"]
    },
    eventWatch: function() {
      return this.$store.getters["ws/eventWatch"]
    },
    podsWatch: function() {
      return this.$store.getters["ws/podWatch"]
    }
  },
  methods: {
    fetchData: function() {
      this.originStatefulset = null
      this.statefulsetEvents = []
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
      if (!this.statefulsetName) {
        Message.error("获取Statefulset名称参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      getStatefulSet(cluster, this.namespace, this.statefulsetName).then(response => {
        // this.loading = false
        this.originStatefulset = response.data
        listPods(cluster, this.originStatefulset.spec.selector).then(response => {
          this.loading = false
          this.pods = response.data
        }).catch(() => {
          this.loading = false
        })

        listEvents(cluster, this.originStatefulset.metadata.uid).then(response => {
          this.eventLoading = false
          if (response.data) {
            this.statefulsetEvents = response.data.length > 0 ? response.data : []
          }
        }).catch(() => {
          this.eventLoading = false
        })
      }).catch(() => {
        this.loading = false
        this.eventLoading = false
      })
    },
    buildStatefulSet: function(statefulset) {
      if (!statefulset) return {}
      let p = {
        uid: statefulset.metadata.uid,
        namespace: statefulset.metadata.namespace,
        name: statefulset.metadata.name,
        replicas: statefulset.spec.replicas,
        status_replicas: statefulset.status.replicas || 0,
        ready_replicas: statefulset.status.readyReplicas || 0,
        resource_version: statefulset.metadata.resourceVersion,
        strategy: statefulset.spec.updateStrategy.type,
        conditions: statefulset.status.conditions,
        created: statefulset.metadata.creationTimestamp,
        label_selector: statefulset.spec.selector,
        labels: statefulset.metadata.labels,
        annotations: statefulset.metadata.annotations,
      }
      return p
    },
    toogleExpand: function(row) {
      let $table = this.$refs.table;
      $table.toggleRowExpansion(row)
    },
    deleteStatefulSets: function() {
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      if ( !this.statefulset ) {
        Message.error("获取Statefulset参数异常，请刷新重试")
      }
      let statefulsets = [{
        namespace: this.statefulset.namespace,
        name: this.statefulset.name,
      }]
      let params = {
        resources: statefulsets
      }
      deleteStatefulSets(cluster, params).then(() => {
        Message.success("删除成功")
      }).catch(() => {
        // console.log(e)
      })
    },
    getStatefulSetYaml: function() {
      if (!this.statefulset) {
        Message.error("获取Statefulset参数异常，请刷新重试")
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
      getStatefulSet(cluster, this.statefulset.namespace, this.statefulset.name, "yaml").then(response => {
        this.yamlLoading = false
        this.yamlValue = response.data
      }).catch(() => {
        this.yamlLoading = false
      })
    },
    updateStatefulSet: function() {
      if (!this.statefulset) {
        Message.error("获取Statefulset参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      console.log(this.yamlValue)
      updateStatefulSet(cluster, this.statefulset.namespace, this.statefulset.name, this.yamlValue).then(() => {
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

.pod-item {
  margin: 20px 20px 20px 5px;
  font-size: 0;
}
.pod-item label {
  width: 90px;
  color: #99a9bf;
  font-weight: 400;
}
.pod-item .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
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
