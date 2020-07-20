<template>
  <div class="cluster-bar">
    <el-breadcrumb class="app-breadcrumb" separator="/">
      <transition-group name="breadcrumb">
        <el-breadcrumb-item key="pods">
          <span class="no-redirect">Pods</span>
        </el-breadcrumb-item>
      </transition-group>
    </el-breadcrumb>

    <!-- <svg-icon class="icon-create" icon-class="create"/> -->
    <!-- <svg-icon class="icon-create" icon-class="delete"/> -->

    <div class="right">
      <el-select v-model="value1" multiple placeholder="命名空间" size="small">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-input
        size="small"
        placeholder="搜索"
        suffix-icon="el-icon-search"
        v-model="input4">
      </el-input>
    </div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'

export default {
  name: 'Clusterbar',
  data() {
      return {
        input4: "",
        options: [{
          value: 'default',
          label: 'default'
        }, {
          value: 'kube-system',
          label: 'kube-system'
        }, {
          value: 'kube-public',
          label: 'kube-public'
        }],
        value1: "",
      }
    }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/variables.scss";
.cluster-bar {
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
</style>
