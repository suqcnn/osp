import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import ws from "./modules/ws";

// console.log(ws)

Vue.use(Vuex)

const getters = {
  token: state => state.user.token,
  username: state => state.user.name,
  clusterWatch: state => state.ws.clusterWatch,
  uidWatch: (state) => (uid) => {
    if (state.ws.clusterWatch && state.ws.clusterWatch.resource && state.ws.clusterWatch.resource.metadata.uid == uid) {
      return state.ws.clusterWatch
    }
  }
}

const state = {
  cluster: "",
}

const mutations = {
  SET_CLUSTER: (state, cluster) => {
    state.cluster = cluster
  },
}

const store = new Vuex.Store({
  modules: {
    user,
    ws
  },
  getters,
  state,
  mutations
})

export default store
