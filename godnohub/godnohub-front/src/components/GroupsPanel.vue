<template>
  <div id="groups">
    <v-row class="groups-container">
      <v-hover
        v-slot:default="{ hover }"
        v-for="item in types"
        :key="item.id">
        <div
          :class="[(typePicked == item.id) ? 'active-group' : '', 'group-card']"
          >
          <v-img
            class="group-image"
            :src="item.picture || 'https://i.imgur.com/ZRguE01.png'"
          >
            <template v-slot:placeholder>
              <div class="load-img-wrapper">
                <v-progress-circular
                  indeterminate
                  style="margin: auto"></v-progress-circular>
              </div>
            </template>
          </v-img>
          <div class="image-color" v-on:click.self="$emit('pick-type', item.id)">
            <v-icon
              small
              :style="hover ? 'display: block' : 'display: none'"
              class="edit-icon"
              title="Редактировать группу"
              color="white"
              v-if="homePageId == routePage"
              @click="openEditDialog(item)">
              mdi-pencil
            </v-icon>
            <div
              class="gradient"
              v-on:click.self="$emit('pick-type', item.id)"
              :style="item.color ?
                'background-image: linear-gradient(to top, ' + item.color + ', #00000000);' :
                'background-image: linear-gradient(to top, #28282850, #00000000);'"
            >
            </div>
            <span class="group-name" v-on:click.self="$emit('pick-type', item.id)">
              {{item.name}}
            </span>
          </div>
        </div>
      </v-hover>

      <v-dialog
        width="unset"
        v-model="editGroupDialogs"
        v-if="groupToEdit"
        @keypress.enter.prevent="editGroup"
      >
        <v-card>
          <v-icon small class="close-dialog" @click="editGroupDialogs = false">mdi-close</v-icon>
          <div class="edit-card">
            <h1 class="headline">Изменить группу</h1>
            <div class="edit-wrapper">
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                class="login-form">
                <v-text-field
                  label="Название"
                  name="Имя группы"
                  type="text"
                  :rules="typeRules"
                  v-model="groupToEdit.name"
                  required>
                </v-text-field>
                <div class="btn-wrapper">
                  <v-btn :disabled="!valid" dense outlined :color="color" @click="editGroup">
                    <v-progress-circular
                      v-if="loading"
                      indeterminate
                      color="grey"
                      class="mr-2"
                      size="18"
                      width="2"
                    ></v-progress-circular>
                    <v-icon left v-if="!loading && success == null">mdi-pencil</v-icon>
                    <v-icon left v-if="!loading && success == true">mdi-check</v-icon>
                    <v-icon left v-if="!loading && success == false">mdi-alert-circle-outline</v-icon>
                    Изменить
                  </v-btn>
                </div>
              </v-form>
            </div>
          </div>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlGroupEdit = '/api/v1/group_edit/'

  export default {
    name: 'GroupsPanel',
    props: ['typePicked', 'types', 'homePageId', 'routePage'],
    data () {
      return {
        valid: false,
        editGroupDialogs: false,
        groupToEdit: null,
        loading: false,
        success: null,
        color: 'primary',
        typeRules: [
          v => {
            if (v) {
              if (v.length > 33) {
                return 'Название группы не может быть длиннее 33-х символов'
              } else {
                return true
              }
            } else {
              return 'Нужно указать группу'
            }
          }
        ]
      }
    },
    methods: {
      openEditDialog (group) {
        this.groupToEdit = group
        this.editGroupDialogs = true
      },
      editGroup () {
        this.loading = true
        this.color = 'primary'
        axios.post(urlGroupEdit, {
          id: this.groupToEdit.id,
          name: this.groupToEdit.name
        })
          .then(response => {
            this.loading = false
            this.success = true
            this.color = 'green'
            let self = this
            setTimeout(function () {
              self.$router.go()
            }, 300)
          })
          .catch(error => {
            console.error(error)
            this.loading = false
            this.success = false
            this.color = 'red lighten-1'
          })
      }
    }
  }
</script>

<style scoped>
  .row {
    margin: 0;
  }

  .groups-container {
    margin: auto;
    margin-bottom: 0.5rem;
  }

  .group-card {
    height: 5rem;
    font-size: 1.3rem;
    width: 15%;
    max-width: 12rem;
    display: flex;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    border-radius: 0.7rem;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
    line-height: 1.1rem;
  }

  .group-image {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 120%;
    transform: translate(-50%, -50%) scale(1.3);
    filter: blur(3px);
    -webkit-filter: blur(3px);
    transition: 0.5s all ease-out;
  }

  .group-name {
    font-family: 'Oswald', sans-serif;
    color: white;
    font-weight: 300;
    padding: 0.1rem 0.3rem;
    margin-bottom: 0.7rem;
    width: 100%;
    word-break: break-word;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translate(-50%, 0);
    transition: 0.5s all ease-out;
  }

  .btn-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .active-group.group-card {
    font-size: 1.7rem;
  }

  @media screen and (max-width: 1024px) {
    .group-card {
      width: 25%;
      margin: 0 1.5%;
    }
  }

  @media screen and (max-width: 820px) {
    .groups-container {
      justify-content: center;
      max-width: 21rem;
    }

    .group-card {
      width: 47%;
      margin-bottom: 0.5rem;
      font-size: 1rem;
      height: 3rem;
    }

    .active-group.group-card {
      font-size: 1.5rem;
    }

    .active-group .group-name {
      bottom: 0.3rem;
    }
  }

  .image-color {
    height: 100%;
    width: 100%;
    background-color: #ebebeb50;
    position: relative;
    transition: 0.3s all ease;
  }

  .gradient {
    height: 70%;
    width: 100%;
    opacity: 0.5;
    position: absolute;
    bottom: 0;
  }

  .edit-icon {
    float: right;
    margin: 0.3rem 0.3rem 0 0;
  }

  .active-group .gradient {
    opacity: 0.8;
  }

  .image-color:hover, .active-group .image-color {
    background-color: #ebebeb30;
  }

  .active-group .group-image {
    filter: none;
    -webkit-filter: none;
    transform: translate(-50%, -50%) scale(1);
  }

  .load-img-wrapper {
    display: flex;
    justify-content: center;
    height: 17rem;
    width: 100%;
  }

  div .v-dialog {
    z-index: 999;
  }

  .headline {
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 1.3rem;
  }

  .edit-card {
    padding: 1rem 3rem;
  }

  @media screen and (max-width: 1000px) {
    .edit-card {
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
