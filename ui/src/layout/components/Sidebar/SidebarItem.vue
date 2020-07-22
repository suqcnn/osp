<template>
  <div>
    <template v-if="item.hidden">
      <template v-if="item.children && item.children.length > 0">
        <sidebar-item
          v-for="child in item.children"
          :key="child.path"
          :item="child"
          class="nest-menu"
        />
      </template>
    </template>
    <template v-else-if="item.meta && item.meta.group && item.meta.group == pathGroup">
      <template v-if="item.children && item.children.length > 0">
        <el-submenu ref="subMenu" :index="item.name" popper-append-to-body>
          <template slot="title">
            <item v-if="item.meta" :icon="item.meta && item.meta.icon" :title="item.meta.title" />
          </template>
          <sidebar-item
            v-for="child in item.children"
            :key="child.path"
            :item="child"
            class="nest-menu"
          />
        </el-submenu>
      </template>
      <template v-else>
        <a v-on:click="routeTo(item)">
          <el-menu-item :index="item.name">
            <item :icon="item.meta && item.meta.icon" :title="item.meta.title" />
          </el-menu-item>
        </a>
      </template>
    </template>
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
  },
  data() {
    // To fix https://github.com/PanJiaChen/vue-admin-template/issues/237
    // TODO: refactor with render function
    // this.onlyOneChild = null
    return {}
  },
  computed: {
    pathGroup() {
      const meta = this.$route.meta
      var group = ''
      if (meta && meta.group) {
        group = meta.group
      }
      return group
    }
  },
  methods: {
    resolvePath(routePath) {
      return path.resolve(this.basePath, routePath)
    },
    routeTo(item) {
      const route = this.$route
      this.$router.push({name: item.name, params: route.params})
    },
  }
}
</script>
