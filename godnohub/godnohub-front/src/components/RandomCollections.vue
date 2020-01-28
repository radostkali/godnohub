<template>
  <div>
    <transition name="change-card" mode="out-in">
      <v-layout wrap v-if="collections" :key="transitionKey">
        <v-flex xs12 md6 lg4 v-for="(collection, i) in collections" :key="i">
          <owner-card
            :responsive="'main-page'"
            :pageId="collection.page_id"
            :homePageId="null"
            :owner="collection">
          </owner-card>
        </v-flex>
      </v-layout>
    </transition>
    <div class="more-collections">
      <v-btn small outlined color="grey" @click="getCollections">
        <v-progress-circular
          v-if="loading"
          indeterminate
          color="grey darken-1"
          class="mr-1"
          size="18"
          width="1"
        ></v-progress-circular>
        Еще
      </v-btn>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import OwnerCard from './OwnerCard'

  const urlRandColl = '/api/v1/random_collections/'

  export default {
    name: 'RandomCollections',
    components: { OwnerCard },
    data () {
      return {
        collections: null,
        transitionKey: 0,
        loading: false
      }
    },
    methods: {
      getCollections () {
        this.loading = true
        let r = new Promise((resolve, reject) => {
          axios.get(urlRandColl)
            .then(response => {
              this.collections = response.data.collections
              this.transitionKey += 1
              resolve(true)
            })
            .catch(error => {
              console.log(error)
              reject(new Error('Registration error'))
            })
        })
        r.then(
          (result) => {
            this.loading = false
          },
          (error) => {
            console.log(error)
            this.loading = false
          }
        )
      }
    },
    created () {
      this.getCollections()
    }
  }
</script>

<style scoped>
  .more-collections {
    margin-top: 3rem;
    margin-bottom: 3rem;
    display: flex;
    justify-content: center;
  }

  /* Animation */
  .change-card-enter {
    transform: translate(-20rem, 0);
    opacity: 0;
  }

  .change-card-leave-to {
    transform: translate(20rem, 0);
    opacity: 0;
  }

  .change-card-enter-active, .change-card-leave-active {
    transition: all 0.3s ease;
  }
</style>
