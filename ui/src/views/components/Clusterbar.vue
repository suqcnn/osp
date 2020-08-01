<template>
  <div class="cluster-bar">
    <el-breadcrumb class="app-breadcrumb" separator="/">
      <transition-group name="breadcrumb">
        <el-breadcrumb-item :key="titleName">
          <span class="no-redirect">{{ titleName }}</span>
        </el-breadcrumb-item>
      </transition-group>
    </el-breadcrumb>

    <!-- <svg-icon class="icon-create" icon-class="create"/> -->
    <!-- <svg-icon class="icon-create" icon-class="delete"/> -->

    <div class="right">

      <!-- <el-button plain size="small">添加集群</el-button> -->
      <el-select v-if="typeof nsFunc !== 'undefined'" v-model="nsInput" @change="nsChange" multiple placeholder="命名空间" size="small">
        <el-option
          v-for="item in namespaces"
          :key="item.name"
          :label="item.name"
          :value="item.name">
        </el-option>
      </el-select>
      <el-input v-if="typeof nameFunc !== 'undefined'"
        size="small"
        placeholder="搜索"
        v-model="nameInput"
        @input="nameDebounce"
        suffix-icon="el-icon-search">
      </el-input>
    </div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import { listNamespace } from '@/api/namespace'
import { Message } from 'element-ui'

let nameTimer
export default {
  name: 'Clusterbar',
  props: {
    titleName: {
      type: String,
      required: true,
      default: ""
    },
    nsFunc: {
      type: Function,
      required: false,
      default: undefined
    },
    nameFunc: {
      type: Function,
      required: false,
      default: undefined
    }
  },
  data() {
    return {
      nameInput: "",
      nsInput: [],
      namespaces: [{
        value: 'default',
        label: 'default'
      }, {
        value: 'kube-system',
        label: 'kube-system'
      }, {
        value: 'kube-public',
        label: 'kube-public'
      }, {
        value: 'osp',
        label: 'osp'
      }],
    }
  },
  created() {
    if (typeof this.nsFunc !== 'undefined') {
      this.fetchNamespace()
    }
  },
  methods: {
    nsChange(vals) {
      if (this.nsFunc) {
        this.nsFunc(vals)
      }
    },
    nameDebounce: function() {
      if (this.nameFunc) {
        if (nameTimer) {
          clearTimeout(nameTimer)
        }
        nameTimer = setTimeout(() => {
          this.nameFunc(this.nameInput)
          // this.nameModel = this.nameInput
          nameTimer = undefined
        }, 500)
      }
    },
    fetchNamespace: function() {
      this.namespaces = []
      console.log('asdfe')
      const cluster = this.$store.state.cluster
      if (cluster) {
        listNamespace(cluster).then(response => {
          this.namespaces = response.data
          this.namespaces.sort((a, b) => {return a.name > b.name ? 1 : -1})
        }).catch(() => {
        })
      } else {
        Message.error("获取集群异常，请刷新重试")
      }
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
      margin-left: 15px;
      .el-select__tags {
        white-space: nowrap;
        overflow: hidden;
      }
    }

  }
}
</style>
