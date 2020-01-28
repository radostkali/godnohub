<template>
  <div>
    <header
      class="navbar"
      :class="{ 'navbar--hidden': !showNavbar }">
      <div class="nav-wrapper">
        <div class="logo-wrapper" v-if="!hideOptions">
          <router-link :to="(isAuth) ? {name: 'page', params: {page: homePageId}} : {name: 'main'}">
            <div class="logo">
              <v-img contain src="/static/img/logo.png" height="1.3rem" width="10rem"></v-img>
            </div>
          </router-link>
        </div>
        <v-row align="center">
          <div class="nav-option" v-if="!hideOptions">
            <router-link :to="{name: 'news'}" v-if="isAuth">
              <v-btn text small color="grey darken-2" title="Новое в подписках">
                Новое <span class="news-count" v-if="newsCount">+{{newsCount}}</span>
              </v-btn>
            </router-link>
          </div>
          <div class="nav-option" v-if="!hideOptions">
            <router-link :to="{name: 'later'}" v-if="isAuth">
              <v-btn text small color="grey darken-2" title="Отложенные карточки">
                Отложенное
              </v-btn>
            </router-link>
          </div>
          <div class="nav-option" v-if="!hideOptions">
            <followings v-if="isAuth">
              Подписки
            </followings>
          </div>
          <v-spacer></v-spacer>
          <div class="nav-option">
            <login v-if="!isAuth"></login>
          </div>
          <div class="nav-option" v-if="!hideOptions">
            <create-card v-if="isAuth" :editing="false">
              <v-hover v-slot:default="{ hover }">
                <v-btn :color="hover ? 'green' : 'green lighten-3'" text small title="Добавить карточку">
                  <v-icon>mdi-card-plus</v-icon> Добавить
                </v-btn>
              </v-hover>
            </create-card>
          </div>
          <div class="nav-option" style="z-index: 34">
            <v-menu open-on-hover offset-y bottom v-if="isAuth">
              <template v-slot:activator="{ on }">
                <v-avatar color="grey lighten-1" size="28" v-on="on">
                  <span v-if="!avatarUrl" class="white--text">{{username | first}}</span>
                  <img v-if="avatarUrl" contain :src="avatarUrl">
                </v-avatar>
              </template>

              <v-list>
                <v-list-item>
                  <router-link :to="{name: 'page', params: {page: homePageId}}">
                    <v-btn text small color="grey darken-1" title="Моя коллекция">
                      <v-icon>mdi-home</v-icon> Коллекция
                    </v-btn>
                  </router-link>
                </v-list-item>
                <v-list-item v-if="hideOptions">
                  <router-link :to="{name: 'news'}" v-if="isAuth">
                    <v-btn text small color="grey darken-2" title="Новое в подписках">
                      <v-icon>mdi-newspaper-variant-multiple-outline</v-icon>
                      Новое
                      <span class="news-count" v-if="newsCount">+{{newsCount}}</span>
                    </v-btn>
                  </router-link>
                </v-list-item>
                <v-list-item v-if="hideOptions">
                  <router-link :to="{name: 'later'}" v-if="isAuth">
                    <v-btn text small color="grey darken-2" title="Отложенные карточки">
                      <v-icon>mdi-folder-clock-outline</v-icon>
                      Отложенное
                    </v-btn>
                  </router-link>
                </v-list-item>
                <v-list-item v-if="hideOptions">
                  <followings v-if="isAuth" :inMenu="hideOptions">
                    <v-icon>mdi-account-multiple</v-icon> Подписки
                  </followings>
                </v-list-item>
                <v-list-item v-if="hideOptions">
                  <create-card v-if="isAuth" :editing="false">
                    <v-hover v-slot:default="{ hover }">
                      <v-btn :color="hover ? 'green' : 'green lighten-3'" text small title="Добавить карточку">
                        <v-icon>mdi-card-plus</v-icon> Добавить
                      </v-btn>
                    </v-hover>
                  </create-card>
                </v-list-item>
                <v-list-item>
                  <settings>
                    <v-btn text small color="grey darken-1"  title="Настройки">
                      <v-icon>mdi-settings-outline</v-icon> Настройки
                    </v-btn>
                  </settings>
                </v-list-item>
                <v-list-item>
                  <logout>
                    <v-btn text small color="grey darken-1"  title="Выйти">
                      <v-icon>mdi-exit-run</v-icon> Выйти
                    </v-btn>
                  </logout>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </v-row>
      </div>
    </header>
  </div>

