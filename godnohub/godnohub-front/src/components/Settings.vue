<template>
  <div>
    <div @click="openDialog">
      <slot></slot>
    </div>
    <v-dialog
      width="unset"
      v-model="settingsDialog"
    >
      <v-card>
        <v-icon small class="close-dialog" @click="settingsDialog = false">mdi-close</v-icon>
        <div class="settings-card">
          <h1 class="headline">Настройки аккаунта</h1>
          <v-layout row wrap class="px-3">
            <v-flex>
              <v-list class="pr-5">
                <v-list-item
                  :class="(block === 'profile') ? 'active-opt' : ''"
                  color="grey darken-2"
                  @click="block = 'profile'">
                  <span class="option">Профиль</span>
                </v-list-item>
                <v-list-item
                  :class="(block === 'collection') ? 'active-opt' : ''"
                  color="grey darken-2"
                  @click="block = 'collection'">
                  <span class="option">Коллекция</span>
                </v-list-item>
              </v-list>
            </v-flex>
            <v-flex>
              <!-- Nickname -->
              <v-card elevation="3" class="px-9 py-3 block-card" v-if="block === 'profile'">
                <h1 class="card-headline">Выбор клички</h1>
                <p style="text-align: center">
                  <span class="pre-nickname">{{preNickText}}</span>
                  <span class="nickname">{{actualNick}}</span>
                </p>
                <v-text-field
                  dense
                  clearable
                  v-model="nickname"
                  prepend-icon="mdi-pencil"
                  :rules="[v => !v || v.length <= 13 || 'Не больше 13-х символов']"
                  class="pa-0 ma-0"
                  label="Новая кличка"
                  @keypress.enter="changeNickname">
                </v-text-field>
                <div class="btn-wrapper">
                  <v-btn dense text :color="nickBlock.color" @click="changeNickname">
                    <v-progress-circular
                      v-if="nickBlock.loading"
                      indeterminate
                      color="grey"
                      class="mr-2"
                      size="18"
                      width="2"
                    ></v-progress-circular>
                    <v-icon left v-if="!nickBlock.loading && nickBlock.success == null">mdi-pencil</v-icon>
                    <v-icon left v-if="!nickBlock.loading && nickBlock.success == true">mdi-check</v-icon>
                    <v-icon left v-if="!nickBlock.loading && nickBlock.success == false">mdi-alert-circle-outline</v-icon>
                    Обновить
                  </v-btn>
                </div>
              </v-card>
              <!-- Avatar -->
              <v-card elevation="3" class="px-9 py-3 block-card" v-if="block === 'profile'">
                <h1 class="card-headline">Выбор аватара</h1>
                <v-layout>
                  <v-flex xs12 md8>
                    <v-flex>
                      <v-file-input
                        dense
                        accept="image/png, image/jpeg"
                        class="pa-0 ma-0"
                        label="Загрузить картинку"
                        prepend-icon="mdi-camera"
                        :rules="[v => !v || v.size < 2000000 || 'Не больше 2-х Мб!']"
                        v-model="avatarFile">
                      </v-file-input>
                    </v-flex>
                    <v-flex class="or-wrapper">
                      <span>или</span>
                    </v-flex>
                    <v-flex>
                      <v-text-field
                        dense
                        clearable
                        prepend-icon="mdi-link-variant"
                        v-model="imageUrl"
                        class="pa-0 ma-0"
                        label="Указать URL"
                        @keypress.enter="uploadAvatar">
                      </v-text-field>
                    </v-flex>
                  </v-flex>
                  <v-flex xs12 md4 class="pl-7">
                    <v-avatar color="grey lighten-1" size="73">
                      <v-img v-if="avatarPreview" :src="avatarPreview"/>
                    </v-avatar>
                    <div class="preview">Аватар</div>
                  </v-flex>
                </v-layout>
                <div class="btn-wrapper">
                  <v-btn dense text :color="avaBlock.color" @click="uploadAvatar">
                    <v-progress-circular
                      v-if="avaBlock.loading"
                      indeterminate
                      color="grey"
                      class="mr-2"
                      size="18"
                      width="2"
                    ></v-progress-circular>
                    <v-icon left v-if="!avaBlock.loading && avaBlock.success == null">mdi-file-upload-outline</v-icon>
                    <v-icon left v-if="!avaBlock.loading && avaBlock.success == true">mdi-check</v-icon>
                    <v-icon left v-if="!avaBlock.loading && avaBlock.success == false">mdi-alert-circle-outline</v-icon>
                    Загрузить
                  </v-btn>
                </div>
              </v-card>
              <!-- Collection -->
              <v-card elevation="3" class="px-9 py-3 block-card" v-if="block === 'collection'">
                <h1 class="card-headline">Адрес коллекции</h1>
                <p style="text-align: center">
                  <span class="pre-nickname">Текущий адрес: </span>
                  <a class="nickname">https://godnohub.herokuapp.com/{{actualAddress}}</a>
                </p>
                <v-text-field
                  dense
                  clearable
                  v-model="address"
                  prepend-icon="mdi-slash-forward"

                  :rules="[
                    v => !v || v.length <= 12 || 'Не больше 12-х символов',
                    v => !v || /^[a-z0-9]+$/.test(v) || 'Только латинские буквы и цифры'
                  ]"
                  class="pa-0 ma-0"
                  label="Новый адрес"
                  @keypress.enter="changeAddress">
                </v-text-field>
                <div class="btn-wrapper">
                  <v-btn dense text :color="addrBlock.color" @click="changeAddress">
                    <v-progress-circular
                      v-if="addrBlock.loading"
                      indeterminate
                      color="grey"
                      class="mr-2"
                      size="18"
                      width="2"
                    ></v-progress-circular>
                    <v-icon left v-if="!addrBlock.loading && addrBlock.success == null">mdi-pencil</v-icon>
                    <v-icon left v-if="!addrBlock.loading && addrBlock.success == true">mdi-check</v-icon>
                    <v-icon left v-if="!addrBlock.loading && addrBlock.success == false">mdi-alert-circle-outline</v-icon>
                    Обновить
                  </v-btn>
                </div>
              </v-card>
            </v-flex>
          </v-layout>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlAvatar = '/api/v1/account/load_avatar/'
  const urlNickname = '/api/v1/account/change_nickname/'
  const urlAddress = '/api/v1/account/change_page_id/'

  export default {
    name: 'Settings',
    props: ['avatarUrl'],
    data () {
      return {
        block: 'profile',
        card: null,
        settingsDialog: false,
        nickBlock: {
          loading: false,
          success: null,
          color: 'primary'
        },
        avaBlock: {
          loading: false,
          success: null,
          color: 'primary'
        },
        addrBlock: {
          loading: false,
          success: null,
          color: 'primary'
        },
        imageUrl: null,
        avatarFile: null,
        avatarPreview: this.$store.getters.AVATAR,
        nickname: null,
        actualNick: this.$store.getters.USERNAME,
        preNickText: 'Сейчас я ',
        address: null,
        actualAddress: this.$store.getters.HOME_PAGE
      }
    },
    watch: {
      'avatarFile' (file) {
        this.avatarPreview = (file) ? URL.createObjectURL(file) : this.imageUrl
      },
      'imageUrl' (url) {
        if (!this.avatarFile) this.avatarPreview = url
      },
      'block' () {
        this.loading = false
        this.success = null
        this.color = 'primary'
      }
    },
    methods: {
      openDialog () {
        setTimeout(() => { this.settingsDialog = true })
      },
      changeAddress () {
        if (
          this.actualAddress !== this.address &&
          this.address &&
          this.address.length <= 12
        ) {
          this.addrBlock.color = 'primary'
          this.addrBlock.loading = true
          let r = new Promise((resolve, reject) => {
            axios.post(urlAddress, { page_id: this.address })
              .then(response => {
                if (response.status === 200) {
                  resolve(this.address)
                } else {
                  reject(new Error('Loading avatar error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Loading avatar error'))
              })
          })
          r.then(
            (result) => {
              this.addrBlock.loading = false
              this.addrBlock.success = true
              this.addrBlock.color = 'success'
              this.$store.dispatch('SET_INFO')
              this.actualAddress = result
            },
            (error) => {
              console.log(error)
              this.addrBlock.loading = false
              this.addrBlock.success = false
              this.addrBlock.color = 'red lighten-1'
            }
          )
        }
      },
      changeNickname () {
        if (
          this.actualNick !== this.nickname &&
          this.nickname &&
          this.nickname.length <= 33
        ) {
          this.nickBlock.color = 'primary'
          this.nickBlock.loading = true
          let r = new Promise((resolve, reject) => {
            axios.post(urlNickname, { nickname: this.nickname })
              .then(response => {
                if (response.status === 200) {
                  resolve(this.nickname)
                } else {
                  reject(new Error('Loading avatar error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Loading avatar error'))
              })
          })
          r.then(
            (result) => {
              this.nickBlock.loading = false
              this.nickBlock.success = true
              this.nickBlock.color = 'success'
              this.$store.dispatch('SET_INFO')
              this.preNickText = 'Теперь я '
              this.actualNick = result
            },
            (error) => {
              console.log(error)
              this.nickBlock.loading = false
              this.nickBlock.success = false
              this.nickBlock.color = 'red lighten-1'
            }
          )
        }
      },
      uploadAvatar () {
        if (this.avatarFile) {
          this.avaBlock.color = 'primary'
          this.avaBlock.loading = true
          let r = new Promise((resolve, reject) => {
            axios.put(urlAvatar, this.avatarFile)
              .then(response => {
                if (response.status === 200 && response.data.avatar_url !== 'error') {
                  resolve(true)
                } else {
                  reject(new Error('Loading avatar error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Loading avatar error'))
              })
          })
          r.then(
            (result) => {
              this.avaBlock.loading = false
              this.avaBlock.success = true
              this.avaBlock.color = 'success'
              this.$store.dispatch('SET_INFO')
            },
            (error) => {
              console.log(error)
              this.avaBlock.loading = false
              this.avaBlock.success = false
              this.avaBlock.color = 'red lighten-1'
            }
          )
        } else if (this.imageUrl) {
          this.avaBlock.loading = true
          this.avaBlock.color = 'primary'
          let r = new Promise((resolve, reject) => {
            axios.post(urlAvatar, {image_url: this.imageUrl})
              .then(response => {
                if (response.status === 200 && response.data.avatar_url !== 'error') {
                  resolve(true)
                } else {
                  reject(new Error('Loading avatar error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Loading avatar error'))
              })
          })
          r.then(
            (result) => {
              this.avaBlock.loading = false
              this.avaBlock.success = true
              this.avaBlock.color = 'success'
              this.$store.dispatch('SET_INFO')
            },
            (error) => {
              console.log(error)
              this.avaBlock.loading = false
              this.avaBlock.success = false
              this.avaBlock.color = 'red lighten-1'
            }
          )
        }
      }
    }
  }
</script>

<style scoped>
  div .v-dialog {
    z-index: 999;
  }

  .headline {
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 1.3rem;
    text-align: center;
  }

  .card-headline {
    font-size: 1.3rem;
    font-family: 'Roboto', sans-serif;
    font-weight: 400;
    color: #7a7a7a;
    margin-bottom: 0.9rem;
    position: relative;
  }

  .card-headline::before {
    content: '';
    position: absolute;
    height: 1px;
    width: 70%;
    bottom: 0;
    left: 0;
    background: #ebebeb;
  }

  .settings-card {
    padding: 1.3rem 1.5rem;
  }

  .block-card {
    min-width: 25rem;
    margin-bottom: 1rem;
  }


  .active-opt {
    transition: 0.3s all ease-out;
    font-weight: 500;
    color: #474747;
    background: #f8f8f8;
  }

  .option {
    font-family: 'Roboto', sans-serif;
    color: #686868;
    word-break: break-all;
    min-width: 9rem;
  }

  @media screen and (max-width: 600px) {
    .block-card {
      min-width: 0;
    }

    .option {
      min-width: 0;
    }
  }

  .pre-nickname {
    font-family: 'Roboto', sans-serif;
    font-size: 0.9rem;
    color: #999999;
  }

  .nickname {
    font-family: 'Roboto', sans-serif;
    font-weight: 400;
    cursor: default;
  }

  .avatar-upload-inputs {
    display: flex;
  }

  .or-wrapper {
    display: flex;
    justify-content: flex-end;
    font-size: 0.9rem;
    color: #757575;
  }

  .preview {
    font-size: 0.9rem;
    color: #757575;
    text-align: center;
    width: 73px;
  }

  .btn-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  @media screen and (max-width: 1000px) {
    .settings-card {
      min-width: 0;
    }
  }

  .close-dialog {
    cursor: pointer;
    position: absolute;
    right: 1rem;
    top: 1rem;
  }
</style>
