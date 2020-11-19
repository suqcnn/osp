<template>
  <div class="cluster-bar">
    <el-breadcrumb class="app-breadcrumb" separator-class="el-icon-arrow-right">
        <el-breadcrumb-item v-for="t in titleName" :key="t" class="no-redirect">
          {{ t }}
        </el-breadcrumb-item>
    </el-breadcrumb>
    <!-- <svg-icon class="icon-create" icon-class="create"/> -->
    <!-- <svg-icon class="icon-create" icon-class="edit"/> -->
    <el-link v-if="typeof editFunc !== 'undefined'" class="icon-create" @click="editFunc()"><svg-icon icon-class="edit"/></el-link>
    <el-link v-if="typeof delFunc !== 'undefined'" class="icon-create" @click="delFunc()"><svg-icon icon-class="delete"/></el-link>

    <div class="right">
      <!-- <el-button v-if="typeof delFunc !== 'undefined'"  size="small" plain @click="delFunc()">删 除</el-button> -->
      <el-button v-if="typeof createFunc !== 'undefined'" size="small" plain @click="createFunc()">{{ createDisplay }}</el-button>
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
      type: Array,
      required: true,
      default: () => {return []}
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
    },
    delFunc: {
      type: Function,
      required: false,
      default: undefined,
    },
    editFunc: {
      type: Function,
      required: false,
      default: undefined,
    },
    createDisplay: {
      type: String,
      required: false,
      default: "创建"
    },
    createFunc: {
      type: Function,
      required: false,
      default: undefined,
    }
  },
  data() {
    return {
      nameInput: "",
      nsInput: [],
      namespaces: [],
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
  // box-shadow: inset 0 0 4px rgba(0, 21, 41, 0.1);
  border: 1px solid #EBEEF5;
  margin: 15px 20px 0px;

  .app-breadcrumb.el-breadcrumb {
    display: inline-block;
    font-size: 20px;
    line-height: 58px;
    margin-left: 8px;

    .no-redirect {
      // color: #97a8be;
      cursor: text;
      font-size: 23px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
    }
    .no-redirect:first-child {
      margin-left: 15px;
    }
  }

  .icon-create:first {
    margin-left: 15px;
  }

  .icon-create {
    display: inline-block;
    line-height: 55px;
    margin-left: 15px;
    vertical-align: 0.95em;
    font-size: 23px;
  }

  .right {
    float: right;
    height: 100%;
    line-height: 52px;
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
<style >
/* .right .el-button.is-plain {
  border-color: #f78989;
  color: #f78989;
}
.right .el-button.is-plain:hover {
  border-color: #f56c6c;
  color: #f56c6c;
}
.right .el-button.is-plain:focus {
  border-color: #f56c6c;
  color: #f56c6c;
} */
</style>
