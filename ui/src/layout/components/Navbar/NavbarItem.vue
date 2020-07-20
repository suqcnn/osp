<template>
  <div class="navbar-item">
    <el-menu :default-active="activeMenu" mode="horizontal" >
        <el-menu-item index="settings" class="submenu-class" v-on:click="globalClick">全局配置</el-menu-item>
        <el-submenu index="cluster" class="submenu-class">
            <template slot="title" class="submenu-class">集群管理</template>
            <el-menu-item index="test1" class="submenu-class" v-on:click="clusterClick('test1')">test1</el-menu-item>
            <el-menu-item index="test2" class="submenu-class" v-on:click="clusterClick('test2')">test2</el-menu-item>
        </el-submenu>
    </el-menu>
  </div>
</template>

<script>

export default {
  data() {
    return {
    };
  },
  computed: {
    activeMenu() {
      const route = this.$route
      const { meta } = route
      if (meta.side) {
        return meta.side
      }
      if (!meta.side || meta.side == "cluster") {
        return route.params.name
      }
      return "cluster"
    },
  },
  methods: {
    globalClick() {
      this.$router.push({name: 'settinsCluster'})
    },
    clusterClick(clusterName) {
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
