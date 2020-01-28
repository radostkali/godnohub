<template>
  <div>
    <v-btn text small color="grey darken-2" @click="openFollowingsDialog">
      <slot></slot>
    </v-btn>
    <v-dialog
      width="unset"
      v-model="followingsDialog">
      <v-card>
        <v-icon small class="close-dialog" @click="followingsDialog = false">mdi-close</v-icon>
        <div class="followers-card">
          <h1 class="headline">Мои подписки</h1>
          <v-list>
            <div class="followers-card-wrapper" v-if="followings.length !== 0">
              <v-list-item class="list-item" v-for="(item, index) in followings" :key="index">
                <user-mini-card
                  :info="item"
                  :homePageId="$store.getters.HOME_PAGE">
                </user-mini-card>
              </v-list-item>
            </div>
            <div v-else class="no-data-block">
              <span class="no-data">Пока что здесь пусто</span>
            </div>
          </v-list>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlFollower = '/api/v1/auth/info'

  export default {
    name: 'Followings',
    props: ['inMenu'],
    data () {
      return {
        followings: [],
        followingsDialog: false
      }
    },
    methods: {
      openFollowingsDialog () {
        setTimeout(() => { this.followingsDialog = true })
      },
      getInfo () {
        axios.get(urlFollower, {
          params: { get_followings: true }
        })
          .then(response => {
            let data = response.data
            this.followings = data.followings
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    watch: {
      '$route' () {
        this.followingsDialog = false
      }
    },
    created () {
      this.getInfo()
    },
    filters: {
      first: function (value) {
        if (!value) return ''
        return value.charAt(0).toUpperCase()
      }
    }
  }
</script>

<style scoped>
  .followers-card-wrapper {
    max-width: 15rem;
    min-width: 13rem;
  }

  .followers-card {
    padding: 1rem 3rem;
  }

  .list-item {
    margin-left: 1rem;
    max-width: 13rem;
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
    text-align: center;
  }

  .no-data-block {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .no-data {
    font-size: 0.9rem;
    color: grey;
    padding: 0.1rem 0.5rem;
    margin-bottom: 1rem;
  }

  .random-card-wrapper {
    position: relative;
    font-family: 'Roboto', sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
</style>
