<template>
  <div @click="logout">
    <slot></slot>
  </div>
</template>

<script>
import axios from 'axios'

const urlLogout = '/api/v1/auth/logout/'

export default {
  name: 'Logout',
  data () {
    return {
      color: 'success'
    }
  },
  methods: {
    logout () {
      axios.post(urlLogout)
        .then(response => {
          if (response.status === 200) {
            this.$store.dispatch('LOGOUT')
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style>
</style>
