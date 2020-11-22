<template>
  <div>
    <clusterbar :titleName="titleName" :nameFunc="nameSearch" :createFunc="createClusterDialog" createDisplay="创建集群"/>
    <div class="dashboard-container" ref="tableCot">
      <el-table
        :data="clusters"
        class="table-fix"
        tooltip-effect="dark"
        :max-height="maxHeight"
        style="width: 100%"
        v-loading="loading"
        :cell-style="cellStyle"
        :default-sort = "{prop: 'name'}"
        row-key="name"
      >
        <el-table-column prop="name" label="名称" show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          min-width="34%"
          show-overflow-tooltip
        >
        </el-table-column>

        <el-table-column label="" width="80">
          <template slot-scope="scope">
            <!-- <el-button
              @click.native.prevent="deleteRow(scope.$index, tableData)"
              type="text"
              size="small">
              删除
            </el-button> -->
            <!-- <el-link :underline="false" style="font-size: 13px">删除</el-link> -->
            <el-dropdown size="medium" >
              <el-link :underline="false"><svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" /></el-link>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native.prevent="clusterConnectToken=scope.row.token; clusterConnectDialog = true" v-if="scope.row.status === 'Pending'">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="link" />
                  <span style="margin-left: 5px;">连接</span>
                </el-dropdown-item>
                <el-dropdown-item @click.native.prevent="deleteClusters([{name: scope.row.name}])">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="delete" />
                  <span style="margin-left: 5px;">删除</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-dialog title="创建集群" :visible.sync="createClusterFormVisible" :close-on-click-modal="false">
        <el-form :model="form">
          <el-form-item label="集群名称">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="createClusterFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleCreateCluster">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div>
      <el-dialog title="集群导入" :visible.sync="clusterConnectDialog" :close-on-click-modal="false">
        <div style="font-size: 15px;">请在现有Kubernetes集群上运行下面的kubeclt命令，以连接OpenSpace平台：</div>
        <!-- <div style="margin-top: 25px; font-size: 15px;">
          <span style="padding: 10px;background-color:#606266; color: rgb(217, 236, 255); ">
            kubectl apply -f http://localhost:8080/v1/import/{{ clusterConnectToken }}
          </span>
          <span style="padding: 10px; border: 1px solid #606266; border-radius: 0px 3px 3px 0px;" class="copy-btn" v-clipboard:copy="f" v-clipboard:success="onCopy" v-clipboard:error="onError">
            <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="copy" />
            复制
          </span>
        </div> -->
        <div style="margin-top: 15px;">
          <el-tag type="info" style="font-size: 14px; border-radius: 4px 0px 0px 4px; border-right-width: 0px;">
            {{ copyCluster }}
          </el-tag>
          <!-- <el-tag type="" style="font-size: 14px; border-radius: 0px 4px 4px 0px;">复制</el-tag> -->
          <el-button plain size="small" slot="append" 
              style="height: 32px; border-radius: 0px 4px 4px 0px; padding: 10px 15px;"
              v-clipboard:copy="copyCluster" v-clipboard:success="onCopy" v-clipboard:error="onError">
              复制
          </el-button>
        </div>
        <div style="font-size: 13px; margin-top: 8px; color: #e6a23c;">
          *注意：请将上述访问地址{{this.locationAddr}}换为Kubernetes集群可以访问的地址。
        </div>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="clusterConnectDialog = false">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { listCluster, createCluster, deleteCluster } from '@/api/cluster'
import { Message } from 'element-ui'

export default {
  name: 'SettingsCluster',
  components: {
    Clusterbar
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
  data() {
    return {
      titleName: ["Cluster"],
      search_name: '',
      cellStyle: {border: 0},
      maxHeight: window.innerHeight - 150,
      loading: true,
      clusters: [],
      createClusterFormVisible: false,
      clusterConnectDialog: false,
      clusterConnectToken: '',
      form: {
        name: '',
      },
      locationAddr: window.location.origin,
    }
  },
  computed: {
    copyCluster() {
      return `kubectl apply -f ${ this.locationAddr }/v1/import/${ this.clusterConnectToken }`;
    }
  },
  methods: {
    fetchData() {
      this.loading = true
      listCluster()
        .then((response) => {
          this.loading = false
          this.clusters = response.data
        })
        .catch(() => {
          this.loading = false
        })
    },
    nameSearch: function(val) {
      this.search_name = val
    },
    createClusterDialog() {
      this.createClusterFormVisible = true;
    },
    handleCreateCluster() {
      console.log(this.form.name)
      if (!this.form.name) {
        Message.error('集群名称不能为空！')
        return
      }
      createCluster(this.form)
        .then((response) => {
          Message.success("集群添加成功")
          this.createClusterFormVisible = false
          this.loading = false
          this.fetchData()
          this.clusterConnectToken = response.data.token
          this.clusterConnectDialog = true;
        })
        .catch(() => {
          // this.createClusterFormVisible = false
          this.loading = false
        })
    },
    deleteClusters(delClusters) {
      if(delClusters.length <= 0) {
        Message.error('请选择要删除的集群')
        return
      }
      deleteCluster(delClusters).then((response) => {
          this.fetchData()
      }).catch((e) => {
        console.log(e)
      })
    },
    onCopy(e) {
      Message.success("复制成功")
    },
    onError(e) {

    }
  },
}
</script>

<style lang="scss" scoped>
.member-bar {
  transition: width 0.28s;
  height: 55px;
  overflow: hidden;
  box-shadow: inset 0 0 4px rgba(0, 21, 41, 0.1);
  margin: 20px 20px 0px;

  .app-breadcrumb.el-breadcrumb {
    display: inline-block;
    font-size: 20px;
    line-height: 55px;
    margin-left: 8px;

    .no-redirect {
      // color: #97a8be;
      cursor: text;
      margin-left: 15px;
      font-size: 23px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
    }
  }

  .icon-create {
    display: inline-block;
    line-height: 55px;
    margin-left: 20px;
    width: 1.8em;
    height: 1.8em;
    vertical-align: 0.8em;
    color: #bfbfbf;
  }

  .right {
    float: right;
    height: 100%;
    line-height: 55px;
    margin-right: 25px;

    .el-input {
      width: 195px;
      margin-left: 15px;
    }

    .el-select {
      .el-select__tags {
        white-space: nowrap;
        overflow: hidden;
      }
    }
  }
}
.dashboard {
  &-container {
    margin: 10px 30px;
    height: calc(100%);
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.table-fix {
  height: calc(100% - 100px);
}
</style>
