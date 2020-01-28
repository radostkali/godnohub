<template>
  <div style="overflow: hidden">
    <div class="header-space"></div>
    <div class="first-block" :style="'height:' + (windowHeight - 48) + 'px'">
      <v-img
        :src="'/static/img/main-title/' + titleImages[titleImg]"
        height="100%"
        :class="['title-back-img', (titlePause) ? '' : 'invisible']"></v-img>
      <div class="title-block">
        <div class="title-block-container"
          @mouseenter="titleImgPause(true)"
          @mouseleave="titleImgPause(false)">
          <div class="title-image-wrapper">
            <div class="title-image-container">
              <v-img
                :src="'/static/img/main-title/' + titleImages[titleImg]"
                :class="(titlePause) ? 'invisible' : ''"
                height="100%"></v-img>
              <v-img
                :src="'/static/img/main-title/' + titleImages[titleImg+1]"
                height="100%"
                @load="imgLoaded"
                class="pre-loaded"></v-img>
            </div>
          </div>
          <div class="title-text">
            <p style="font-size: 3rem">Годнохаб</p>
            <p>Твоя коллекция годноты</p>
          </div>
        </div>
      </div>
      <div class="actions-block">
        <div class="action-wrapper wrapper-back">
          <span class="action-link how-link" v-scroll-to="'#how-block'">
            Что это?
          <div class="img-how">
            <v-img contain src="/static/img/main-els/how.png"></v-img>
          </div>
          </span>
        </div>
        <div class="action-wrapper wrapper-back">
          <span
            class="action-link"
            @mouseenter="eyeStatus = true"
            @mouseleave="eyeStatus = false"
            v-scroll-to="'#collections-block'">
            Посмотреть коллекции
          </span>
        </div>
        <div
          :class="(eyeStatus) ? 'img-eye' : 'img-eye-none'"
          :style="'top:' + eyeEls[0].top + 'px; left:' + eyeEls[0].left + 'px; width:' + eyeEls[0].width + 'px;'">
          <v-img contain src="/static/img/main-els/eye.png"></v-img>
        </div>
        <div
          :class="(eyeStatus) ? 'img-eye' : 'img-eye-none'"
          @mouseenter="eyeStatus = true"
          :style="'top:' + eyeEls[1].top + 'px; left:' + eyeEls[1].left + 'px; width:' + eyeEls[1].width + 'px;'">
          <v-img contain src="/static/img/main-els/eye.png"></v-img>
        </div>
        <div
          :class="(eyeStatus) ? 'img-eye' : 'img-eye-none'"
          :style="'top:' + eyeEls[2].top + 'px; left:' + eyeEls[2].left + 'px; width:' + eyeEls[2].width + 'px;'">
          <v-img contain src="/static/img/main-els/eye.png"></v-img>
        </div>
        <div class="action-wrapper wrapper-back">
          <login>
            <template v-slot:login-link><span></span></template>
            <template v-slot:registration-link>
              <span class="action-link vortex-link">Создать коллекцию
                <div class="img-vortex">
                  <v-img contain src="/static/img/main-els/vortex.png"></v-img>
                </div>
              </span>
            </template>
          </login>
        </div>
      </div>
    </div>
    <div class="how-block" id="how-block">
      <div class="how-block-container" :style="'height:' + windowHeight + 'px'" @mouseenter="pause(0)">
        <div class="col" v-for="c in 5" :key="c">
          <div class="col-container" :style="(c % 2 === 0) ? 'transform: translate(0, ' + cardImagesTranslate1 + '%)' : 'transform: translate(0, ' + cardImagesTranslate2 + '%)'">
            <div class="card-img-wrapper" v-for="(item, i) in cardImages" :key="i">
              <v-img class="card-img" :src="'/static/img/cards-img/' + item" contain></v-img>
            </div>
          </div>
        </div>
      </div>
      <div class="how-title-wrapper">
        <h1 class="how-title">Годнохаб — это...</h1>
      </div>
      <div class="how-info">
        <span style="padding-left: 1rem">Когда</span
        ><div
          class="changing"
          @mouseenter="pause(1)"><span
          :style="'transform: rotate(' + rotate1 + 'deg); background: ' + color1"
          >{{text1[actualText1]}}</span></div
        ><span>, что</span
        ><div
          class="changing"
          @mouseenter="pause(2)"><span
          :style="'transform: rotate(' + rotate2 + 'deg); background: ' + color2"
          >{{text2[actualText2]}}</span>.</div>
          <v-icon class="mobile-hint" color="white" @click="pause(12)">mdi-gesture-tap</v-icon>
      </div>
    </div>
    <div class="card-block" :style="'height:' + (windowHeight / 2) + 'px'">
      <h1 class="card-h1">Единица годноты</h1>
      <random-card></random-card>
    </div>
    <div class="collections-block" id="collections-block" :style="'min-height:' + windowHeight + 'px'">
      <h1 class="card-h1">Cлучайные коллекции пользователей</h1>
      <div>
        <random-collections></random-collections>
      </div>
    </div>
    <footer :style="'height:' + windowHeight + 'px'">
      <div class="actions-block last-block">
        <div class="action-wrapper">
          <login>
            <template v-slot:login-link><span></span></template>
            <template v-slot:registration-link>
              <v-btn outlined color="#4D9C6B">
                Создать свою коллекцию
              </v-btn>
            </template>
          </login>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
  import Login from './Login'

  function getRandomIntInclusive (min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min + 1)) + min
  }

  export default {
    name: 'MainPage',
    components: { Login },
    data () {
      return {
        titleImg: 0,
        titleImages: ['1-min.jpg', '2-min.jpg', '3-min.jpg', '4-min.jpg', '5-min.jpg', '6-min.jpg', '7-min.jpg', '8-min.jpg',
          '9-min.jpg', '10-min.jpg', '11-min.jpg', '12-min.jpg', '13-min.jpg', '14-min.jpg', '1-min.jpg'],
        titlePause: false,
        titleImgLoaded: false,
        windowHeight: 0,
        cardImages: ['1.png', '2.png', '3.png', '4.png', '1.png', '2.png', '3.png', '4.png',
          '1.png', '2.png', '3.png', '4.png'],
        paused1: false,
        paused2: false,
        color1: '',
        color2: '',
        colors: ['#FF206E', '#41EAD4', '#E6AF2E', '#06D6A0', '#9BC53D', '#4D9C6B', '#5BC0EB', '#F64740', '#3772FF', '#FF8300'],
        cardImagesTranslate1: -50,
        cardImagesTranslate2: -50,
        text1: ['не знаешь', 'думаешь', 'фантазируешь', 'сомневаешься', 'знаешь', 'ищешь',
          'рекомендуешь', 'спрашиваешь', 'выбираешь'],
        text2: ['посмотреть', 'почитать', 'послушать', 'узнать', 'попробовать', 'исследовать'],
        textCounter1: 0,
        textCounter2: 10,
        rotate1: 10,
        rotate2: 0,
        actualText1: 0,
        actualText2: 0,
        transitionKey: 0,
        eyeEls: [{}, {}, {}],
        eyeStatus: false
      }
    },
    methods: {
      titleImgPause (command) {
        if (command) {
          this.titlePause = true
        } else {
          this.titlePause = false
          this.changePicture()
        }
      },
      imgLoaded () {
        this.titleImgLoaded = true
        this.changePicture()
      },
      changePicture () {
        if (!this.titlePause) {
          setTimeout(() => {
            if (!this.titlePause && this.titleImgLoaded) {
              this.titleImgLoaded = false
              this.titleImg += 1
            }
            if (this.titleImg >= this.titleImages.length - 1) { this.titleImg = 0 }
          }, 500)
        }
      },
      eyesChanger () {
        let windowPart = window.innerWidth / this.eyeEls.length
        for (let i = 0; i < this.eyeEls.length; i++) {
          this.eyeEls[i] = {
            top: getRandomIntInclusive(10, this.windowHeight),
            left: getRandomIntInclusive((windowPart * i), ((windowPart * (i + 1)) - 120)),
            width: getRandomIntInclusive(30, 120)
          }
        }
        setInterval(() => {
          if (this.eyeStatus) {
            for (let i = 0; i < this.eyeEls.length; i++) {
              this.eyeEls[i] = {
                top: getRandomIntInclusive(10, this.windowHeight),
                left: getRandomIntInclusive((windowPart * i), ((windowPart * (i + 1)) - 120)),
                width: getRandomIntInclusive(30, 120)
              }
            }
          }
        }, 500)
      },
      pause (command) {
        if (command === 1) {
          this.paused1 = true
          this.color1 = this.colors[Math.floor(Math.random() * this.colors.length)]
        } else if (command === 2) {
          this.paused2 = true
          this.color2 = this.colors[Math.floor(Math.random() * this.colors.length)]
        } else if (command === 0 && this.paused1 && this.paused2) {
          this.paused1 = false
          this.paused2 = false
          this.color1 = ''
          this.color2 = ''
        } else if (command === 12) {
          if (this.paused1 && this.paused2) {
            this.pause(0)
          } else {
            this.pause(1)
            this.pause(2)
          }
        }
      },
      handleResize () {
        this.windowHeight = window.innerHeight
      },
      handleScroll () {
        let end = this.windowHeight * 3
        let scroll = window.scrollY
        if (scroll <= end) {
          this.cardImagesTranslate1 = -80 + (((scroll / end) * 100) / 1.7)
          this.cardImagesTranslate2 = -20 - (((scroll / end) * 100) / 1.3)
        }
      },
      textChanger () {
        setInterval(() => {
          if (!this.paused1) { this.textCounter1 += 1 }
          if (!this.paused2) { this.textCounter2 += 1 }
          if (this.textCounter1 >= 2) {
            this.actualText1 += 1
            this.textCounter1 = 0
            this.rotate1 = getRandomIntInclusive(-7, 7)
          }
          if (this.textCounter2 >= 2) {
            this.actualText2 += 1
            this.textCounter2 = 0
            this.rotate2 = getRandomIntInclusive(-7, 7)
          }
          this.actualText1 = (this.actualText1 >= this.text1.length) ? 0 : this.actualText1
          this.actualText2 = (this.actualText2 >= this.text2.length) ? 0 : this.actualText2
        }, 100)
      }
    },
    created () {
      window.addEventListener('resize', this.handleResize)
      window.addEventListener('scroll', this.handleScroll)
      this.handleResize()
      this.textChanger()
      this.eyesChanger()
    },
    destroyed () {
      window.removeEventListener('resize', this.handleResize)
      window.addEventListener('scroll', this.handleScroll)
    }
  }
