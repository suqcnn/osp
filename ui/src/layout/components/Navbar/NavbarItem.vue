<template>
  <div class="navbar-item">
    <el-menu :default-active="activeMenu" mode="horizontal" >
        <el-menu-item index="settings" class="submenu-class" v-on:click="globalClick">全局配置</el-menu-item>
        <el-submenu index="cluster" class="submenu-class">
            <template slot="title" class="submenu-class">集群管理</template>
              <el-menu-item v-if="loading" index="load" v-loading="loading" class="submenu-class" disabled>加载中...</el-menu-item>
              <el-menu-item v-if="noCluster" index="none" class="submenu-class" v-on:click="globalClick" disabled>暂无集群，请添加集群</el-menu-item>
              <el-menu-item v-for="c in clusters" :key="c.name" :index="c.name" v-on:click="clusterClick(c.name)"><a >{{ c.name }}</a></el-menu-item>
            <!-- <el-menu-item index="test1" class="submenu-class" v-on:click="clusterClick('test1')">test1</el-menu-item>
            <el-menu-item index="test2" class="submenu-class" v-on:click="clusterClick('test2')">test2</el-menu-item> -->
        </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import { listCluster } from '@/api/cluster'

export default {
  data() {
    return {
      clusters: [],
      loading: true,
      noCluster: false,
    };
  },
  created() {
    this.fetchClusters()
  },
  computed: {
    activeMenu() {
      const route = this.$route
      const { meta } = route
      if (meta.group && meta.group == 'cluster') {
        this.$store.commit('SET_CLUSTER', route.params.name)
        return route.params.name
      }
      return meta.group
    },
  },
  methods: {
    fetchClusters() {
      this.noCluster = false
      this.loading = true
      listCluster().then(response => {
        this.loading = false
        this.clusters = response.data
        if (!this.clusters) {
          this.noCluster = true
        }
      }).catch(() => {
        this.loading = false
      })
    },
    globalClick() {
      this.$store.commit('SET_CLUSTER', '')
      this.$router.push({name: 'settinsCluster'})
    },
    clusterClick(clusterName) {
      this.$store.commit('SET_CLUSTER', clusterName)
      this.$router.push({name: 'cluster', params: {'name': clusterName}})
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar-item {
  position: relative;
  display: inline-block;
  height: 50px;
  line-height: 50px;
  overflow: hidden;
  margin-left: 90px;

}
</style>
