<template>
  <div class="navbar-logo-container">
    <transition name="navbarLogoFade">
      <router-link key="logo" class="navbar-logo-link" to="/">
        <!-- <img v-if="logo" :src="logo" class="navbar-logo"> -->
        <h1 class="navbar-title">{{ title }} </h1>
      </router-link>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'NavbarLogo',
  data() {
    return {
      title: 'OpenSpace',
      logo: 'https://wpimg.wallstcn.com/69a1c46c-eb1c-4b46-8bd4-e9e686ef5251.png'
    }
  }
}
</script>

<style lang="scss" scoped>
.navbarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.navbarLogoFade-enter,
.navbarLogoFade-leave-to {
  opacity: 0;
}

.navbar-logo-container {
  position: relative;
  display: inline-block;
  // width: 100%;
  height: 50px;
  line-height: 50px;
  overflow: hidden;

  & .navbar-logo-link {
    height: 100%;
    // width: 100%;

    & .navbar-title {
      margin: 0px 0px 0px 25px;
      font-weight: 500;
      font-size: 20px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
    }
  }

}
</style>
