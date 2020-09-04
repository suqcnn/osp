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
  // uidWatch: (state) => (uid) => {
  //   if (state.clusterWatch && state.clusterWatch.resource && state.clusterWatch.resource.metadata.uid == uid) {
  //     return state.clusterWatch
  //   }
  // },
  podWatch: ( _, getters ) => {
    return getters.resourceWatch("pods")
  },
  eventWatch: ( _, getters ) => {
    return getters.resourceWatch("event")
  },
  deploymentWatch: ( _, getters ) => {
    return getters.resourceWatch("deployment")
  },
  statefulsetsWatch: ( _, getters ) => {
    return getters.resourceWatch("statefulset")
  },
  daemonsetsWatch: ( _, getters ) => {
    return getters.resourceWatch("daemonset")
  },
  jobsWatch: ( _, getters ) => {
    return getters.resourceWatch("job")
  },
  cronjobsWatch: ( _, getters ) => {
    return getters.resourceWatch("cronjob")
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
