<template>
  <div>
    <clusterbar :titleName="titleName" :editFunc="getSecretYaml" />
    <div class="dashboard-container">
      <el-form label-position="left" class="pod-item" label-width="180px" v-if="secret.metadata">
        <el-form-item label="名称">
          <span>{{ secret.metadata.name }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ secret.metadata.creationTimestamp }}</span>
        </el-form-item>
        <el-form-item label="Namespace">
          <span>{{ secret.metadata.namespace }}</span>
        </el-form-item>
        <el-form-item label="Type">
          <span>{{ secret.type }}</span>
        </el-form-item>

        <el-form-item label="Labels">
          <span v-if="!secret.metadata.labels">——</span>
          <template v-else v-for="(key, val) in secret.metadata.labels" >
            <span :key="key" class="back-class">{{key}}:{{val}}<br/></span>
          </template>
        </el-form-item>

        <el-form-item label="Annotations">
          <span v-if="!secret.metadata.annotations">——</span>
          <template v-else v-for="(key, val) in secret.metadata.annotations" >
            <span :key="key" class="back-class">{{key}}:{{val}}<br/></span>
          </template>
        </el-form-item>
      </el-form>

      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="Data" name="1" v-if="secret.data">
          <div v-for="(key, val) in secret.data" :key="val" >
            <span >{{val}}</span>
            <el-input type="textarea"  :autosize='{ minRows: 2, maxRows: 4 }' readonly v-model="secret.data[val]">
              <i slot="suffix" class="el-input__icon el-icon-date"></i>
            </el-input>
          </div>
        </el-collapse-item>

      </el-collapse>


      <el-dialog title="编辑" :visible.sync="yamlDialog" :close-on-click-modal="false" width="60%" top="55px">
        <yaml v-if="yamlDialog" v-model="yamlValue" :loading="yamlLoading"></yaml>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="yamlDialog = false" size="small">取 消</el-button>
          <el-button plain size="small">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar, Yaml } from '@/views/components'
import { getSecret } from '@/api/secret'
import { Message } from 'element-ui'

export default {
  name: 'SecretDetail',
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
      originSecret: {},
      eventLoading: true,
      activeNames: ["1"]
    }
  },
  created() {
    this.fetchData()
  },
  watch: {},
  computed: {
    titleName: function() {
      return ['Secret', this.secretName]
    },
    secretName: function() {
      return this.$route.params ? this.$route.params.secretName : ''
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    secret: function() {
      console.log(this.originSecret)
      return this.originSecret
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
      this.originSecret = {}
      this.loading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error('获取集群参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.secretName) {
        Message.error('获取Secret名称参数异常，请刷新重试')
        this.loading = false
        this.eventLoading = false
        return
      }
      if (!this.namespace) {
        Message.error('获取获取Secret命名空间参数异常，请刷新重试')
      }
      getSecret(cluster, this.namespace, this.secretName).then(response => {
        this.loading = false
        this.originSecret = response.data
      }).catch(() => {
        this.loading = false
      })
    },
    getSecretYaml: function() {
      if (!this.secretName) {
        Message.error('获取Secret参数异常，请刷新重试')
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
      getSecret(cluster, this.namespace, this.secretName, 'yaml')
        .then((response) => {
          this.yamlLoading = false
          this.yamlValue = response.data
        })
        .catch(() => {
          this.yamlLoading = false
        })
    },
    updateSecret: function() {
      if (!this.Secret) {
        Message.error("获取Secret参数异常，请刷新重试")
        return
      }
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        return
      }
      console.log(this.yamlValue)
      console.log(this.secret)
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
  width: 60%;
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
