<template>
  <div id="content">

    <div id="sidebar" :class="{ invisible: !isMenuVisible }">
      <v-layout column justify-start fill-height>
        <div class="logo-wrapper">
          <router-link :to="(isAuth) ? {name: 'page', params: {page: homePageId}} : {name: 'main'}">
            <div class="logo">
              <v-img contain src="/static/img/logo.png" height="1.5rem" width="10rem"></v-img>
            </div>
          </router-link>
        </div>
        <div class="filter-wrapper">
          <div class="filter-group">
            <p class="filter-title">Фильтры</p>
          </div>
          <div class="filter-group">
            <v-select
              :items="types"
              v-model="typesPicked"
              label="Группа / Тип"
              attach
              chips
              deletable-chips
              dense
              multiple>
              <template v-slot:no-data>
                <span class="no-data">Здесь нечего выбирать</span>
              </template>
            </v-select>
          </div>
          <div class="filter-group">
            <v-select
              :items="tags"
              v-model="tagsPicked"
              label="Тэги"
              attach
              chips
              deletable-chips
              dense
              multiple
            >
            <template v-slot:no-data>
              <span class="no-data">Здесь нечего выбирать</span>
            </template>
          </v-select>
          </div>
          <div class="filter-group">
            <v-btn @click="applyFilters" class="ml-3" outlined color="teal darken-2">
              <v-icon left>mdi-filter-variant</v-icon> Применить
            </v-btn>
          </div>
        </div>
        <v-spacer></v-spacer>
      </v-layout>
    </div>

    <div class="sidebar-close-layer"
    :class="{ invisible: !isMenuVisible }"
    @click.prevent="toggle"></div>
    <div id="burger"
        :class="{ active: isMenuVisible }"
        @click.prevent="toggle">
      <button type="button" class="burger-button" title="Menu">
        <span class="burger-bar burger-bar--1"></span>
        <span class="burger-bar burger-bar--2"></span>
        <span class="burger-bar burger-bar--3"></span>
      </button>
    </div>

    <div class="container-wrapper">
      <div class="header-space"></div>
      <div class="content-wrapper">
        <cards-content
          :info="info"
          :later="true"
          :news="false"
          :tagsFiltered="[]"
        ></cards-content>

        <div class="empty-page" v-if="info.length === 0">
          <p class="no-cards">
            Пока что здесь не отложено годноты
          </p>
        </div>
      </div>
    </div>

    <infinite-loading
    v-if="!errored"
    :identifier="infiniteId"
    @infinite="infiniteHandler"
    spinner="spiral">
      <div slot="no-more"></div>
      <div slot="no-results"></div>
    </infinite-loading>
    <v-snackbar
      v-model="errored"
      bottom
      color="red lighten-2"
    >
      Тут точно есть что грузить?
    </v-snackbar>

  </div>
</template>

<script>
  import Vuetify from 'vuetify'
  import axios from 'axios'
  import { mapGetters } from 'vuex'

  const urlPostCards = '/api/v1/later/?page=1'
  const urlPostFilters = '/api/v1/later_filters/'

  export default {
    name: 'LaterPage',
    vuetify: new Vuetify(),
    data () {
      return {
        info: [],
        next_page: urlPostCards,
        errored: false,
        isMenuVisible: false,
        infiniteId: 0,
        params: {},
        types: [],
        typesPicked: [],
        tagsPicked: [],
        tags: []
      }
    },
    methods: {
      clearAll () {
        this.info = []
        this.next_page = urlPostCards
        this.errored = false
        this.isMenuVisible = false
        this.params = {}
        this.clearFilters()
      },
      clearFilters () {
        this.types = []
        this.typesPicked = []
        this.tagsPicked = []
        this.tags = []
        this.tagsFiltered = []
      },
      resetCards () {
        this.info = []
        this.next_page = urlPostCards
        this.infiniteId += 1
      },
      infiniteHandler ($state) {
        axios.get(this.next_page, {
          params: this.params
        })
          .then(response => {
            let data = response.data.results
            for (let i = 0; i < data.length; i++) {
              data[i].tags = JSON.parse(data[i].tags)
            }
            this.info = this.info.concat(data)
            this.next_page = response.data.next
            this.buttonActive = true
            if (this.next_page == null) {
              $state.complete()
            } else {
              $state.loaded()
            }
          })
          .catch(error => {
            console.log(error)
            this.errored = true
          })
      },
      applyFilters () {
        if (this.buttonActive) {
          this.buttonActive = false
          this.params = {
            type: this.typesPicked + '',
            tags: this.tagsPicked + ''
          }
          this.resetCards()
        }
      },
      getFilters () {
        axios.get(urlPostFilters)
          .then(response => {
            let data = response.data
            this.types = data.types
            this.tags = data.tags
          })
          .catch(error => {
            console.log(error)
          })
      },
      toggle () {
        this.isMenuVisible = !this.isMenuVisible
      }
    },
    computed: {
      ...mapGetters({
        isAuth: 'IS_AUTH',
        homePageId: 'HOME_PAGE',
        displayChange: 'CARD_DISPLAY'
      })
    },
    watch: {
      'isAuth': function (newVal, oldVal) {
        if (!newVal) {
          this.$router.push('/')
        }
        this.resetCards()
      },
      'displayChange': function () {
        this.infiniteId += 1
      }
    },
    beforeRouteUpdate (to, from, next) {
      this.clearAll()
      this.resetCards()
    },
    beforeRouteEnter (to, from, next) {
      next(vm => {
        if (vm.isAuth) {
          next('')
        } else {
          next('/')
        }
      })
    },
    created () {
      this.getFilters()
    }
  }
