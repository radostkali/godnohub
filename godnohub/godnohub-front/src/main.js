// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import InfiniteLoading from 'vue-infinite-loading'
import {store} from './store'
import VueRouter from 'vue-router'
import NewsPage from './components/NewsPage'
import ContentPage from './components/ContentPage'
import MainPage from './components/MainPage'
import LaterPage from './components/LaterPage'
import VueScrollTo from 'vue-scrollto'

Vue.config.productionTip = false
const vuetifyOptions = { }

Vue.use(Vuetify)
Vue.use(VueScrollTo)
Vue.use(InfiniteLoading)
Vue.use(VueRouter)

var router = new VueRouter({
  mode: 'history',
  base: '/',
  routes: [
    {path: '/', name: 'main', component: MainPage},
    {
      path: '/news',
      name: 'news',
      component: NewsPage
    },
    {
      path: '/later',
      name: 'later',
      component: LaterPage
    },
    {
      path: '/:page',
      name: 'page',
      component: ContentPage,
      children: [
        { path: '', component: ContentPage },
        { path: ':group', name: 'group', component: ContentPage, alias: ':group' }
      ]
    }
  ]
})

Vue.filter('first', function (value) {
  if (!value) return ''
  return value.charAt(0).toUpperCase()
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App },
  vuetify: new Vuetify(vuetifyOptions)
})
