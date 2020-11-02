<template>
  <div>
    <div class="member-bar">
      <el-breadcrumb class="app-breadcrumb" separator="/">
        <transition-group name="breadcrumb">
          <el-breadcrumb-item key="pods">
            <span class="no-redirect">Cluster</span>
          </el-breadcrumb-item>
        </transition-group>
      </el-breadcrumb>
      <div class="right">
        <el-button size="mini" @click="createClusterFormVisible = true"
          >创建集群</el-button
        >
        <el-input size="small" placeholder="搜索" suffix-icon="el-icon-search">
        </el-input>
      </div>
    </div>
    <div class="dashboard-container" ref="tableCot">
      <el-table
        v-loading="loading"
        :data="clusters"
        class="table-fix"
        :max-height="maxHeight"
        tooltip-effect="dark"
        style="width: 100%"
        fit
      >
        <!-- <div slot="empty">
          <el-link >添加集群</el-link>
        </div> -->
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
          <template>
            <!-- <el-button
              @click.native.prevent="deleteRow(scope.$index, tableData)"
              type="text"
              size="small">
              删除
            </el-button> -->
            <el-link :underline="false" style="font-size: 13px">删除</el-link>
          </template>
        </el-table-column>
      </el-table>
      <!-- {{ clustersWatch }} -->
    </div>
    <div>
      <el-dialog title="创建集群" :visible.sync="createClusterFormVisible">
        <el-form :model="form">
          <el-form-item label="集群名称">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="createClusterFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleCreateCluster"
            >确 定</el-button
          >
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
// import { Clusterbar } from '@/views/components'
import { listCluster, createCluster } from '@/api/cluster'
import { Message } from 'element-ui'

export default {
  name: 'SettingsCluster',
  components: {
    // Clusterbar
  },
  created() {
    this.fetchData()
  },
  // computed: {
  //   clustersWatch: function() {
  //     return this.$store.getters['ws/podWatch']
  //   },
  // },
  // watch: {
  //   clustersWatch: function(newObj) {
  //     console.log('watch obj', newObj)
  //   },
  // },
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