</script>

<style scoped>
.container-wrapper {
    float: right;
    width: 80%;
  }

  .content-wrapper {
    width: 100%;
    padding: 1rem;
  }

  @media screen and (max-width: 1000px) {
    .container-wrapper {
      float: right;
      width: 60%;
    }
    div#sidebar {
      width: 40%;
    }
  }

  .owner-card-modile {
    display: none !important;
  }

  @media screen and (max-width: 820px) {
    .owner-card {
      display: none !important;
    }

    .owner-card-modile {
      display: flex !important;
    }
  }

  @media screen and (max-width: 600px) {
    .container-wrapper {
      width: 100%;
    }

    div#sidebar {
      width: 21rem;
    }

    div.sidebar-close-layer {
      display: block;
    }

    #sidebar.invisible {
      left: -21rem;
    }

    .sidebar-close-layer.invisible {
      display: none;
    }

    .logo-wrapper {
      display: flex;
      justify-content: center;
    }
  }


  .logo-wrapper {
    width: 31%;
    margin-top: 1rem;
    margin-left: 3rem;
  }

  .header-space {
    height: 3rem;
  }

  .row {
    margin: 0;
  }

  /* Sidebar */
  #sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    min-height: 31rem;
    width: 20%;
    z-index: 9;
    overflow: scroll;
    -ms-overflow-style: none;
    scrollbar-width: none;
    background: #FAFAFA;
    box-shadow: inset -1px 0px #00000030;
    transition: 0.3s all ease-out;
  }

  #sidebar::-webkit-scrollbar {
    display: none;
  }

  .sidebar-close-layer {
    display: none;
    position: fixed;
    right: 0;
    top: 0;
    height: 100%;
    width: 100%;
    z-index: 3;
  }

  .filter-wrapper {
    margin-top: 1.3rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .filter-group {
    margin-bottom: 1rem;
  }

  .filter-title {
    margin: 0;
    color: #929292;
    font-size: 0.8rem;
  }

  .filter-name {
    text-align: left;
    margin-left: 1rem;
    color: #00000070;
  }

  .v-select {
    margin-left: 7%;
    width: 85%;
  }

  /* Menu toogle */
  .burger-button:focus {
    outline: 0;
  }

  .burger-button {
    cursor: pointer;
    position: relative;
    height: 30px;
    width: 32px;
    display: block;
    z-index: 999;
    border: 0;
    border-radius: 0;
    background-color: transparent;
    pointer-events: all;
    transition: transform .6s cubic-bezier(.165,.84,.44,1);
  }

  .burger-bar {
    background-color: #00000090;
    position: absolute;
    top: 50%;
    right: 6px;
    left: 6px;
    height: 2px;
    width: auto;
    margin-top: -1px;
    transition: transform .6s cubic-bezier(.165,.84,.44,1),
      opacity .3s cubic-bezier(.165,.84,.44,1),
      background-color .6s cubic-bezier(.165,.84,.44,1);
  }

  .burger-bar--1 {
    -webkit-transform: translateY(-6px);
    transform: translateY(-6px);
  }

  .burger-bar--2 {
    transform-origin: 100% 50%;
    transform: scaleX(.8);
  }

  .burger-button:hover .burger-bar--2 {
    transform: scaleX(1);
  }

  .no-touchevents .burger-bar--2:hover {
    transform: scaleX(1);
  }

  .burger-bar--3 {
    transform: translateY(6px);
  }

  #burger.active .burger-button {
    transform: rotate(-180deg);
  }

  #burger.active .burger-bar--1 {
    transform: rotate(45deg)
  }

  #burger.active .burger-bar--2 {
    opacity: 0;
  }

  #burger.active .burger-bar--3 {
    transform: rotate(-45deg)
  }

  #burger {
    display: none;
  }

  @media screen and (max-width: 600px) {
    #burger {
      display: block;
      position: fixed;
      z-index: 33;
      top: 0.9rem;
      left: 0.9rem;
    }
  }

  .load-img-wrapper {
    display: flex;
    justify-content: center;
    height: 17rem;
    width: 100%;
  }

  .no-data {
    font-size: 0.9rem;
    color: grey;
    padding: 0.1rem 0.5rem;
  }

  .empty-page {
    width: 100%;
    height: 10rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .no-cards {
    color: #00000050;
    font-family: 'Roboto', sans-serif;
    font-size: 1.1rem;
  }
</style>
