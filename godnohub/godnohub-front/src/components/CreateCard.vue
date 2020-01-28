<template>
  <div>
    <div @click="openDialog">
      <slot></slot>
    </div>
    <v-dialog
      width="unset"
      v-model="createCardDialog"
    >
      <v-card>
        <v-icon small class="close-dialog" @click="createCardDialog = false">mdi-close</v-icon>
        <div class="create-card">
          <h1 class="headline">Создание контента</h1>
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            class="card-form">
            <v-layout wrap>
              <v-flex xs12 md12 lg6 class="pa-0">
                <!-- Type -->
                <v-combobox
                  v-model="cardType.value"
                  :items="cardType.variants"
                  item-text="name"
                  item-value="id"
                  :search-input.sync="cardType.search"
                  hide-selected
                  label="Группа"
                  persistent-hint
                  :rules="typeRules"
                  required
                >
                  <template v-if="cardType.noData" v-slot:no-data>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          "<strong>{{ cardType.search }}</strong>" нету. Нажми <kbd>enter</kbd> для добавления.
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                  <template v-slot:selection="data">
                    <v-chip
                      small
                      v-if="data.item.id"
                      :key="data.item.id"
                      :input-value="data.selected"
                      class="v-chip--select-multi">
                      <v-icon
                        size="21"
                        v-if="newTypeChecker(data.item.name) && gotFilters"
                        title="Новая группа"
                        color="#57B27A">
                        mdi-new-box</v-icon>
                      <span>{{ data.item.name }}</span>
                    </v-chip>
                    <v-chip
                      small
                      v-if="!data.item.id"
                      :key="data.item"
                      :input-value="data.selected"
                      class="v-chip--select-multi">
                      <v-icon
                        size="21"
                        v-if="newTypeChecker(data.item) && gotFilters"
                        title="Новая группа"
                        color="#57B27A">
                        mdi-new-box</v-icon>
                      <span>{{ data.item }}</span>
                    </v-chip>
                  </template>
                </v-combobox>
                <!-- Title -->
                <v-text-field
                  v-model="cardTitle"
                  @blur="getImages(false)"
                  @keypress.enter="getImages(false)"
                  label="Название"
                  :rules="titleRules"
                  required>
                  </v-text-field>
                <!-- Image -->
                <div class="image-input-group">
                  <v-progress-linear indeterminate v-if="imageLoading" class="pa-0 ma-0"></v-progress-linear>
                  <v-layout wrap v-if="images.length > 0" style="max-width: 35rem">
                    <v-flex md2 class="px-1" v-for="(img, index) in images" :key="index">
                      <v-img
                        :src="img || 'https://i.imgur.com/ZRguE01.png'"
                        contain
                        height="9rem"
                        :class="[(cardURL === img) ? 'active-img' : '', 'image-pick']"
                        @click="cardURL = img"></v-img>
                    </v-flex>
                  </v-layout>
                  <p class="image-page" v-if="images.length > 0" @click="imagePage += 1">Еще</p>
                  <v-checkbox v-model="typeCover" dense label="Обложка группы" style="float: right" class="pl-1"></v-checkbox>
                  <v-text-field v-model="cardURL" label="URL картинки"></v-text-field>
                </div>
                <!-- Tags -->
                <v-combobox
                  v-model="cardTags.value"
                  :items="cardTags.variants"
                  :search-input.sync="cardTags.search"
                  item-text="name"
                  item-value="id"
                  hide-selected
                  label="Тэги"
                  persistent-hint
                  small-chips
                  multiple
                  deletable-chips
                  :rules="tagRules">
                  <template v-if="cardTags.noData" v-slot:no-data>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          "<strong>{{ cardTags.search }}</strong>" нету. Нажми <kbd>enter</kbd> для добавления.
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                  <template v-slot:selection="data">
                    <v-chip
                      small
                      v-if="data.item.id"
                      :key="data.item.id"
                      :input-value="data.selected"
                      class="v-chip--select-multi pr-1">
                      <v-icon
                        v-if="newTagChecker(data.item.name) && gotFilters"
                        title="Новый тэг"
                        size="21"
                        color="#57B27A">
                        mdi-new-box</v-icon>
                      <span class="mr-2">{{ data.item.name }}</span>
                      <v-icon
                        small
                        title="Убрать тэг"
                        size="18"
                        @click="data.parent.selectItem(data.item)"
                      >mdi-close</v-icon>
                    </v-chip>
                    <v-chip
                      small
                      v-if="!data.item.id"
                      :key="data.item"
                      :input-value="data.selected"
                      class="v-chip--select-multi pr-1">
                      <v-icon
                        v-if="newTagChecker(data.item) && gotFilters"
                        title="Новый тэг"
                        size="21"
                        color="#57B27A">
                        mdi-new-box</v-icon>
                      <span class="mr-2">{{ data.item }}</span>
                      <v-icon
                        small
                        title="Убрать тэг"
                        color="grey darken-1"
                        @click="data.parent.selectItem(data.item)"
                      >mdi-close</v-icon>
                    </v-chip>
                  </template>
                </v-combobox>
                <!-- Rating -->
                <v-checkbox
                  on-icon="mdi-clock"
                  class="pl-3"
                  v-model="postStorage"
                  :disabled="later"
                  dense
                  label="Отложить"
                  style="float: right"></v-checkbox>
                <v-autocomplete
                  :disabled="postStorage"
                  v-model="cardRate.value"
                  :items="cardRate.variants"
                  item-text="name"
                  item-value="rate"
                  :search-input.sync="cardRate.search"
                  label="Степень годноты"
                  small-chips
                  :rules="rateRules"
                  required
                >
                </v-autocomplete>
              </v-flex>
              <v-flex xs12 md12 lg6 class="pa-0">
                <div class="card-wrapper">
                  <card
                    :editing="true"
                    :info="resultCard"
                    :display="'full'"
                    :news="false"
                    :tagsFiltered="[]">
                  </card>
                </div>
              </v-flex>
            </v-layout>
            <v-row justify="end" class="mt-3">
              <v-btn color="grey" outlined @click="clearAll" dense style="margin-right: 1rem">
                <v-icon left>mdi-close</v-icon>
                Очистить
              </v-btn>
              <v-btn :disabled="!valid" :color="color" @click="post" dense>
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                  color="white darken-1"
                  class="mr-2"
                  size="18"
                  width="2"
                ></v-progress-circular>
                <v-icon left v-if="!loading && success == null">mdi-content-save-outline</v-icon>
                <v-icon left v-if="!loading && success == true">mdi-check</v-icon>
                <v-icon left v-if="!loading && success == false">mdi-alert-circle-outline</v-icon>
                Сохранить
              </v-btn>
            </v-row>
          </v-form>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'

  const urlPost = '/api/v1/card/create/'
  const urlImages = '/api/v1/card/get_images/'
  const urlFilters = '/api/v1/filters/'

  export default {
    name: 'CreateCard',
    props: ['cardInfo', 'editing', 'later'],
    data () {
      return {
        valid: false,
        gotFilters: false,
        postStorage: false,
        createCardDialog: false,
        loading: false,
        success: null,
        color: 'success',
        cardId: null,
        cardTitle: null,
        cardURL: null,
        imageLoading: false,
        searched: null,
        imagePage: 1,
        images: [],
        typeCover: false,
        cardType: {
          value: '',
          variants: [],
          search: null,
          noData: true
        },
        cardTags: {
          value: null,
          variants: [],
          search: null,
          noData: true
        },
        cardRate: {
          value: null,
          variants: [],
          search: null,
          noData: true
        },
        resultCard: {
          title: 'Название',
          color: '#818181',
          id: 0,
          imgur_url: 'https://i.imgur.com/ZRguE01.png',
          rating: {name: 'Степень годноты', id: 0},
          tags: [{name: 'Тэги', id: 0}],
          type: {name: 'Тип', id: 0}
        },
        titleRules: [
          v => {
            if (v) {
              if (v.length > 100) {
                return 'Название не может быть длиннее 100-х символов'
              } else {
                return true
              }
            } else {
              return 'Нужно указать название'
            }
          }
        ],
        tagRules: [
          v => {
            if (v) {
              if (v.length > 10) {
                return 'Не больше 10-ти тэгов'
              } else if (v.length > 0) {
                for (let i = 0; i < v.length; i++) {
                  if (v[i].length > 33) {
                    return 'Тэг не может быть длиннее 33-х символов'
                  } else {
                    return true
                  }
                }
              } else {
                return true
              }
            } else {
              return true
            }
          }
        ],
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
        ],
        rateRules: [
          v => {
            if (this.postStorage) {
              return true
            } else {
              if (v) {
                return true
              } else {
                return 'Нужно дать оценку'
              }
            }
          }
        ]
      }
    },
    watch: {
      imagePage: function () {
        this.getImages(true)
      },
      cardURL: function (val) {
        this.resultCard.imgur_url = (val === '') ? 'https://i.imgur.com/ZRguE01.png' : val
      },
      cardTitle: function (val) {
        this.resultCard.title = val
      },
      'cardType.value': function (val) {
        this.resultCard.type = (typeof val === 'string') ? {name: val, id: 0} : val
      },
      'cardRate.value': function (val) {
        const rates = {
          6: 'Без сознания',
          1: 'Одним глазком',
          2: 'Годнота',
          3: 'Абсолютная годнота',
          9: 'Скрытая годнота'
        }
        this.resultCard.rating = (Number.isInteger(val)) ? {name: rates[val], rate: val} : val
      },
      'cardTags.value': function (val) {
        let tags = []
        if (Array.isArray(val)) {
          for (let i = 0; i < val.length; i++) {
            const tag = val[i]
            if (typeof tag === 'string') {
              tags.push({name: tag, id: 0})
            } else {
              tags.push(tag)
            }
          }
          this.resultCard.tags = tags
        } else {
          this.resultCard.tags = {name: val, id: 0}
        }
      }
    },
    methods: {
      newTagChecker (value) {
        for (let i = 0; i < this.cardTags.variants.length; i++) {
          const element = this.cardTags.variants[i].name
          if (element.toLowerCase() === value.toLowerCase()) return false
        }
        return true
      },
      newTypeChecker (value) {
        for (let i = 0; i < this.cardType.variants.length; i++) {
          const element = this.cardType.variants[i].name
          if (element.toLowerCase() === value.toLowerCase()) return false
        }
        return true
      },
      clearAll () {
        this.cardType.value = null
        this.cardTags.value = null
        this.cardTitle = null
        this.cardURL = null
        this.resultCard.color = null
        this.cardRate.value = null
        this.typeCover = false
      },
      openDialog () {
        this.getFilters()
        setTimeout(() => { this.createCardDialog = true })
      },
      getImages (nextPage) {
        if ((this.cardTitle && !this.imageLoading && this.searched !== this.cardTitle) || nextPage) {
          let r = new Promise((resolve, reject) => {
            this.imageLoading = true
            if (this.searched !== this.cardTitle) {
              this.imagePage = 1
              this.searched = this.cardTitle
            }

            axios.get(urlImages, {
              params: {
                title: this.cardTitle,
                page: this.imagePage
              }
            })
              .then(response => {
                if (response.status === 200) {
                  this.images = response.data.images
                  resolve(true)
                } else {
                  reject(new Error('Getting card images error'))
                }
              })
              .catch(error => {
                console.log(error)
                reject(new Error('Getting card images error'))
              })
          })
          r.then(
            (result) => {
              this.imageLoading = false
            },
            (error) => {
              console.log(error)
              this.imageLoading = false
            }
          )
        }
      },
      getFilters () {
        let pageId = this.$store.getters.HOME_PAGE
        axios.get(urlFilters, {
          params: {
            page_id: pageId,
            type_id: 'all'
          }
        })
          .then(response => {
            let data = response.data
            this.cardType.variants = data.types
            this.cardTags.variants = data.tags
            this.cardRate.variants = data.rates
            this.gotFilters = true
          })
          .catch(error => {
            console.log(error)
          })
        if (this.cardInfo) {
          this.cardType.value = this.cardInfo.type
          this.cardTags.value = this.cardInfo.tags
          this.cardTitle = this.cardInfo.title
          this.cardURL = this.cardInfo.imgur_url
          this.resultCard.color = this.cardInfo.color
          this.cardId = this.cardInfo.id
          this.cardRate.value = (this.later) ? null : this.cardInfo.rating.rate
        }
      },
      post () {
        if (this.$refs.form.validate()) {
          this.loading = true
          let r = new Promise((resolve, reject) => {
            axios.post(urlPost, {
              title: this.cardTitle,
              img_url: this.cardURL,
              rating: this.cardRate.value,
              tags: this.cardTags.value,
              type: this.cardType.value,
              cover: this.typeCover,
              post_storage: this.postStorage,
              from_post_storage: this.later === true,
              id: this.cardId
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
              this.loading = false
              this.success = true
              this.color = 'success'
              let self = this
              setTimeout(function () {
                self.$router.go()
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
      }
    }
  }
</script>

<style scoped>
  div .v-dialog {
    z-index: 999
  }

  .headline {
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 1.3rem;
  }

  .create-card {
    padding: 1rem 3rem;
    min-width: 68rem;
  }

  .card-form {
    padding-right: 1.3rem;
  }

  .card-wrapper {
    width: 100%;
    padding-left: 1.3rem;
    display: block;
  }

  @media screen and (max-width: 1000px) {
    .card-wrapper {
      padding-left: 0;
    }
    .create-card {
      min-width: 0;
    }
  }

  .close-dialog {
    cursor: pointer;
    position: absolute;
    right: 1rem;
    top: 1rem;
  }

  .image-pick {
    cursor: pointer;
  }

  .active-img {
    border: 1px solid #1976d270;
  }

  .image-page {
    text-align: right;
    font-size: 0.8rem;
    margin: 0;
    color: #1976d2;
    cursor: pointer;
  }
</style>
