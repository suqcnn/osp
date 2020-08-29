<template>
    <div>
        <clusterbar :titleName="titleName" :nsFunc="nsSearch" :nameFunc="nameSearch" />
        <div class="dashboard-container">
            <el-table
            ref="multipleTable"
            :data="configMaps"
            class="table-fix"
            tooltip-effect="dark"
            :max-height="maxHeight"
            style="width: 100%"
            v-loading="loading"
            :cell-style="cellStyle"
            :default-sort = "{prop: 'name'}"
            row-key="uid"
            >
            <el-table-column
              type="selection"
              width="45">
            </el-table-column>
            <el-table-column
              prop="name"
              label="名称"
              min-width="45"
              show-overflow-tooltip>
              <template slot-scope="scope">
                <span class="name-class" v-on:click="nameClick(scope.row.namespace, scope.row.name)">
                  {{ scope.row.name }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="namespace"
              label="命名空间"
              min-width="40"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              prop="keys"
              label="Keys"
              min-width="45"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column
            prop="create_time"
            label="创建时间"
            min-width="45"
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
                    <el-dropdown-item @click.native.prevent="nameClick(scope.row.namespace, scope.row.name)">
                      <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="detail" />
                      <span style="margin-left: 5px;">详情</span>
                    </el-dropdown-item>
                    <el-dropdown-item @click.native.prevent="getPodYaml(scope.row.namespace, scope.row.name)">
                      <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="edit" />
                      <span style="margin-left: 5px;">修改</span>
                    </el-dropdown-item>
                    <el-dropdown-item @click.native.prevent="deletePods([{namespace: scope.row.namespace, name: scope.row.name}])">
                      <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px; vertical-align: -0.25em" icon-class="delete" />
                      <span style="margin-left: 5px;">删除</span>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
        </div>
    </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { Message } from 'element-ui'
import { listConfigMaps } from '@/api/config_map'

export default {
    name: "ConfigMap",
    components: {
        Clusterbar,
    },
    data() {
        return {
            titleName: ["ConfigMap"],
            originConfigMaps: [],
            search_name: "",
            search_ns: [],
            cellStyle: {border: 0},
            maxHeight: window.innerHeight - 150,
            loading: true
        }
    },
    created() {
        this.fetchData()
    },
    computed: {
        configMaps: function() {
            let data = []
            for (let c of this.originConfigMaps) {
                if (this.search_ns.length > 0 && this.search_ns.indexOf(c.namespace) < 0) continue
                if (this.search_name && !c.name.includes(this.search_name)) continue
                var str = ""
                for (let s of c.keys) {
                    str += s + ","
                }
                console.log(str)
                if (str.length > 0) {
                    str = str.substr(0, str.length - 1)
                }
                c['keys'] = str
                data.push(c)
            }
            return data
        }
    },
    methods: {
        nsSearch: function(vals) {
            this.search_ns = []
            for(let ns of vals) {
                this.search_ns.push(ns)
            }
        },
        nameSearch: function(val) {
            this.search_name = val
        },
        fetchData: function() {
            this.loading = true
            this.originConfigMaps = []
            const cluster = this.$store.state.cluster
            if (cluster) {
                listConfigMaps(cluster).then(response => {
                    this.loading = false
                    this.originConfigMaps = response.data
                }).catch(() => {
                    this.loading = false
                })
            } else {
                this.loading = false
                Message.error("获取集群异常，请刷新重试.")
            }
        }
    }
}
</script>