</script>

<style scoped>
  .header-space {
    height: 3rem;
  }

  .first-block {
    height: 20rem;
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Roboto', sans-serif;
  }

  .title-block {
    width: 100%;
    height: 80%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .title-block-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    padding-top: 0.1rem;
    background: white;
  }

  .title-block p {
    margin: 0;
  }

  .title-image-wrapper {
    margin-top: 0.9rem;
    margin-right: 1.5rem;
    height: 9.7rem;
    width: 6.3rem;
    border-top: 5px solid black;
    border-left: 5px solid black;
    padding-left: 3px;
    padding-top: 3px;
  }

  .title-image-container {
    height: 100%;
    background: #4D9C6B;
    position: relative;
  }

  .title-back-img {
    transition: all 0.3s ease-out;
    position: absolute;
    top: 0;
    left: 0;
  }

  .pre-loaded {
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
  }

  .invisible {
    transition: all 0.3s ease-out;
    opacity: 0;
  }

  .actions-block {
    display: flex;
    justify-content: center;
    padding: 0 1rem;
    width: 100%;
  }

  .action-wrapper {
    padding: 0 1rem;
    position: relative;
  }

  .wrapper-back {
    background: #000000;
  }

  .action-link {
    color: #ffffff;
    cursor: pointer;
    z-index: 3;
  }

  .action-link:hover {
    text-decoration: underline;
  }

  .img-how {
    position: absolute;
    bottom: 100%;
    left: 0;
    transform: translate(-121%, 18%) rotate(-45deg);
    width: 0;
    z-index: 5;
    transition: 0.3s all;
  }

  .how-link:hover .img-how{
    width: 13rem;
    transform: translate(-121%, 18%) rotate(-45deg);
  }

  .img-vortex {
    position: absolute;
    left: 100%;
    top: 50%;
    width: 0;
    transform: translate(0, -100%) rotate(-45deg);
    z-index: 5;
    transition: 0.3s all;
  }

  .vortex-link:hover .img-vortex {
    width: 33rem;
    transform: translate(-68px, -100%) rotate(-45deg);
  }

  .img-eye {
    position: absolute;
    opacity: 0.3;
  }

  .img-eye-none {
    display: none;
  }

  .how-block {
    width: 100%;
    background: white;
    position: relative;
    overflow: hidden;
    font-family: 'Roboto', sans-serif;
  }

  .col {
    padding: 0;
    min-width: 21rem;
    position: relative;
  }

  .col-container {
    position: absolute;
    top: 50%;
  }

  .how-block-container {
    width: 120%;
    overflow: hidden;
    display: flex;
    transform: translate(-5rem, 0)
  }

  .card-img-wrapper {
    width: 25rem;
  }

  .card-img {
    perspective: 33rem;
    transform: rotateX(30deg) rotateY(-30deg);
  }

  .how-title-wrapper {
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .how-title {
    font-size: 1.8rem;
    position: relative;
    color: black;
    padding: 0 0.5rem;
  }

  .how-info {
    position: absolute;
    padding: 0;
    top: 55%;
    left: 50%;
    width: 90%;
    transform: translate(-50%, -50%);
    font-size: 3.3rem;
    color: white;
  }

  .how-info span {
    background: #000;
    display: inline-block;
    padding: 0 1rem;
  }

  div.changing {
    display: inline-block;
    background: #000;
    min-width: 26rem;
    cursor: default;
  }

  .changing span {
    background: none;
  }

  .mobile-hint {
    background: #000;
    display: none;
  }

  .card-block {
    margin-top: 3rem;
    margin-bottom: 5rem;
    min-height: 37rem;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: 'Roboto', sans-serif;
  }

  .card-h1 {
    font-size: 1.7rem;
    margin-bottom: 3rem;
    font-weight: 200;
  }

  .collections-block {
    padding-top: 3rem;
    position: relative;
    background: white;
    font-family: 'Roboto', sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  footer {
    height: 9rem;
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: 'Roboto', sans-serif;
    margin-bottom: 3rem;
  }

  .last-block {
    justify-content: center;
  }

  @media screen and (max-width: 1000px) {
    .img-vortex, .img-how, .img-eye {
      display: none;
    }
  }

  @media screen and (max-width: 600px) {
    .card-img-wrapper {
      width: 13rem;
    }

    .col {
      padding: 0;
      min-width: 10rem;
    }

    .how-title {
      font-size: 1rem;
    }

    .how-info {
      font-size: 1.7rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    div.changing {
      min-width: 0;
      display: block;
      width: fit-content;
    }

    .mobile-hint {
      display: block;
    }

    .card-block {
      height: auto !important;
    }
  }
</style>
