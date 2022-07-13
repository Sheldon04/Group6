<template>
  <div class="video" :style="{ height: voidHeight }">
    <video ref="videoElement" muted></video>
    <div class="img_error" v-if="imgError">
      <p>视频播放错误，请联系管理员！</p>
    </div>
  </div>
</template>

<script>
import flvjs from 'flv.js'
export default {
  name: 'FlvLive',
  props: ['url', 'height', 'destroy'], // 视频流路径，播放器高度，是否销毁播放器
  data () {
    return {
      flvPlayer: '',
      imgError: false,
      voidHeight: ''
    }
  },
  mounted () {
    // 判断是否传入高度，如果没有，高度100%
    this.height ? (this.voidHeight = this.height) : (this.voidHeight = '100%')
    // 页面加载完成后，初始化
    this.$nextTick(() => {
      this.init(this.url)
    })
  },
  methods: {
    // 初始化
    init (source) {
      if (flvjs.isSupported()) {
        this.flvPlayer = flvjs.createPlayer({
          type: 'flv',
          url: source,
          // url: 'https://mister-ben.github.io/videojs-flvjs/bbb.flv',
          duration: 6000,
          isLive: true, // 实时流
          hasAudio: false,
          hasVideo: true
        }, {
          cors: false, // 是否跨域
          enableStashBuffer: false,
          fixAudioTimestampGap: false,
          isLive: true,
          lazyLoad: true,
          autoCleanupSourceBuffer: true // 是否自动清理缓存
        })

        this.flvPlayer.attachMediaElement(this.$refs.videoElement)
        this.flvPlayer.load()
        this.flvPlayer.play()

        // 加载完成
        this.flvPlayer.on(flvjs.Events.LOADING_COMPLETE, () => {
          this.imgError = false
        })

        // 加载失败
        this.flvPlayer.on(
          flvjs.Events.ERROR,
          () => {
            this.imgError = true
          },
          (error) => {
            console.log(error)
          }
        )
      } else {
        this.imgError = true
      }
    },
    // 销毁
    detachMediaElement () {
      this.flvPlayer.pause()
      this.flvPlayer.unload()
      this.flvPlayer.detachMediaElement()
      this.flvPlayer.destroy()
      this.flvPlayer = ''
    }
  },
  watch: {
    url () {
      this.imgError = false
      // 切换流之前，判断之前的流是否销毁
      // eslint-disable-next-line no-unused-expressions
      this.flvPlayer === '' ? '' : this.detachMediaElement()
      // 初始化
      this.init(this.url)
    },
    destroy () {
      // 传入开关值
      if (this.destroy) {
        this.init(this.url)
      } else {
        // eslint-disable-next-line no-unused-expressions
        this.flvPlayer === '' ? '' : this.detachMediaElement()
      }
    }
  },
  beforeDestroy () {
    this.detachMediaElement()
  }
}
</script>

<style scoped>
.video {
  position: relative;
  height: 100%;
}
video {
  width: 100%;
  height: 100%;
  object-fit: fill;
}
.img_error {
  position: absolute;
  top: 30%;
  left: 50%;
  margin-left: -120px;
  text-align: center;
}
.img_error > img {
  margin-bottom: 1em;
}
.img_error > p {
  color: #00fdff;
  font-weight: bold;
  font-size: 1.2em;
}
</style>
