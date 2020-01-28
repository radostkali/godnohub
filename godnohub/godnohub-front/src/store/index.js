import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const urlInfo = '/api/v1/auth/info'

export const store = new Vuex.Store({
  state: {
    is_authenticated: false,
    home_page: undefined,
    username: undefined,
    avatar: undefined,
    card_display: 'full'
  },
  getters: {
    IS_AUTH: state => state.is_authenticated,
    HOME_PAGE: state => state.home_page,
    USERNAME: state => state.username,
    AVATAR: state => state.avatar,
    CARD_DISPLAY: state => state.card_display
  },
  mutations: {
    LOGIN: (state) => {
      state.is_authenticated = true
    },
    LOGOUT: (state) => {
      state.is_authenticated = false
      state.home_page = undefined
    },
    SET_HOME_PAGE: (state, pageId) => {
      state.home_page = pageId
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_CARD_DISPLAY: (state, display) => {
      state.card_display = display
    }
  },
  actions: {
    LOGIN (context) {
      context.commit('LOGIN')
    },
    LOGOUT (context) {
      context.commit('LOGOUT')
    },
    SET_INFO (context) {
      axios.get(urlInfo)
        .then(response => {
          let pageId = response.data.page_id
          let username = response.data.username
          let avatar = response.data.avatar
          context.commit('SET_HOME_PAGE', pageId)
          context.commit('SET_USERNAME', username)
          context.commit('SET_AVATAR', avatar)
        })
        .catch(error => {
          console.log(error)
        })
    },
    CHANGE_DISPLAY (context, display) {
      context.commit('SET_CARD_DISPLAY', display)
    }
  }
})
