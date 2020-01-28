<template>
  <div>
    <v-icon
      @click="postToStorage"
      v-if="!postStorageLoading && postStorageSuccess === null"
      title="Отложить"
      :small="small"
      color="grey">
      mdi-folder-clock
    </v-icon>
    <v-progress-circular
      v-if="postStorageLoading"
      indeterminate
      color="grey"
      class="mr-2"
      style="cursor: default"
      size="18"
      width="2"
    ></v-progress-circular>
    <v-icon
      v-if="!postStorageLoading && postStorageSuccess"
      title="Карточка отложена"
      style="cursor: default"
      :small="small"
      color="success">
      mdi-check-bold
    </v-icon>
    <v-icon
      @click="postToStorage"
      v-if="!postStorageLoading && (postStorageSuccess === false)"
      title="Ошибка"
      :small="small"
      color="error">
      mdi-alert-circle-outline
    </v-icon>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlPost = '/api/v1/card/create/'

  export default {
    name: 'ToPostStorage',
    props: ['cardInfo', 'small'],
    data () {
      return {
        postStorageLoading: false,
        postStorageSuccess: null
      }
    },
    methods: {
      postToStorage () {
        this.postStorageLoading = true
        let r = new Promise((resolve, reject) => {
          axios.post(urlPost, {
            title: this.cardInfo.title,
            img_url: this.cardInfo.imgur_url,
            tags: this.cardInfo.tags,
            type: this.cardInfo.type,
            post_storage: true,
            from_post_storage: false
          })
            .then(response => {
              if (response.status === 200) {
                resolve(true)
              } else {
                reject(new Error('Creating card error'))
              }
            })
            .catch(error => {
              console.log(error)
              reject(new Error('Creating card error'))
            })
        })
        r.then(
          (result) => {
            this.postStorageLoading = false
            this.postStorageSuccess = true
          },
          (error) => {
            console.log(error)
            this.postStorageLoading = false
            this.postStorageSuccess = false
          }
        )
      }
    }
  }
</script>

<style scoped>
  .v-snack {
    z-index: 1000 !important;
  }
</style>
