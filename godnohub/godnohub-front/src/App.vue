<template>
  <div id="app">
    <v-app>
      <nav-header style="z-index: 33"></nav-header>
      <main>
        <router-view></router-view>
      </main>
    </v-app>
  </div>
</template>

<script>
  import Vue from 'vue'
  import NavHeader from './components/NavHeader'
  import CreateCard from './components/CreateCard'
  import ToPostStorage from './components/ToPostStorage'
  import CardsContent from './components/CardsContent'
  import Settings from './components/Settings'
  import Card from './components/Card.vue'
  import UserMiniCard from './components/UserMiniCard.vue'
  import RandomCollections from './components/RandomCollections'
  import RandomCard from './components/RandomCard'
  import axios from 'axios'

  Vue.component('card', Card)
  Vue.component('settings', Settings)
  Vue.component('create-card', CreateCard)
  Vue.component('to-post-storage', ToPostStorage)
  Vue.component('cards-content', CardsContent)
  Vue.component('user-mini-card', UserMiniCard)
  Vue.component('random-collections', RandomCollections)
  Vue.component('random-card', RandomCard)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  function getCookie (name) {
    var value = '; ' + document.cookie
    var parts = value.split('; ' + name + '=')
    if (parts.length === 2) return parts.pop().split(';').shift()
    else return false
  }

  export default {
    name: 'app',
    components: {NavHeader},
    mounted: function () {
      let sessionid = getCookie('sessionid')
      if (sessionid) {
        this.$store.dispatch('LOGIN')
        let pageId = this.$store.getters.HOME_PAGE
        if (pageId === undefined) {
          this.$store.dispatch('SET_INFO')
        }
      }
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Montserrat:300,400&display=swap');
  @import url('https://fonts.googleapis.com/css?family=Oswald:200,300,400&display=swap');

  body {
    margin: 0;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: #f1f1f1;
  }

  main {
    text-align: center;
  }

  a {
    text-decoration: none;
  }

  .v-btn {
    text-transform: none !important;
    font-family: 'Roboto', sans-serif;
    letter-spacing: normal !important;
    font-weight: 300 !important;
    font-size: 0.9rem !important;
  }
</style>
