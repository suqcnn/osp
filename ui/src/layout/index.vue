<template>
  <div class="app-wrapper">
    <div class="fixed-header">
      <navbar />
    </div>
    <sidebar class="sidebar-container" />
    <div class="main-container">
      <app-main />
      <!-- main container -->
    </div>
  </div>
</template>

<script>
import { Navbar, Sidebar, AppMain} from './components'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain
  }
}
</script>

<style lang="scss" scoped>
  @import "~@/styles/mixin.scss";
  @import "~@/styles/variables.scss";

  .app-wrapper {
    @include clearfix;
    position: relative;
    height: 100%;
    width: 100%;
  }

  .fixed-header {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 9;
    width: 100%;
    transition: width 0.28s;
  }

  .fixed-sidebar {
    position: fixed;
    top: 50px;
    right: 0;
    z-index: 9;
    width: $sideBarWidth;
    transition: width 0.28s;
  }

</style>
