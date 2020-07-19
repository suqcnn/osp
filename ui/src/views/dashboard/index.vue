<template>
  <div>
    <clusterbar />
    <div class="dashboard-container">
      <!-- <div class="dashboard-text"></div> -->
      <el-table
        ref="multipleTable"
        :data="tableData"
        class="table-fix"
        tooltip-effect="dark"
        style="width: 100%"
        >
        <el-table-column
          type="selection"
          width="45">
        </el-table-column>
        <el-table-column
          prop="name"
          label="名称"
          width="200"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="namespace"
          label="命名空间"
          width="120"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="containers"
          label="容器"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="restarts"
          label="重启"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="controller"
          label="控制器"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="qos"
          label="QoS"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="age"
          label="时长"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          show-overflow-tooltip>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'

export default {
  name: 'Dashboard',
  components: {
    Clusterbar
  },
  data() {
      return {
        tableData: [{
          name: 'dashboard-metrics-scraper-7cd9fcc8b8-czxx4',
          namespace: 'default',
          containers: 2,
          restarts: 0,
          controller: 'ReplicaSet',
          qos: 'Burstable',
          age: '1d',
          status: 'Running'
        },]
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
</style>
