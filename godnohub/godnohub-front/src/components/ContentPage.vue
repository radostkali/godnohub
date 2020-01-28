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
              :items="tags"
              v-model="tagsPicked"
              item-text="name"
              item-value="id"
              label="Тэги"
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
              :items="rates"
              v-model="ratesPicked"
              item-text="name"
              item-value="rate"
              label="Тонкая настройка"
              attach
              chips
              deletable-chips
              dense
              multiple
            ></v-select>
          </div>
          <div class="filter-group">
            <v-btn @click="applyFilters" class="ml-3" outlined color="teal darken-2">
              <v-icon left>mdi-filter-variant</v-icon> Применить
            </v-btn>
          </div>
        </div>
        <v-spacer></v-spacer>
        <owner-card
          class="owner-card"
          :responsive="'desktop'"
          :pageId="routePage"
          :homePageId="homePageId"
          :owner="owner">
        </owner-card>
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
        <owner-card
          class="owner-card-modile"
          :responsive="'mobile'"
          :pageId="routePage"
          :homePageId="homePageId"
          :owner="owner">
        </owner-card>
        <groups-panel
          v-if="!emptyPage"
          :types="types"
          :typePicked="routeGroup"
          :homePageId="homePageId"
          :routePage="routePage"
          v-on:pick-type="pickType"
        ></groups-panel>

        <cards-content
          v-if="!emptyPage"
          :info="info"
          :news="false"
          :tagsFiltered="tagsFiltered"
        ></cards-content>

        <div class="empty-page" v-if="emptyPage">
          <p class="no-cards">
            Пока что здесь нет годноты
          </p>
          <create-card v-if="routePage === homePageId" :editing="false">
            <v-hover v-slot:default="{ hover }">
              <v-btn :color="hover ? 'green' : 'green lighten-1'" outlined title="Добавить карточку">
                Добавить?
              </v-btn>
            </v-hover>
          </create-card>
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
  import OwnerCard from './OwnerCard'
  import GroupsPanel from './GroupsPanel'
  import axios from 'axios'
  import { mapGetters } from 'vuex'

  const urlCards = '/api/v1/cards/'
  const urlGroupEdit = '/api/v1/group_edit/'
  const urlFilters = '/api/v1/filters/'
  const urlOwner = '/api/v1/owner_info/'

  export default {
    name: 'Content',
    vuetify: new Vuetify(),
    components: { OwnerCard, GroupsPanel },
    data () {
      return {
        info: [],
        emptyPage: false,
        next_page: urlCards + '?page=1',
        errored: false,
        isMenuVisible: false,
        owner: {
          username: null,
          avatar: null,
          cardCount: null,
          followed: null,
          followers: null
        },
        types: [],
        tagsPicked: [],
        tags: [],
        tagsFiltered: [],
        ratesPicked: null,
        rates: [],
        infiniteId: 0,
        routePage: this.$route.params.page,
        routeGroup: this.$route.params.group || 0,
        params: {},
        editGroupDialogs: false,
        groupToEdit: null,
        loading: false,
        success: null,
        color: 'primary',
        buttonActive: true
      }
    },
    methods: {
      openEditDialog (group) {
        this.groupToEdit = group
        this.editGroupDialogs = true
      },
      editGroup () {
        this.loading = true
        this.color = 'primary'
        axios.post(urlGroupEdit, {
          id: this.groupToEdit.id,
          name: this.groupToEdit.name
        })
          .then(response => {
            this.loading = false
            this.success = true
            this.color = 'green'
            let self = this
            setTimeout(function () {
              self.$router.go()
            }, 300)
          })
          .catch(error => {
            console.error(error)
            this.loading = false
            this.success = false
            this.color = 'red lighten-1'
          })
      },
      clearAll () {
        this.info = []
        this.next_page = urlCards + '?page=1'
        this.errored = false
        this.isMenuVisible = false
        this.types = []
        this.params = { type_id: this.routeGroup }
        this.clearFilters()
      },
      clearFilters () {
        this.tagsPicked = []
        this.tags = []
        this.tagsFiltered = []
        this.ratesPicked = null
        this.rates = []
      },
      pickType (typeId) {
        this.routeGroup = typeId
        this.clearFilters()
        this.getFilters()
        this.params = {
          type_id: this.routeGroup + '',
          tags: this.tagsPicked + '',
          rating: this.ratesPicked + ''
        }
        this.resetCards()
      },
      applyFilters () {
        if (this.buttonActive) {
          this.buttonActive = false
          this.params = {
            type_id: this.routeGroup + '',
            tags: this.tagsPicked + '',
            rating: this.ratesPicked + ''
          }
          this.tagsFiltered = Array.from(this.tagsPicked)
          this.resetCards()
        }
      },
      resetCards () {
        this.info = []
        this.next_page = urlCards + '?page=1'
        this.infiniteId += 1
      },
      infiniteHandler ($state) {
        this.params['page_id'] = this.routePage
        this.params['type_id'] = this.routeGroup
        axios.get(this.next_page, {
          params: this.params
        })
          .then(response => {
            if (response.data.status !== 'No Cards') {
              this.info = this.info.concat(response.data.results)
              this.next_page = response.data.next
              this.buttonActive = true
              if (this.next_page == null) {
                $state.complete()
              } else {
                $state.loaded()
              }
            } else {
              $state.complete()
              this.emptyPage = true
            }
          })
          .catch(error => {
            console.log(error)
            this.errored = true
          })
      },
      getFilters (backUrl = false) {
        axios.get(urlFilters, {
          params: {
            page_id: this.routePage,
            type_id: this.routeGroup
          }
        })
          .then(response => {
            let data = response.data
            this.types = data.types
            this.tags = data.tags
            this.rates = data.rates
            if (!backUrl) window.history.pushState({}, document.title, `/${this.routePage}/${data.type}`)
            this.routeGroup = data.type
          })
          .catch(error => {
            console.log(error)
          })
      },
      toggle () {
        this.isMenuVisible = !this.isMenuVisible
      },
      getOwnerInfo () {
        axios.get(urlOwner, {
          params: { page_id: this.routePage }
        })
          .then(response => {
            let data = response.data
            this.owner = {
              username: data.username,
              avatar: data.avatar,
              cardCount: data.card_count,
              followed: data.follow === 1,
              followers: data.followers,
              followings: data.followings
            }
          })
          .catch(error => {
            console.log(error)
          })
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
      'isAuth': function () {
        this.resetCards()
      },
      'displayChange': function () {
        this.infiniteId += 1
      }
    },
    beforeRouteUpdate (to, from, next) {
      this.routePage = to.params.page
      this.routeGroup = to.params.group || 0
      this.clearAll()
      this.getFilters(true)
      this.resetCards()
      this.getOwnerInfo()
      next()
    },
    created () {
      this.getFilters(true)
      this.getOwnerInfo()
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
