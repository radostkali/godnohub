<template>
  <div>
    <div style="display: flex">
      <div @click="loginDialog = true">
        <slot name="login-link">
          <v-btn text small color="primary">Войти</v-btn>
        </slot>
      </div>
      <div @click="registrationDialog = true">
        <slot name="registration-link">
          <v-btn text small color="primary">Создать аккаунт</v-btn>
        </slot>
      </div>
    </div>
    <v-dialog
      v-model="loginDialog"
    >
      <v-card class="login-card" v-on:keyup.enter="authenticate">
        <div class="login-screen">
          <h1 class="headline">Вход в чудесный мир годного контента</h1>
          <v-form class="login-form">
            <v-text-field
              label="Ящик"
              name="Почта"
              type="text"
              v-model="username">
              <v-icon slot="prepend">mdi-account</v-icon>
            </v-text-field>

            <v-text-field
              label="Пароль"
              name="password"
              type="password"
              v-model="password">
              <v-icon slot="prepend">mdi-lock</v-icon>
            </v-text-field>
          </v-form>

          <v-card-actions>
            <v-btn small text color="grey lighten-1" @click="registrationInit">Создать аккаунт</v-btn>
            <v-spacer></v-spacer>
            <v-btn small outlined :color="color" @click="authenticate">
              <v-progress-circular
                v-if="loading"
                indeterminate
                color="grey darken-1"
                class="mr-1"
                size="18"
                width="1"
              ></v-progress-circular>
              <v-icon left v-if="!loading && success == null">mdi-account-outline</v-icon>
              <v-icon left v-if="!loading && success == true" color="green">mdi-check</v-icon>
              <v-icon left v-if="!loading && success == false" color="red lighten-1">mdi-alert-circle-outline</v-icon>
              Войти
            </v-btn>
          </v-card-actions>
        </div>

      </v-card>
    </v-dialog>

    <v-dialog
      v-model="registrationDialog"
    >
      <v-card class="login-card">
        <div class="login-screen">
          <h1 class="headline">Включение в Годнохаб</h1>
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            class="login-form">
            <v-text-field
              v-model="name"
              label="Кличка"
              :rules="[
                v => !!v || 'Нужно выбрать кличку',
                v => v.length <= 13 || 'Кличка должна быть короткой и емкой (не больше 13-ти символов)'
              ]"
              required>
            ></v-text-field>
            <v-text-field
              v-model="email"
              label="Почта"
              :rules="[
                v => !!v || 'Нужно указать ящик', v => /.+@.+\..+/.test(v) || 'Ящик указан некорректно',
                v => v.length <= 33 || 'Не больше 33-х символов',
                v => /^\S*$/.test(v) || 'Почта с пробелами? -_-'
              ]"
              required
            ></v-text-field>
            <v-text-field
              label="Пароль"
              name="password"
              type="password"
              v-model="newPassword"
              :rules="[
                v => !!v || 'Нужно указать пароль',
                v => /^(?=.[A-Za-z!%&'()*+./;<=>?\\,/:#@-\[\]_])(?=.*\d)[A-Za-z!%&'()*+./;<=>?\\,/:#@-\[\]_\d]/.test(v)
                  || 'Пароль может включать только латинские буквы, цифры и специальные символы',
                v => v.length <= 40 || 'Не больше 40-ка символов',
                v => v.length >= 7 || 'Не меньше 7-ми символов',
                v => /^\S*$/.test(v) || 'Укажите пароль без пробелов'
              ]"
              required>
            </v-text-field>
            <v-text-field
              label="Подтверждение пароля"
              name="password"
              type="password"
              v-model="confirmPassword"
              :rules="[
                v => !!v || 'Нужно в точности повторить пароль',
                v => (v === newPassword) || 'Пароль не совпадает'
              ]"
              required>
            </v-text-field>

            <v-checkbox
              v-model="checkbox"
              label="Согласен на полное отсутствие правил и политики конфиденциальности"
              type="checkbox"
              dense
              :rules="[v => !!v || 'Согласие с отсутствием правил абсолютно обязательно']"
              required
            ></v-checkbox>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn small outlined :color="color" @click="registrate" :disabled="!valid">
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                  color="grey darken-1"
                  class="mr-1"
                  size="18"
                  width="1"
                ></v-progress-circular>
                <v-icon left v-if="!loading && success == null">mdi-account-outline</v-icon>
                <v-icon left v-if="!loading && success == true" color="green">mdi-check</v-icon>
                <v-icon left v-if="!loading && success == false" color="red lighten-1">mdi-alert-circle-outline</v-icon>
                Зарегистрироваться
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-form>
        </div>

      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlRegister = '/api/v1/auth/create_account/'
  const urlLogin = '/api/v1/auth/login/'

  export default {
    name: 'Login',
    data () {
      return {
        valid: false,
        username: '',
        password: '',
        loginDialog: false,
        loading: false,
        success: null,
        color: 'grey darken-1',
        registrationDialog: false,
        name: '',
        email: '',
        newPassword: '',
        confirmPassword: '',
        checkbox: false
      }
    },
    methods: {
      authenticate () {
        this.loading = true
        this.color = 'grey darken-1'
        let a = new Promise((resolve, reject) => {
          axios.post(urlLogin, {
            username: this.username,
            password: this.password
          })
            .then(response => {
              if (response.status === 200) {
                resolve(true)
              } else {
                reject(new Error('Registration error'))
              }
            })
            .catch(error => {
              console.log(error)
              reject(new Error('Registration error'))
            })
        })
        a.then(
          (result) => {
            this.loading = false
            this.success = true
            this.color = 'green'
            let self = this
            this.$store.dispatch('LOGIN')
            this.$store.dispatch('SET_INFO')
            setTimeout(function () {
              self.closeLoginDialog()
            }, 300)
          },
          (error) => {
            console.error(error)
            this.loading = false
            this.success = false
            this.color = 'red lighten-1'
          }
        )
      },
      registrate () {
        if (this.$refs.form.validate()) {
          this.loading = true
          this.color = 'grey darken-1'
          let r = new Promise((resolve, reject) => {
            axios.post(urlRegister, {
              email: this.email,
              name: this.name,
              password: this.newPassword
            })
              .then(response => {
                if (response.data.status === 'Success') {
                  resolve(true)
                } else {
                  console.log(response.data.status)
                  reject(new Error('Registration error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Registration error'))
              })
          })
          r.then(
            (result) => {
              this.loading = false
              this.success = true
              this.color = 'green'
              this.$store.dispatch('LOGIN')
              this.$store.dispatch('SET_INFO')
              let self = this
              setTimeout(function () {
                self.$router.push({name: 'page', params: {page: self.$store.getters.HOME_PAGE}})
              }, 300)
            },
            (error) => {
              console.log(error)
              this.loading = false
              this.success = false
              this.color = 'red lighten-1'
            }
          )
        }
      },
      registrationInit () {
        this.closeLoginDialog()
        this.registrationDialog = true
      },
      closeLoginDialog () {
        this.username = ''
        this.password = ''
        this.loading = false
        this.success = null
        this.color = 'grey darken-1'
        this.loginDialog = false
      },
      closeRegistrationDialog () {
        this.loading = false
        this.success = null
        this.color = 'grey darken-1'
        this.name = ''
        this.email = ''
        this.newPassword = ''
        this.checkbox = false
        this.registrationDialog = false
      }
    },
    watch: {
      loginDialog (val) {
        !val && this.closeLoginDialog()
      },
      registrationDialog (val) {
        !val && this.closeRegistrationDialog()
      }
    }
  }
</script>

<style>
  .headline {
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 1.3rem;
  }

  div .v-dialog{
    width: 23rem;
    z-index: 999;
  }

  .login-card {
    padding: 1.3rem 2rem;
    overflow: hidden;
  }

  .login-form {
    margin: 0 1rem;
  }

  .error-msg {
    color: #ef5350;
    font-family: 'Roboto';
    font-size: 0.9rem;
  }
</style>
