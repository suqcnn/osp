<template>
  <div>
    <clusterbar :titleName="titleName" :editFunc="getPodYaml" />
    <div class="dashboard-container">
      <el-form label-position="left" inline class="pod-item">
        <el-form-item label="状态">
          <span>{{ pod.status }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ pod.created }}</span>
        </el-form-item>
        <el-form-item label="命名空间">
          <span>{{ pod.namespace }}</span>
        </el-form-item>
        <el-form-item label="节点">
          <span>{{ pod.node_name }}</span>
        </el-form-item>
        <el-form-item label="服务账户">
          <span>{{ pod.service_account }}</span>
        </el-form-item>
        <el-form-item label="Pod IP">
          <span>{{ pod.ip }}</span>
        </el-form-item>
        <el-form-item label="控制器">
          <span>{{ pod.controlled }}/{{ pod.controlled_name }}</span>
        </el-form-item>
        <el-form-item label="QoS Class">
          <span>{{ pod.qos }}</span>
        </el-form-item>
        <el-form-item label="标签">
          <template v-for="(val, key) in pod.labels">
            <span :key="key">{{ key }}: {{ val }}<br /></span>
          </template>
        </el-form-item>
        <el-form-item label="注解">
          <span v-if="!pod.annonations">——</span>

          <template v-else v-for="(val, key) in pod.annonations">
            <span :key="key">{{ key }}: {{ val }}<br /></span>
          </template>
        </el-form-item>
      </el-form>

      <el-dialog
        title="终端"
        :visible.sync="terminal"
        :close-on-click-modal="false"
        width="80%"
        top="55px"
      >
        <terminal
          v-if="terminal"
          :cluster="cluster"
          :namespace="namespace"
          :pod="podName"
          :container="selectContainer"
        ></terminal>
      </el-dialog>

      <el-dialog
        title="日志"
        :visible.sync="log"
        :close-on-click-modal="false"
        width="80%"
        top="55px"
      >
        <log
          v-if="log"
          :cluster="cluster"
          :namespace="namespace"
          :pod="podName"
          :container="selectContainer"
        ></log>
      </el-dialog>

      <el-dialog
        title="编辑"
        :visible.sync="yamlDialog"
        :close-on-click-modal="false"
        width="60%"
        top="55px"
      >
        <yaml
          v-if="yamlDialog"
          v-model="yamlValue"
          :loading="yamlLoading"
        ></yaml>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="yamlDialog = false" size="small"
            >取 消</el-button
          >
          <el-button plain @click="updatePod()" size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getConfigMap } from '@/api/config_map'
import { Message } from 'element-ui'
import { Terminal } from '@/views/components'
import { Log } from '@/views/components'

export default {
  name: 'PodDetail',
  components: {
    Clusterbar,
    Terminal,
    Log,
    Yaml,
  },
  data() {
    return {
      yamlDialog: false,
      yamlValue: '',
      yamlLoading: true,
      log: false,
      terminal: false,
      cellStyle: { border: 0 },
      loading: true,
      originConfigMap: undefined,
      selectContainer: '',
      eventLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {},
  computed: {
    titleName: function() {
      return ['ConfigMap', this.configMapName]
    },
    configMapName: function() {
      return this.$route.params ? this.$route.params.configMapName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    configMap: function() {
      return {}
    },
  },
  methods: {
    fetchData: function() {
      this.originPods = []
      this.podEvents = []
      this.loading = true
      this.eventLoading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error('获取集群参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.namespace) {
        Message.error('获取命名空间参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.configMapName) {
        Message.error('获取ConfigMap名称参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
    },
    toogleExpand: function(row) {
      let $table = this.$refs.table
      $table.toggleRowExpansion(row)
    },
    envStr: function(env) {
      let s = env.name + ': '
      if (env.value) {
        s += env.value
      } else if (env.valueFrom) {
        if (env.valueFrom.configMapKeyRef) {
          s += `configmap(${env.valueFrom.configMapKeyRef.key}:${env.valueFrom.configMapKeyRef.name})`
        } else if (env.valueFrom.fieldRef) {
          s += `fieldRef(${env.valueFrom.fieldRef.apiVersion}:${env.valueFrom.fieldRef.fieldPath})`
        } else if (env.valueFrom.secretKeyRef) {
          s += `secret(${env.valueFrom.secretKeyRef.key}:${env.valueFrom.secretKeyRef.name})`
        } else {
          s += String(env.valueFrom)
        }
      }
      return s
    },

    getConfigMapYaml: function() {
      if (!this.pod) {
        Message.error('获取Pod参数异常，请刷新重试')
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
      getConfigMap(cluster, this.pod.namespace, this.pod.name, 'yaml')
        .then((response) => {
          this.yamlLoading = false
          this.yamlValue = response.data
        })
        .catch(() => {
          this.yamlLoading = false
        })
    },
  },
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
