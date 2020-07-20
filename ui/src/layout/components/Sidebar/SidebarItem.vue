<template>
  <div v-if="!item.hidden">
    <template v-if="hasOneShowingChild(item.children,item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!item.alwaysShow">
      <a v-if="isDisplay(onlyOneChild.meta)" v-on:click="routeTo(onlyOneChild)">
      <!-- <app-link v-if="isDisplay(onlyOneChild.meta)" to="{name: node, params: {name: test}}"> -->
        <el-menu-item :index="onlyOneChild.name" :class="{'submenu-title-noDropdown':!isNest}">
          <item :icon="onlyOneChild.meta.icon||(item.meta&&item.meta.icon)" :title="onlyOneChild.meta.title" />
        </el-menu-item>
      <!-- </app-link> -->
      </a>
    </template>

    <el-submenu v-else-if="isDisplay(item.meta)" ref="subMenu" :index="item.name" popper-append-to-body>
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta && item.meta.icon" :title="item.meta.title" />
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :is-nest="true"
        :item="child"
        :base-path="resolvePath(child.path)"
        class="nest-menu"
      />
    </el-submenu>
  </div>
</template>

<script>
import path from 'path'
import Item from './Item'

export default {
  name: 'SidebarItem',
  components: { Item },
  props: {
    // route object
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    // To fix https://github.com/PanJiaChen/vue-admin-template/issues/237
    // TODO: refactor with render function
    this.onlyOneChild = null
    return {}
  },
  methods: {
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          // Temp set(will be used if only has one showing child)
          this.onlyOneChild = item
          return true
        }
      })

      // When there is only one child router, the child router is displayed by default
      if (showingChildren.length === 1) {
        return true
      }

      // Show parent if there are no child router to display
      if (showingChildren.length === 0) {
        this.onlyOneChild = { ... parent, path: '', noShowingChildren: true }
        return true
      }

      return false
    },
    resolvePath(routePath) {
      return path.resolve(this.basePath, routePath)
    },
    routeTo(item) {
      const route = this.$route
      console.log(item)
      this.$router.push({name: item.name, params: route.params})
    },
    isDisplay(meta) {
      if (!meta) {
        return false
      }
      const route = this.$route
      const routeMeta = route.meta
      if (!meta.side && !routeMeta.side) {
        return true
      }
      if (meta.side && !routeMeta.side) {
        return false
      }
      if (meta.side == routeMeta.side) {
        return true
      }
      return false
    }
  }
}
</script>
