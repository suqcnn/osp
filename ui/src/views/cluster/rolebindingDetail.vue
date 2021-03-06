<template>
  <div>
    <clusterbar :titleName="titleName" :delFunc="deleteRoleBindings" :editFunc="getRoleBindingYaml"/>
    <div class="dashboard-container" v-loading="loading">

      <el-form label-position="left" class="pod-item" label-width="120px">
        <el-form-item label="名称">
          <span>{{ rolebinding.name }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ rolebinding.created }}</span>
        </el-form-item>
        <el-form-item label="命名空间">
          <span>{{ rolebinding.namespace }}</span>
        </el-form-item>
        <el-form-item label="角色">
          <span>{{ rolebinding.role.kind + '/' + rolebinding.role.name }}</span>
        </el-form-item>
        <el-form-item label="绑定主体">
          <span v-for="s of rolebinding.subjects" :key="s.name" class="back-class">
            {{ s.kind + '/' + s.name }}<br/>
          </span>
        </el-form-item>
        <!-- <el-form-item label="Secrets">
          <span>{{ getSecretsName(rolebinding.secrets) }}</span>
        </el-form-item> -->
        <el-form-item label="标签">
          <span v-if="!rolebinding.labels">—</span>
          <template v-else v-for="(val, key) in rolebinding.labels" >
            <span :key="key" class="back-class">{{key}}: {{val}} <br/></span>
          </template>
        </el-form-item>
        <!-- <el-form-item label="注解">
          <span v-if="!rolebinding.annotations">—</span>
          
          <template v-else v-for="(val, key) in rolebinding.annotations">
            <span :key="key">{{key}}: {{val}}<br/></span>
          </template>
        </el-form-item> -->
      </el-form>
      
      <el-collapse class="podCollapse" :value="['secrets', 'events']">
        <!-- <el-collapse-item title="Secrets" name="secrets">
          <template slot="title">
            <span class="title-class">Secrets</span>
          </template>
          <div class="msgClass">
            <span>{{ rolebinding.secrets }}</span>
          </div>
        </el-collapse-item> -->
        <el-collapse-item title="Events" name="events">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
          <div class="msgClass">
            <el-table
              v-if="rolebindingEvents && rolebindingEvents.length > 0"
              :data="rolebindingEvents"
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
                    {{ scope.row.reason ? scope.row.reason : "—" }}
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
                    {{ scope.row.message ? scope.row.message : "—" }}
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
          <el-button plain @click="updateRoleBinding()" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getRoleBinding, deleteRoleBindings, updateRoleBinding } from '@/api/rolebinding'
import { listEndpoints } from '@/api/endpoints'
import { listEvents, buildEvent } from '@/api/event'
// import { listPods, containerClass, buildPods, podMatch, deletePods } from '@/api/pods'
import { Message } from 'element-ui'

