<template>
  <div class="navbar-item">
    <el-menu :default-active="activeMenu" mode="horizontal" >
        <el-menu-item index="settings" class="submenu-class" v-on:click="globalClick">全局配置</el-menu-item>
        <el-submenu index="cluster" class="submenu-class">
            <template slot="title" class="submenu-class">集群管理</template>
            <el-menu-item v-if="loading" index="load" v-loading="loading" class="submenu-class" disabled>加载中...</el-menu-item>
            <el-menu-item v-if="noCluster" index="none" class="submenu-class" v-on:click="globalClick" disabled>暂无集群，请添加集群</el-menu-item>
            <template v-for="c in clusters">
              <el-menu-item v-if="c.status === 'Pending'" :key="c.name" :index="c.name" disabled>
                <!-- <a :underline="false" :disabled="true">{{ c.name }}</a> -->
                {{c.name}}
              </el-menu-item>
              <el-menu-item v-else :key="c.name" :index="c.name" v-on:click="clusterClick(c.name)">
                <a >{{ c.name }}</a>
              </el-menu-item>
            </template>
            
        </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import { listCluster } from '@/api/cluster'

export default {
  data() {
    return {
      origin_clusters: [],
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
        this.$store.dispatch('watchCluster', route.params.name)
        return route.params.name
      }
      this.$store.dispatch('watchCluster', '')
      return meta.group
    },
    clusters() {
      var cs = [];
      for(var c of this.origin_clusters) {
        cs.push(c)
      }
      cs.sort((a, b) => {
        if(a.status > b.status) return 1;
        if(a.name > b.name) return 1;
        return -1;
      })
      return cs;
    }
  },
  methods: {
    fetchClusters() {
      this.noCluster = false
      this.loading = true
      listCluster().then(response => {
        this.loading = false
        this.origin_clusters = response.data ? response.data : []
        if (!this.origin_clusters) {
          this.noCluster = true
        }
      }).catch(() => {
        this.loading = false
      })
    },
    globalClick() {
      // this.$store.dispatch('watchCluster', '')
      this.$router.push({name: 'settinsCluster'})
    },
    clusterClick(clusterName) {
      // this.$store.dispatch('watchCluster', clusterName)
      console.log(clusterName);
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
