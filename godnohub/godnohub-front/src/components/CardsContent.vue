<template>
  <div>
    <div class="view-wrapper">
      <div class="text">
        <span>Сменить вид:</span>
      </div>
      <div class="options">
        <div :class="['button', (display === 'full') ? 'active-view' : '']">
          <v-icon class="icon" @click="$store.dispatch('CHANGE_DISPLAY', 'full')">mdi-grid-large</v-icon>
        </div>
        <div :class="['button', (display === 'list') ? 'active-view' : '']">
          <v-icon class="icon" @click="$store.dispatch('CHANGE_DISPLAY', 'list')">mdi-format-columns</v-icon>
        </div>
      </div>
    </div>
    <v-layout wrap v-if="display === 'full'">
      <v-col class="px-1" v-for="(c, i) in colNum" :key="c">
        <v-flex  v-for="(item, index) in info" :key="item.id" class="pb-3" v-if="colIndexes[i].includes(index)">
          <card
            :editing="false"
            :news="news"
            :info="item"
            :later="later"
            :display="display"
            :newCard="(last_check) ? (last_check < new Date(item.timestamp)) : null"
            :owner="(followings) ? followings.find(x => x.id === item.owner) : null"
            :tagsFiltered="tagsFiltered">
          </card>
        </v-flex>
      </v-col>
    </v-layout>
    <v-layout wrap v-if="display === 'list'">
      <v-flex xs12 md6 lg4 v-for="item in info" :key="item.id" class="pb-3 px-1">
        <card
          :editing="false"
          :news="news"
          :info="item"
          :later="later"
          :display="display"
          :newCard="(last_check) ? (last_check < new Date(item.timestamp)) : null"
          :owner="(followings) ? followings.find(x => x.id === item.owner) : null"
          :tagsFiltered="tagsFiltered">
        </card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'CardsContent',
    props: ['info', 'news', 'tagsFiltered', 'followings', 'last_check', 'later'],
    data () {
      return {
        colNum: 2,
        oldColNum: 0,
        colIndexes: [[], [], []]
      }
    },
    computed: {
      ...mapGetters({
        display: 'CARD_DISPLAY'
      })
    },
    methods: {
      handleResize () {
        if (window.innerWidth <= 960) {
          this.colNum = 1
        } else if (window.innerWidth <= 1264) {
          this.colNum = 2
        } else if (window.innerWidth >= 1604) {
          this.colNum = 3
        }
        if (this.oldColNum !== this.colNum) this.colsDistribution()
      },
      colsDistribution () {
        let tmpCols = JSON.parse(JSON.stringify(this.colNum))
        if (tmpCols === 1) {
          this.colIndexes[0] = [...Array(this.info.length).keys()]
          this.oldColNum = 1
        } else if (tmpCols === 2) {
          this.colIndexes[0] = [...Array(this.info.length).keys()].filter((x, i) => i % 2 === 0)
          this.colIndexes[1] = [...Array(this.info.length).keys()].filter((x, i) => i % 2 !== 0)
          this.oldColNum = 2
        } else if (tmpCols === 3) {
          for (let c = 0; c < 6; c++) {
            this.colIndexes[c] = []
          }
          for (let i = 0; i < this.info.length; i++) {
            for (let c = 0; c < tmpCols; c++) {
              if ((i + (tmpCols - c)) % tmpCols === 0) this.colIndexes[c].push(i)
            }
          }
          this.oldColNum = 3
        }
      }
    },
    watch: {
      'info' () {
        this.colsDistribution()
      },
      'display' () {
        this.colsDistribution()
      }
    },
    created () {
      window.addEventListener('resize', this.handleResize)
      this.handleResize()
    },
    destroyed () {
      window.removeEventListener('resize', this.handleResize)
    }
  }
</script>

<style scoped>
  .view-wrapper {
    width: 99%;
    padding-right: 1%;
    margin: 0;
    display: flex;
    justify-content: flex-end;
  }

  .options {
    display: flex;
  }

  .text {
    font-family: 'Roboto', sans-serif;
    font-size: .9rem;
    color: #9b9b9b;
    margin-right: 0.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }


  .icon {
    color: #929292;
    cursor: pointer;
    margin: 0;
  }

  .button {
    margin-right: 0.3rem;
    padding: 0.1rem;
    border-radius: 0.3rem;
    transition: 0.3s all ease-in;
  }

  .button:hover {
    background: #e6e6e6;
  }

  .active-view {
    background: #e6e6e6;
  }
</style>
