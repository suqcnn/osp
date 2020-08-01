<template>
  <div>
    <clusterbar titleName="Cluster" />
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
        <el-table-column
          prop="name"
          label="名称"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          min-width="34%"
          show-overflow-tooltip>
        </el-table-column>

        <el-table-column
          label=""
          width="80">

          <template >
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
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { listCluster } from '@/api/cluster'

export default {
  name: 'SettingsCluster',
  components: {
    Clusterbar
  },
  created() {
    this.fetchData()
  },
  computed: {
    clustersWatch: function() {
      return this.$store.getters["ws/podWatch"]
    }
  },
  watch: {
    clustersWatch: function (newObj) {
      console.log("watch obj", newObj)
    }
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
      maxHeight: window.innerHeight - 150,
      loading: true,
      clusters: []
    }
  },
  methods: {
    fetchData() {
      this.loading = true
      listCluster().then(response => {
        this.loading = false
        this.clusters = response.data
      }).catch(() => {
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
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
