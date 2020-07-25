import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'

Vue.use(Vuex)

const getters = {
  token: state => state.user.token,
  username: state => state.user.name
}

const store = new Vuex.Store({
  modules: {
    user
  },
  getters
})

export default store
