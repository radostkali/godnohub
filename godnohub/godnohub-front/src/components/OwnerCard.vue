<template>
  <div class="owner-card-wrapper">
    <div :class="['owner-card', (responsive === 'mobile') ? 'mobile-card' : (responsive === 'main-page') ? 'main-page-card' : 'desktop-card']">
      <v-layout row>
        <v-flex xs3 class="image-wrapper">
          <v-avatar color="grey lighten-1" size="73">
            <span v-if="!owner.avatar" class="white--text">{{owner.username | first}}</span>
            <img v-if="owner.avatar" contain :src="owner.avatar" style="cursor: pointer" @click="avatarDialog = true">
          </v-avatar>
        </v-flex>
        <v-flex xs9 class="text-wrapper">
          <h1>{{owner.username}}</h1>
        </v-flex>
        <v-hover v-slot:default="{ hover }" v-if="homePageId !== pageId && homePageId">
          <v-icon
            class="follow-icon"
            :title="owner.followed ? 'Отписаться' : 'Подписаться'"
            :color="hover ? '#4D9C6B' : 'grey'"
            @click="follow">
            {{ owner.followed ? 'mdi-eye' : 'mdi-eye-plus-outline'}}
          </v-icon>
        </v-hover>
      </v-layout>
      <div class="info-panel">
        <div class="info-block" v-if="owner.cardCount">
          <span class="info-count">{{owner.cardCount}}</span>
          <p class="info-title">
            карточек
          </p>
        </div>
        <div class="info-block" v-if="owner.followers">
          <span class="info-count">{{owner.followers.length}}</span>
          <p class="info-title info-link" @click="openDialog('followers')">
            подписчики
          </p>
        </div>
        <div class="info-block" v-if="owner.followings">
          <span class="info-count">{{owner.followings.length}}</span>
          <p class="info-title info-link" @click="openDialog('followings')">
            подписан
          </p>
        </div>
      </div>
    </div>
    <div class="check-page-btn">
      <router-link :to="{name: 'page', params: {page: pageId}}">
        <v-btn
          v-if="responsive === 'main-page'"
          text
          color="#4D9C6B"
          style="font-weight: 400"
          small
          >Смотреть</v-btn>
      </router-link>
    </div>
    <v-dialog
      width="unset"
      v-model="avatarDialog">
      <v-card>
        <v-icon small class="close-dialog" @click="avatarDialog = false">mdi-close</v-icon>
        <div class="avatar-card">
          <img v-if="owner.avatar" contain :src="owner.avatar">
        </div>
      </v-card>
    </v-dialog>
    <v-dialog
      width="unset"
      v-model="followersDialog">
      <v-card>
        <v-icon small class="close-dialog" @click="followersDialog = false">mdi-close</v-icon>
        <div class="followers-card">
          <h1 class="headline">{{(dialogBlock == 'followers') ? 'Подписчики' : 'Подписки'}} {{owner.username}}</h1>
          <div class="followers-card-wrapper" v-if="dialogBlock == 'followers'">
            <user-mini-card
              v-for="(item, index) in owner.followers"
              :info="item"
              :homePageId="homePageId"
              :key="index"
              style="margin-bottom: 0.7rem;">
            </user-mini-card>
          </div>
          <div class="followers-card-wrapper" v-if="dialogBlock == 'followings'">
            <user-mini-card
              v-for="(item, index) in owner.followings"
              :info="item"
              :homePageId="homePageId"
              :key="index"
              style="margin-bottom: 0.7rem;">
            </user-mini-card>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>

</template>

<script>
  import axios from 'axios'

  const urlFollow = '/api/v1/follow/'

  export default {
    name: 'OnwerCard',
    props: ['pageId', 'homePageId', 'responsive', 'owner'],
    data () {
      return {
        followersDialog: false,
        dialogBlock: null,
        avatarDialog: false
      }
    },
    methods: {
      openDialog (block) {
        this.followersDialog = true
        this.dialogBlock = block
      },
      follow () {
        axios.post(urlFollow, {
          command: this.owner.followed ? 'unfollow' : 'follow',
          page_id: this.pageId
        })
          .then(response => {
            let data = response.data
            this.owner.followed = data.follow === 1
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    watch: {
      'pageId': function () {
        this.followersDialog = false
      }
    }
  }
</script>

<style scoped>
  .owner-card-wrapper {
    width: 100%;
    padding: 0.5rem;
    padding-top: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
  }

  .owner-card {
    width: 100%;
    padding: 0.3rem 1rem 1.3rem 1rem;
    position: relative;
    max-width: 21rem;
    margin: auto;
  }

  .mobile-card {
    margin-bottom: 0.5rem;
    border-radius: 0.5rem;
    background: #ffffff;
  }

  .main-page-card {
    border-radius: 0.5rem;
    border: 1px solid #00000010;
  }

  .desktop-card::before {
    content: '';
    height: 1px;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: #ececec;
  }

  .image-wrapper {
    position: absolute;
    top: 0;
    transform: translate(0, -50%);
  }

  .text-wrapper {
    padding-left: 5rem;
  }

  h1 {
    font-family: 'Oswald', sans-serif;
    font-weight: 500;
    font-size: 1.3rem;
    text-align: left;
  }

  p {
    font-family: 'Roboto', sans-serif;
    font-size: 0.8rem;
    text-align: left;
  }

  .follow-icon {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    cursor: pointer;
  }

  .check-page-btn {
    margin-top: 0.5rem;
    margin-bottom: 1rem;
  }

  .info-panel {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 1rem;
  }

  .info-block {
    padding: 0 0.5rem;
  }

  .info-title {
    color: #000000a9;
    margin: 0;
  }

  .info-link {
    text-decoration: underline;
    text-decoration-style: dashed;
    text-decoration-color: #00000050;
    cursor: pointer;
  }

  .info-count {
    font-family: 'Roboto', sans-serif;
    font-size: 1.5rem;
    font-weight: 300;
  }

  .follow-wrapper {
    margin: 0 0.3rem;
  }

  @media screen and (max-width: 1000px) {
    .followers-card {
      min-width: 0;
    }
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

  .headline {
    font-family: 'Roboto', sans-serif;
    font-size: 1.3rem !important;
    margin-bottom: 1.3rem;
  }

  .followers-card {
    padding: 1rem 3rem;
  }

  .followers-card-wrapper {
    max-width: 15rem;
  }

  .followers-card-user {
    margin-bottom: 1rem;
    display: flex;
  }

  .avatar-card {
    padding: 0.3rem;
  }
</style>