export default {
  name: 'RoleBindingDetail',
  components: {
    Clusterbar,
    Yaml
  },
  data() {
    return {
      yamlDialog: false,
      yamlValue: "",
      yamlLoading: true,
      cellStyle: {border: 0},
      loading: true,
      originRoleBinding: undefined,
      // pods: [],
      endpoints: [],
      selectContainer: '',
      selectPodName: '',
      rolebindingEvents: [],
      eventLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    rolebindingWatch: function (newObj) {
      if (newObj && this.originRoleBinding) {
        let newUid = newObj.resource.metadata.uid
        if (newUid !== this.rolebinding.uid) {
          return
        }
        let newRv = newObj.resource.metadata.resourceVersion
        if (this.rolebinding.resource_version < newRv) {
          this.originRoleBinding = newObj.resource
        }
      }
    },
    eventWatch: function (newObj) {
      if (newObj && this.originRoleBinding) {
        let event = newObj.resource
        if (event.involvedObject.namespace !== this.rolebinding.namespace) return
        if (event.involvedObject.uid !== this.rolebinding.uid) return
        let newUid = newObj.resource.metadata.uid
        if (newObj.event === 'add') {
          this.rolebindingEvents.push(buildEvent(event))
        } else if (newObj.event == 'update') {
          let newRv = newObj.resource.metadata.resourceVersion
          for (let i in this.rolebindingEvents) {
            let d = this.rolebindingEvents[i]
            if (d.uid === newUid) {
              if (d.resource_version < newRv){
                let newEvent = buildEvent(newObj.resource)
                this.$set(this.rolebindingEvents, i, newEvent)
              }
              break
            }
          }
        } else if (newObj.event === 'delete') {
          this.rolebindingEvents = this.rolebindingEvents.filter(( { uid } ) => uid !== newUid)
        }
      }
    },
  },
  computed: {
    titleName: function() {
      return ['RoleBindings', this.rolebindingName]
    },
    rolebindingName: function() {
      return this.$route.params ? this.$route.params.rolebindingName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    kind: function() {
      if (this.namespace) return 'RoleBinding';
      return 'ClusterRoleBinding'
    },
    rolebinding: function() {
      let p = this.buildRoleBinding(this.originRoleBinding)
      return p
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    rolebindingWatch: function() {
      return this.$store.getters["ws/rolebindingsWatch"]
    },
    eventWatch: function() {
      return this.$store.getters["ws/eventWatch"]
    },
  },
  methods: {
    fetchData: function() {
      this.originRoleBinding = null
      this.rolebindingEvents = []
      this.loading = true
      this.eventLoading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      if (this.kind === 'RoleBinding' && !this.namespace) {
        Message.error("获取命名空间参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      var namespace = this.namespace;
      if (this.kind === 'ClusterRoleBinding') namespace = 'n';
      if (!this.rolebindingName) {
        Message.error("获取RoleBinding名称参数异常，请刷新重试")
        this.loading = false
        this.eventLoading = false
        return
      }
      getRoleBinding(cluster, namespace, this.rolebindingName, this.kind).then(response => {
        this.loading = false
        this.originRoleBinding = response.data

        listEvents(cluster, this.originRoleBinding.metadata.uid).then(response => {
          this.eventLoading = false
          if (response.data) {
            this.rolebindingEvents = response.data.length > 0 ? response.data : []
          }
        }).catch(() => {
          this.eventLoading = false
        })
      }).catch(() => {
        this.loading = false
        this.eventLoading = false
      })
    },
    buildRoleBinding: function(rolebinding) {
      if (!rolebinding) return {}
      let p = {
        uid: rolebinding.metadata.uid,
        namespace: rolebinding.metadata.namespace,
        name: rolebinding.metadata.name,
        resource_version: rolebinding.metadata.resourceVersion,
        subjects: rolebinding.subjects,
        role: rolebinding.roleRef,
        created: rolebinding.metadata.creationTimestamp,
        labels: rolebinding.metadata.labels,
        annotations: rolebinding.metadata.annotations,
      }
      return p
    },
    toogleExpand: function(row) {
      let $table = this.$refs.table;
      $table.toggleRowExpansion(row)
    },
    deleteRoleBindings: function() {
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      if ( !this.rolebinding ) {
        Message.error("获取RoleBinding参数异常，请刷新重试")
      }
      let rolebindings = [{
        namespace: this.rolebinding.namespace,
        name: this.rolebinding.name,
      }]
      let params = {
        resources: rolebindings
      }
      deleteRoleBindings(cluster, params).then(() => {
        Message.success("删除成功")
      }).catch(() => {
        // console.log(e)
      })
    },
    getRoleBindingYaml: function() {
      if (!this.rolebinding) {
        Message.error("获取RoleBinding参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      var namespace = this.namespace
      if (this.kind === 'ClusterRoleBinding') namespace = 'n'
      this.yamlValue = ""
      this.yamlDialog = true
      this.yamlLoading = true
      getRoleBinding(cluster, namespace, this.rolebinding.name, this.kind, "yaml").then(response => {
        this.yamlLoading = false
        this.yamlValue = response.data
      }).catch(() => {
        this.yamlLoading = false
      })
    },
    updateRoleBinding: function() {
      if (!this.rolebinding) {
        Message.error("获取RoleBinding参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      console.log(this.yamlValue)
      updateRoleBinding(cluster, this.rolebinding.namespace, this.rolebinding.name, this.yamlValue).then(() => {
        Message.success("更新成功")
      }).catch(() => {
        // console.log(e) 
      })
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
