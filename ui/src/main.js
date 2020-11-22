import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'

import router from './router'
import store from './store'
import '@/permissions'
// import '@/websocket'

import '@/styles/index.scss' // global css
import '@/icons' // icon
import VueClipboard from 'vue-clipboard2';

Vue.use(VueClipboard)

Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App),
}).$mount('#app')
