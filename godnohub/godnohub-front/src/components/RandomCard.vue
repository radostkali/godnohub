<template>
  <div class="wrapper">
    <div class="card-container">
      <transition name="change-card" mode="out-in">
        <card
          :key="card.info.id"
          v-if="card"
          :editing="false"
          :news="true"
          :info="card.info"
          :display="'full'"
          :newCard="false"
          :owner="card.owner"
          :tagsFiltered="[]"
          ></card>
      </transition>
    </div>
    <div class="card-random">
      <v-btn small outlined color="grey" @click="getCard">
        <v-progress-circular
          v-if="loading"
          indeterminate
          color="grey darken-1"
          class="mr-1"
          size="18"
          width="1"
        ></v-progress-circular>
        Случайная карточка
      </v-btn>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import OwnerCard from './OwnerCard'

  const urlRandCard = '/api/v1/random_card/'

  export default {
    name: 'RandomCollections',
    components: { OwnerCard },
    data () {
      return {
        card: null,
        loading: false
      }
    },
    methods: {
      getCard () {
        this.loading = true
        let r = new Promise((resolve, reject) => {
          axios.get(urlRandCard)
            .then(response => {
              this.card = response.data
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
      this.getCard()
    }
  }
</script>

<style scoped>
  .wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .card-container {
    width: 90%;
    max-width: 37rem;
    position: relative;
  }

  .card-random {
    margin-top: 3rem;
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
