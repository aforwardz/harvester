import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
const state = {
  LoginState: false,
  DataShown: [],
  LoadingDataShown: false,
  LastDataRequest: {
    url: '',
    param: {}
  }
};

// var DataShown = []

export default new Vuex.Store({
  state
})
