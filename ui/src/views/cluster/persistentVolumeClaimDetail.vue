<template>
  <div>
    <clusterbar :titleName="titleName" :editFunc="getPersistentVolumeClaimYaml" />
    <div class="dashboard-container">
      <el-form label-position="left" class="pod-item" label-width="180px" v-if="PersistentVolumeClaim.metadata">
        <el-form-item label="名称">
          <span>{{ PersistentVolumeClaim.metadata.name }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ PersistentVolumeClaim.metadata.creationTimestamp }}</span>
        </el-form-item>
        <el-form-item label="状态">
          <span>{{ PersistentVolumeClaim.status.phase }}</span>
        </el-form-item>
        <el-form-item label="Namespace">
          <span>{{ PersistentVolumeClaim.metadata.namespace }}</span>
        </el-form-item>
        <el-form-item label="Capacity">
          <span>{{ PersistentVolumeClaim.spec.resources.requests.storage }}</span>
        </el-form-item>
        <el-form-item label="storageClassName">
          <span v-if="!PersistentVolumeClaim.spec.storageClassName">——</span>
          <span v-else>{{ PersistentVolumeClaim.spec.storageClassName }}</span>
        </el-form-item>
        <el-form-item label="AccessMode">
          <template v-for="key in PersistentVolumeClaim.spec.accessModes" >
            <span :key="key" class="back-class">{{key}} <br/></span>
          </template>
        </el-form-item>
        <el-form-item label="Finalizers">
          <span v-if="!PersistentVolumeClaim.metadata.finalizers">——</span>
          <template v-else v-for="key in PersistentVolumeClaim.metadata.finalizers" >
            <span :key="key" class="back-class">{{key}}<br/></span>
          </template>
        </el-form-item>
      </el-form>

      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="Selector" name="1" v-if="PersistentVolumeClaim.spec && PersistentVolumeClaim.spec.selector">
          <el-form label-position="left" class="pod-item" label-width="180px">
            <el-form-item label="Match Labels">
              <template v-for="(key, val) in PersistentVolumeClaim.spec.selector.matchLabels">
                <span :key="key" class="back-class">{{key}}:{{val}}</span>
              </template>
            </el-form-item>
            <el-form-item label="Match Expressions">
              <span v-if="!PersistentVolumeClaim.spec.selector.matchExpressions">——</span>
              <template v-else v-for="(key, val) in PersistentVolumeClaim.spec.selector.matchExpressions">
                <span :key="key" class="back-class">{{key}}:{{val}}</span>
              </template>
            </el-form-item>
          </el-form>
        </el-collapse-item>
        <el-collapse-item title="Events" name="2">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
          <div class="msgClass">
            <el-table
              v-if="persistentVolumeClaimEvents && persistentVolumeClaimEvents.length > 0"
              :data="persistentVolumeClaimEvents"
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
          <el-button plain @click="updatePersistentVolumeClaim" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getPersistentVolumeClaim, updatePersistentVolumeClaim } from '@/api/persistent_volume_claim'
import { listEvents } from '@/api/event'
import { Message } from 'element-ui'

export default {
  name: 'PersistentVolumeClaimDetail',
  components: {
    Clusterbar,
    Yaml,
  },
  data() {
    return {
      yamlDialog: false,
      yamlValue: '',
      yamlLoading: true,
      cellStyle: { border: 0 },
      loading: true,
      originPersistentVolumeClaim: {},
      selectContainer: '',
      eventLoading: true,
      activeNames: ["1"],
      persistentVolumeClaimEvents: []
    }
  },
  created() {
    this.fetchData()
  },
  watch: {},
  computed: {
    titleName: function() {
      return ['PersistentVolumeClaim', this.PersistentVolumeClaimName]
    },
    PersistentVolumeClaimName: function() {
      return this.$route.params ? this.$route.params.persistentVolumeClaimName : ''
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    PersistentVolumeClaim: function() {
      console.log(this.originPersistentVolumeClaim)
      return this.originPersistentVolumeClaim
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ""
    }
  },
  methods: {
    handleChange(val) {
        console.log(val);
    },
    fetchData: function() {
      this.originPersistentVolumeClaim = {}
      this.loading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error('获取集群参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.PersistentVolumeClaimName) {
        Message.error('获取PersistentVolumeClaim名称参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.namespace) {
        Message.error('获取获取PersistentVolumeClaim命名空间参数异常，请刷新重试')
      }
      getPersistentVolumeClaim(cluster, this.namespace, this.PersistentVolumeClaimName).then(response => {
        this.loading = false
        this.originPersistentVolumeClaim = response.data
        listEvents(cluster, this.originPersistentVolumeClaim.metadata.uid).then(response => {
          this.eventLoading = false
          if (response.data) {
            this.persistentVolumeClaimEvents = response.data.length > 0 ? response.data : []
          }
        }).catch(() => {
          this.eventLoading = false
        })
      }).catch(() => {
        this.loading = false
      })
    },
    getPersistentVolumeClaimYaml: function() {
      if (!this.PersistentVolumeClaimName) {
        Message.error('获取PersistentVolumeClaim参数异常，请刷新重试')
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error('获取集群参数异常，请刷新重试')
        return
      }
      this.yamlValue = ''
      this.yamlDialog = true
      this.yamlLoading = true
      getPersistentVolumeClaim(cluster, this.namespace, this.PersistentVolumeClaimName, 'yaml')
        .then((response) => {
          this.yamlLoading = false
          this.yamlValue = response.data
        })
        .catch(() => {
          this.yamlLoading = false
        })
    },
    updatePersistentVolumeClaim: function() {
      if (!this.PersistentVolumeClaim) {
        Message.error("获取PersistentVolumeClaim参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      updatePersistentVolumeClaim(cluster, this.namespace, this.PersistentVolumeClaimName, this.yamlValue).then(() => {
        Message.success("更新成功")
      }).catch(() => {
        // console.log(e) 
      })
    },
  },
}
</script>

<style lang="scss" scoped>
  .my-table >>> .el-table__row>td{
  /* 去除表格线 */
  border: none;
}

.my-table >>> .el-table::before {
	height: 0px;
}

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
  color: #409eff;
}
</style>

<style>
/* .el-table__expand-icon {
  display: none;
} */
.el-table__expanded-cell[class*='cell'] {
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
  width: 40%;
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
