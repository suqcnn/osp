import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import ws from "./modules/ws";

import { getToken } from '@/utils/auth' // get token from cookie

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

var wsConn = null

const actions = {
  watchCluster({ commit }, cluster) {
    console.log('watch cluster', cluster)
    if (wsConn) {
      wsConn.send(JSON.stringify({action: "watchCluster", params: {cluster: cluster}}))
    }
    commit('SET_CLUSTER', cluster)
  },
}

const store = new Vuex.Store({
  modules: {
    user,
    ws
  },
  getters,
  state,
  mutations,
  actions
})

var wsOnOpen = function() {
  console.log("ws connect success")
  wsConn.send(JSON.stringify({action: "watchCluster", params: {cluster: state.cluster}}))
}

var wsOnError = function(e) {
  console.log("ws connect error", e)
  reConnect()
}

var wsOnMessage = function(e) {
  let data = JSON.parse(e.data)
  console.log("receive watch", data)
  store.commit('ws/UPDATE_CLUSTER_WATCH', data)
}

var wsOnClose = function(e) {
  console.log("ws closed", e)
  reConnect()
}

function connect() {
  try{
    var protocal = window.location.protocol == 'http:' ? 'ws':'wss'
    wsConn = new WebSocket(`${protocal}://${window.location.host}/ws/web/connect`)
    wsConn.onopen = wsOnOpen
    wsConn.onerror = wsOnError
    wsConn.onmessage = wsOnMessage
    wsConn.onclose = wsOnClose
  } catch(e) {
    console.log(e)
    reConnect()
  }
}

function reConnect() {
  if(reConnect.lock) return;
  reConnect.lock = true;
  setTimeout(() => {
    reConnect.lock = false;
    connect()
  }, 5000)
}

const hasToken = getToken()

if (hasToken) {
  try{
    connect()
  } catch (error) {
    console.log(error)
  }
}

export default store
