<template>
  <div class="user-mini-card">
    <v-layout row wrap class="card-layout">
      <v-flex xs3 class="avatar-wrapper">
        <router-link class="avatar" :to="{name: 'page', params: {page: info.page_id}}">
          <v-avatar color="grey lighten-1" size="37">
            <span v-if="!info.avatar" class="white--text">{{info.username | first}}</span>
            <img v-if="info.avatar" contain :src="info.avatar" style="cursor: pointer">
          </v-avatar>
        </router-link>
      </v-flex>
      <v-flex xs9 class="text-wrapper">
        <router-link class="username" :to="{name: 'page', params: {page: info.page_id}}">
          <span>{{info.username}}</span>
        </router-link>
        <span class="subscrubers">Подписчиков: {{info.follower_count}}</span>
      </v-flex>
      <v-hover v-slot:default="{ hover }" v-if="homePageId !== info.page_id && homePageId">
        <v-icon
          class="follow-icon"
          :title="info.followed ? 'Отписаться' : 'Следить'"
          :color="hover ? '#4D9C6B' : 'grey'"
          @click="follow"
          small>
          {{ info.followed ? 'mdi-eye' : 'mdi-eye-outline'}}
        </v-icon>
      </v-hover>
    </v-layout>
    <v-snackbar
      v-model="snackbar.on"
      bottom
      :color="snackbar.color"
      :timeout="1000"
    >
      {{ snackbar.text }}
      <v-btn
        dark
        text
        @click="snackbar.on = false"
      >
        Закрыть
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlFollow = '/api/v1/follow/'

  export default {
    name: 'UserMiniCard',
    props: ['info', 'homePageId'],
    data () {
      return {
        snackbar: {
          on: false,
          color: '',
          text: ''
        }
      }
    },
    methods: {
      follow () {
        axios.post(urlFollow, {
          command: this.info.followed ? 'unfollow' : 'follow',
          page_id: this.info.page_id
        })
          .then(response => {
            let data = response.data
            this.info.followed = data.follow === 1
            this.snackbar = {
              on: true,
              color: 'success',
              text: 'Все получилось!'
            }
          })
          .catch(error => {
            console.log(error)
            this.snackbar = {
              on: true,
              color: 'error',
              text: 'Что-то пошло не так!'
            }
          })
      }
    }
  }
</script>

<style scoped>
  .user-mini-card {
    width: 100%;
  }

  .card-layout {
    position: relative;
  }

  .avatar-wrapper {
    display: flex;
    justify-content: center;
  }

  .avatar {
    margin: auto;
  }

  .text-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 0.1rem;
  }

  a.username {
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    padding-right: 1.3rem;
    text-align: left;
  }

  .subscrubers {
    font-size: 0.7rem;
    font-family: 'Roboto', sans-serif;
    color: #a7a7a7;
    text-align: left;
  }

  .follow-icon {
    position: absolute;
    margin: 0;
    top: 0.3rem;
    right: 0.1rem;
    cursor: pointer;
    display: none !important;
  }

  .user-mini-card:hover .follow-icon {
    display: block !important;
  }

  .close-dialog {
    cursor: pointer;
    position: absolute;
    right: 1rem;
    top: 1rem;
  }

  div .v-dialog {
    z-index: 999;
  }

  .avatar-card {
    padding: 0.3rem;
  }
</style>
