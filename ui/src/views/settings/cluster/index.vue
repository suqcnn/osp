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
                <el-dropdown-item @click.native.prevent="nameClick(scope.row.namespace, scope.row.name)" v-if="scope.row.status === 'Pending'">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="link" />
                  <span style="margin-left: 5px;">连接</span>
                </el-dropdown-item>
                <el-dropdown-item @click.native.prevent="deleteClusters([{namespace: scope.row.namespace, name: scope.row.name}])">
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
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { listCluster, createCluster } from '@/api/cluster'
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
      form: {
        name: '',
      },
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
      }
      createCluster(this.form)
        .then(() => {
          this.loading = false
          this.fetchData()
        })
        .catch(() => {
          this.loading = false
        })
      this.createClusterFormVisible = false
    },
    deleteClusters(delClusters) {

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
