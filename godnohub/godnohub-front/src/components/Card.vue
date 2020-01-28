<template>
  <div class="card">
    <v-hover v-slot:default="{ hover }" v-if="display === 'full'">
    <v-card
      tile
      outlined
      :class="[newCard ? 'card-new' : 'card-old', 'card-class']">
      <div class="color-line" :style="'background:' + info.color"></div>
      <div class="color-line-back" :style="'background:' + info.color"></div>
      <v-layout row wrap>
        <v-flex xs12 sm5 class="image-wrapper">
          <v-img
            :src="info.imgur_url || 'https://i.imgur.com/ZRguE01.png'"
            @error="imageLoadError"
            aspect-ratio="1"
            :class="(later) ? 'image-1' : 'image-' + info.rating.rate"
            contain
          >
            <template v-slot:placeholder>
              <div class="load-img-wrapper">
                <v-progress-circular
                  indeterminate
                  :color="info.color + ' lighten-5'"
                  style="margin: auto"></v-progress-circular>
              </div>
            </template>
          </v-img>
        </v-flex>
        <v-flex xs12 sm7>
          <div class="text-wrapper">
            <v-layout column justify-start fill-height>
              <span v-if="news" class="type">{{ info.type.name }}</span>
              <span v-if="later" class="type">{{ info.type }}</span>
              <v-icon
                :style="hover ? 'display: block' : 'display: none'"
                class="delete-icon"
                title="Удалить карточку"
                color="grey"
                v-if="is_home && !editing && is_auth"
                @click="deleteDialog = true">
                mdi-delete
              </v-icon>
              <create-card v-if="is_home && !editing && is_auth" :cardInfo="info" :editing="true">
                <v-icon
                  :style="hover ? 'display: block' : 'display: none'"
                  class="edit-icon"
                  title="Редактировать"
                  color="grey">
                  mdi-pencil
                </v-icon>
              </create-card>
              <to-post-storage
                class="post-storage-icon"
                :style="hover ? 'display: block' : 'display: none'"
                v-if="!is_home && !editing && is_auth && !later"
                :cardInfo="info">
              </to-post-storage>
              <v-icon
                :style="hover ? 'display: block' : 'display: none'"
                class="post-storage-icon"
                title="Удалить карточку"
                color="grey"
                v-if="later"
                @click="deleteDialog = true">
                mdi-delete
              </v-icon>
              <create-card v-if="!is_home && !editing && is_auth" :cardInfo="info" :editing="true" :later="later">
                <v-icon
                  :style="hover ? 'display: block' : 'display: none'"
                  class="repost-icon"
                  title="Добавить себе"
                  color="grey">
                  mdi-plus-box
                </v-icon>
              </create-card>
              <h1
                :style="(info.title.length > 44) ? 'font-size: 1.2rem' : ''">
                {{ info.title }}
              </h1>
              <p v-if="!later" :rating="info.rating.rate" class="rating">{{ info.rating.name }}</p>
              <v-spacer></v-spacer>
              <div class="tags-wrapper news-tags" v-if="news">
                <div
                  class="tag owner">
                  <router-link :to="{name: 'page', params: {page: owner.page_id}}">
                    <v-avatar style="opacity: 1" color="grey lighten-1" size="17">
                      <span v-if="owner.avatar === null" class="white--text">{{owner.username | first}}</span>
                      <img v-if="owner.avatar" contain :src="owner.avatar">
                    </v-avatar>
                    <span class="owner-name" title="Автор карточки">{{ owner.username }}</span>
                  </router-link>
                </div>
              </div>
              <div class="tags-wrapper">
                <div
                  class="tag"
                  v-for="item in info.tags"
                  :key="item.id"
                  :class="{activetag: tagsFiltered.includes(item.id)}">
                  {{ (later) ? item : item.name }}
                </div>
              </div>
            </v-layout>
          </div>
        </v-flex>
      </v-layout>
    </v-card>
    </v-hover>

    <v-hover v-slot:default="{ hover }" v-if="display === 'list'">
    <v-card
      tile
      outlined
      :class="[newCard ? 'card-new' : 'card-old', 'card-class']">
      <div class="mini-color-line" :style="'background:' + info.color"></div>
      <div class="mini-color-line-back" :style="'background:' + info.color"></div>
      <v-layout row wrap>
        <v-flex xs3 class="image-wrapper image-wrapper-mini">
          <v-img
            :src="info.imgur_url || 'https://i.imgur.com/ZRguE01.png'"
            @error="imageLoadError"
            aspect-ratio="1"
            class="image-mini"
            contain
          >
            <template v-slot:placeholder>
              <div class="load-img-wrapper">
                <v-progress-circular
                  indeterminate
                  :color="info.color + ' lighten-5'"
                  style="margin: auto"></v-progress-circular>
              </div>
            </template>
          </v-img>
        </v-flex>
        <v-flex xs9>
          <div class="text-wrapper mini-text-wrapper">
            <v-layout column justify-start fill-height>
              <v-icon
                small
                :style="hover ? 'display: block' : 'display: none'"
                class="delete-icon mini-icon-1"
                title="Удалить карточку"
                color="grey"
                v-if="is_home && !editing && is_auth"
                @click="deleteDialog = true">
                mdi-delete
              </v-icon>
              <create-card v-if="is_home && !editing && is_auth" :cardInfo="info" :editing="true">
                <v-icon
                  small
                  :style="hover ? 'display: block' : 'display: none'"
                  class="edit-icon mini-icon-2"
                  title="Редактировать"
                  color="grey">
                  mdi-pencil
                </v-icon>
              </create-card>
              <to-post-storage
                class="post-storage-icon mini-icon-2"
                :style="hover ? 'display: block' : 'display: none'"
                v-if="!is_home && !editing && is_auth && !later"
                :cardInfo="info"
                :small="true">
              </to-post-storage>
              <v-icon
                :style="hover ? 'display: block' : 'display: none'"
                class="post-storage-icon mini-icon-2"
                title="Удалить карточку"
                color="grey"
                v-if="later"
                @click="deleteDialog = true">
                mdi-delete
              </v-icon>
              <create-card v-if="!is_home && !editing && is_auth" :cardInfo="info" :editing="true" :later="later">
                <v-icon
                  small
                  :style="hover ? 'display: block' : 'display: none'"
                  class="repost-icon mini-icon-1"
                  title="Добавить себе"
                  color="grey">
                  mdi-plus-box
                </v-icon>
              </create-card>
              <h1
                class="mini-h1"
                :style="(info.title.length > 44) ? 'font-size: 1rem' : 'font-size: 1.2rem'">
                {{ info.title }}
                <span v-if="news" class="type mini-type">{{ info.type.name }}</span>
                <span v-if="later" class="type mini-type">{{ info.type }}</span>
              </h1>
              <p v-if="!later" :rating="info.rating.rate" class="rating mini-rating">{{ info.rating.name }}</p>
              <v-spacer></v-spacer>
              <div class="tags-wrapper news-tags mini-tags-wrapper" v-if="news">
                <div
                  class="tag owner">
                  <router-link :to="{name: 'page', params: {page: owner.page_id}}">
                    <v-avatar style="opacity: 1" color="grey lighten-1" size="17">
                      <span v-if="owner.avatar === null" class="white--text">{{owner.username | first}}</span>
                      <img v-if="owner.avatar" contain :src="owner.avatar">
                    </v-avatar>
                    <span class="owner-name" title="Автор карточки">{{ owner.username }}</span>
                  </router-link>
                </div>
              </div>
              <div class="tags-wrapper mini-tags-wrapper">
                <div
                  class="tag"
                  v-for="item in info.tags"
                  :key="item.id"
                  :class="{activetag: tagsFiltered.includes(item.id)}">
                  {{ (later) ? item : item.name }}
                </div>
              </div>
            </v-layout>
          </div>
        </v-flex>
      </v-layout>
    </v-card>
    </v-hover>

    <v-dialog
      v-model="deleteDialog"
    >
      <v-card class="delete-card">
        <v-icon small class="close-dialog" @click="deleteDialog = false">mdi-close</v-icon>
        <h1>Удалить {{info.title}}?</h1>
        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn small color="error" @click="deleteEntry">
              <v-progress-circular
                v-if="loading"
                indeterminate
                color="white darken-1"
                class="mr-1"
                size="18"
                width="1"
              ></v-progress-circular>
              <v-icon left v-if="!loading && success == null">mdi-delete</v-icon>
              <v-icon left v-if="!loading && success == true">mdi-check</v-icon>
              <v-icon left v-if="!loading && success == false">mdi-alert-circle-outline</v-icon>
              Удалить
            </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'
  import { mapGetters } from 'vuex'

  const urlDelete = '/api/v1/card/delete/'

  export default {
    name: 'Card',
    props: ['info', 'tagsFiltered', 'editing', 'news', 'newCard', 'owner', 'display', 'later'],
    data () {
      return {
        is_home: false,
        is_auth: false,
        deleteDialog: false,
        editDialog: false,
        loading: false,
        success: null
      }
    },
    methods: {
      imageLoadError () {
        this.info.imgur_url = 'https://i.imgur.com/ZRguE01.png'
      },
      deleteEntry () {
        if (this.info.id !== 0) {
          this.loading = true
          let r = new Promise((resolve, reject) => {
            axios.post(urlDelete, {
              id: this.info.id,
              post_storage: this.later === true
            })
              .then(response => {
                if (response.status === 200) {
                  resolve(true)
                } else {
                  reject(new Error('Deleting card error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Deleting card error'))
              })
          })
          r.then(
            (result) => {
              this.loading = false
              this.success = true
              let self = this
              setTimeout(function () {
                self.$router.go()
              }, 300)
            },
            (error) => {
              console.log(error)
              this.loading = false
              this.success = false
            }
          )
        }
      }
    },
    computed: {
      ...mapGetters({
        isAuth: 'IS_AUTH',
        homePageId: 'HOME_PAGE'
      })
    },
    watch: {
      'homePageId': function (val) {
        if (val === this.$route.params.page && this.$route.params.page) {
          this.is_home = true
        }
      }
    },
    created () {
      if (this.homePageId === this.$route.params.page && this.$route.params.page) {
        this.is_home = true
      }
      this.is_auth = this.isAuth
    }
  }
</script>

<style scoped>
  .card {
    font-family: 'Montserrat', sans-serif;
    position: relative;
    height: 100%;
  }

  .card-class {
    height: 100%;
    display: flex;
    justify-content: center;
    flex-direction: column;
  }

  .card-new {
    background-color: #f7fff9;
    border-bottom: 1px solid #D7EADC !important;
    border-right: 1px solid #D7EADC !important;
    border-left: 1px solid #D7EADC !important;
  }

  .card-old {
    background-color: #ffffff;
  }

  .color-line {
    width: 100%;
    height: 0.3rem;
    opacity: 0.3;
    position: absolute;
    top: 0;
    z-index: 3;
  }

  .layout {
    z-index: 5;
  }

  .color-line-back {
    width: 100%;
    height: 0.3rem;
    opacity: 0.05;
    position: absolute;
    top: 0;
    transition: 0.3s all ease-out;
    z-index: 4;
  }

  .card:hover .color-line-back {
    height: 100%;
  }

  .mini-color-line {
    width: 0.3rem;
    height: 100%;
    opacity: 0.3;
    position: absolute;
    left: 0;
    z-index: 3;
  }

  .mini-color-line-back {
    width: 0.3rem;
    height: 100%;
    opacity: 0.05;
    position: absolute;
    left: 0;
    transition: 0.3s all ease-out;
  }

  .card:hover .mini-color-line-back {
    width: 100%;
  }

  div.card .v-card {
    overflow: hidden;
    border: none;
    padding-top: 0.3rem;
    z-index: 4;
  }

  .delete-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    cursor: pointer;
  }

  .edit-icon {
    position: absolute;
    top: 1rem;
    right: 3rem;
    cursor: pointer;
  }

  .repost-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    cursor: pointer;
  }

  .post-storage-icon {
    position: absolute;
    top: 1rem;
    right: 3rem;
    cursor: pointer;
  }

  .mini-icon-1 {
    right: 0.5rem;
  }

  .mini-icon-2 {
    line-height: 1;
    right: 1.8rem;
  }

  .image-1 {
    height: 11rem;
  }

  .image-2 {
    height: 13rem;
  }

  .image-3 {
    height: 15rem;
  }

  .image-6 {
    height: 9rem;
  }

  .image-9 {
    height: 12rem;
  }

  .image-mini {
    margin-left: 0.5rem;
    height: 5rem;
  }

  .image-wrapper {
    margin: 0.5rem 0;
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding-left: 1rem;
  }

  @media screen and (max-width: 600px) {
    .image-wrapper {
      padding-left: 0;
    }

    .image-wrapper-mini {
      padding-left: 1rem;
    }

    .image-mini {
      height: 3rem;
    }
  }

  .load-img-wrapper {
    display: flex;
    justify-content: center;
    height: 17rem;
    width: 100%;
  }

  .text-wrapper {
    width: 90%;
    height: 100%;
    margin-left: 5%;
    margin-right: 5%;
    margin-top: 0.7rem;
    text-align: left;
    color: #000000;
  }

  .mini-text-wrapper {
    margin-top: 0.3rem;
  }

  .text-wrapper h1 {
    max-height: 7rem;
    font-size: 1.4rem;
    padding-right: 5rem;
  }

  .text-wrapper h1.mini-h1 {
    padding-right: 3rem !important;
  }

  h1 {
    font-family: 'Oswald', sans-serif;
    font-weight: 300;
    margin-top: 0
  }

  span, p {
    font-size: 0.8rem;
    font-weight: 400;
  }

  .mini-type {
    font-size: 0.7rem;
    font-weight: 200;
  }

  span.type {
    color: #9b9b9b;
    transition: 0.3s all ease-out;
  }

  .card:hover span.type {
    color: #696969;
  }

  p.rating {
    margin-top: 1.3rem;
  }

  p.mini-rating {
    margin: 0.3rem 0;
  }

  .tags-wrapper {
    padding-bottom: 1.9rem;
  }

  .tags-wrapper.mini-tags-wrapper {
    padding-bottom: 1rem;
  }

  .news-tags {
    padding-bottom: .5rem;
  }

  .news-tags.mini-tags-wrapper {
    padding-bottom: .3rem;
  }

  .tag {
    font-size: 0.8rem;
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 0.3rem;
    background: #e2e2e2;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    opacity: 0.5;
    transition: 0.3s all ease-out;
  }

  .mini-tags-wrapper .tag {
    font-size: 0.8rem;
    padding: 0.07rem 0.3rem;
  }

  .card:hover .tag {
    opacity: 0.7;
  }

  .tag.activetag {
    background: #c5c5c5;
    color: #000000;
    font-weight: 600;
  }

  @media screen and (max-width: 600px) {
    .text-wrapper {
      margin-bottom: 3rem;
      text-align: center;
    }

    .text-wrapper h1 {
      padding-right: 0;
    }
  }

  .delete-card h1 {
    padding: 1rem 3rem;
    font-size: 1.3rem;
  }

  .close-dialog {
    cursor: pointer;
    position: absolute;
    right: 1rem;
    top: 1rem;
  }

  .tag.owner {
    opacity: 1 !important;
    background: #c5c5c55e;
    font-weight: 600;
  }
  .owner-name {
    color: #00000083;
  }

</style>
