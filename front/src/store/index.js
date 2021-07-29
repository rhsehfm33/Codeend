import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import contest from './modules/contest'
import api from '@oj/api'
import types from './types'

Vue.use(Vuex)
// node.js는 process.env 객체의 속성으로 시스템의 환경 변수를 나타내는
// process 변수가 존재함
// process.env.NODE_ENV 표현식은 __DEV__ 상수처럼 빌드 타임에 문자열로 대체됨
// 개발 모드
const debug = process.env.NODE_ENV !== 'production'

// State 상태
const rootState = {
  website: {},
  modalStatus: {
    mode: 'login', // or 'register',
    // visible 보여지는 상태가 아님
    visible: false
  }
}

// Getters
const rootGetters = {
  'website' (state) {
    return state.website
  },
  'modalStatus' (state) {
    return state.modalStatus
  }
}

// Mutations
const rootMutations = {
  [types.UPDATE_WEBSITE_CONF] (state, payload) {
    state.website = payload.websiteConfig
  },
  [types.CHANGE_MODAL_STATUS] (state, {mode, visible}) {
    if (mode !== undefined) {
      state.modalStatus.mode = mode
    }
    if (visible !== undefined) {
      state.modalStatus.visible = visible
    }
  }
}

// Actions
const rootActions = {
  // api의 getWebsiteConf 함수에 commit을 주고 호출
  getWebsiteConfig ({commit}) {
    api.getWebsiteConf().then(res => {
      // commit 함수에 types의 UPDATE_WEBSITE_CONF : WebsiteConf 업데이트 함수 호출
      // websiteConfig에 응답받은 데이터의 데이터를 받음
      commit(types.UPDATE_WEBSITE_CONF, {
        websiteConfig: res.data.data
      })
    })
  },
  changeModalStatus ({commit}, payload) {
    commit(types.CHANGE_MODAL_STATUS, payload)
  },
  changeDomTitle ({commit, state}, payload) {
    if (payload && payload.title) {
      window.document.title = state.website.website_name_shortcut + ' | ' + payload.title
    } else {
      window.document.title = state.website.website_name_shortcut + ' | ' + state.route.meta.title
    }
  }
}

export default new Vuex.Store({
  modules: {
    user,
    contest
  },
  state: rootState,
  getters: rootGetters,
  mutations: rootMutations,
  actions: rootActions,
  strict: debug
})

export { types }
