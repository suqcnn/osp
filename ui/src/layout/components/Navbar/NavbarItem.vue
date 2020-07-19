<template>
  <div class="navbar-item">
    <el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1" class="submenu-class">全局配置</el-menu-item>
        <el-submenu index="2" class="submenu-class">
            <template slot="title" class="submenu-class">集群管理</template>
            <el-menu-item index="2-1" class="submenu-class">test1</el-menu-item>
            <el-menu-item index="2-2" class="submenu-class">test2</el-menu-item>
        </el-submenu>
    </el-menu>
  </div>
</template>

<script>

export default {
  data() {
    return {
      activeIndex: '1',
      activeIndex2: '1'
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
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
