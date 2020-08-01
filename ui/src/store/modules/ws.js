const getDefaultState = () => {
  return {
    clusterWatch: null,
  }
}

const state = getDefaultState()

const mutations = {
  UPDATE_CLUSTER_WATCH: (state, obj) => {
    console.log(obj)
    state.clusterWatch = obj
  },
}

const getters = {
  resourceWatch: (state) => (res) => {
    if (state.clusterWatch && state.clusterWatch.obj && state.clusterWatch.obj == res) {
      return state.clusterWatch
    }
  },
  uidWatch: (state) => (uid) => {
    if (state.clusterWatch && state.clusterWatch.resource && state.clusterWatch.resource.metadata.uid == uid) {
      return state.clusterWatch
    }
  },
  podWatch: ( _, getters ) => {
    return getters.resourceWatch("pods")
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