</template>

<script>
  import axios from 'axios'
  import Login from './Login'
  import Logout from './Logout'
  import Followings from './Followings'
  import { mapGetters } from 'vuex'

  const urlNewsInfo = '/api/v1/news_info/'

  export default {
    name: 'Header',
    components: {
      Login,
      Logout,
      Followings
    },
    data () {
      return {
        showNavbar: true,
        lastScrollPosition: 0,
        hideOptions: false,
        newsCount: 0
      }
    },
    computed: {
      ...mapGetters({
        isAuth: 'IS_AUTH',
        homePageId: 'HOME_PAGE',
        username: 'USERNAME',
        avatarUrl: 'AVATAR'
      })
    },
    mounted () {
      window.addEventListener('scroll', this.onScroll)
      window.addEventListener('resize', this.onResize)
    },
    beforeDestroy () {
      window.removeEventListener('scroll', this.onScroll)
      window.removeEventListener('resize', this.onResize)
    },
    created () {
      this.onResize()
    },
    methods: {
      onResize () {
        this.hideOptions = window.innerWidth < 777
      },
      onScroll () {
        const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop
        if (currentScrollPosition < 0) {
          return
        }
        if (Math.abs(currentScrollPosition - this.lastScrollPosition) < 60) {
          return
        }
        this.showNavbar = currentScrollPosition < this.lastScrollPosition
        this.lastScrollPosition = currentScrollPosition
      },
      getNewsCount () {
        let r = new Promise((resolve, reject) => {
          axios.get(urlNewsInfo, {
            params: {
              news_count: 1
            }
          })
            .then(response => {
              if (response.status === 200) {
                this.newsCount = response.data.news_count
                resolve(true)
              } else {
                reject(new Error('Getting news count error'))
              }
            })
            .catch(error => {
              console.log(error)
              reject(new Error('Getting news count error'))
            })
        })
        r.then(
          (result) => {
          },
          (error) => {
            console.log(error)
          }
        )
      }
    },
    watch: {
      $route (to, from) {
        this.getNewsCount()
      },
      'isAuth' () {
        this.getNewsCount()
      }
    }
  }
</script>

<style>
  .navbar {
    height: 3rem;
    width: 100%;
    background: #fafafa;
    position: fixed;
    transform: translate3d(0, 0, 0);
    transition: 0.1s all ease-out;
    z-index: 10;
  }

  .nav-option {
    margin-left: 0.3rem;
  }

  .navbar.navbar--hidden {
    transform: translate3d(0, -100%, 0);
  }

  .v-list .v-btn__content {
    text-decoration: none;
  }

  .v-icon {
    margin-right: 0.3rem;
  }

  .v-list-item {
    padding: 0 4px;
  }

  .nav-wrapper {
    float: right;
    padding-right: 3rem !important;
    padding: 12px;
    width: 100%;
    display: flex;
  }

  .logo-wrapper {
    width: 20%;
  }

  @media screen and (max-width: 1000px) {
    .logo-wrapper {
      width: 40%;
    }
  }

  .nav-option:first-child {
    margin-left: 1rem;
  }

  .news-count {
    margin-left: 0.3rem;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    font-size: 0.8rem;
    color: #aaa;
    background: #eee;
    border-radius: 0.3rem;
    padding: 0.1rem 0.3rem;
  }
</style>
