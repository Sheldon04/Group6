// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import '../theme/index.css'
import axios from 'axios'
import api from './router/api'
import 'videojs-flash'
import * as echarts from 'echarts'
import fabric from 'fabric'
Vue.prototype.echarts = echarts
Vue.use(fabric)

Vue.use(ElementUI)
Vue.prototype.$http = axios
Vue.prototype.localAPI = api.localAPI
Vue.prototype.localMedia = api.localMedia

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

router.beforeEach((to, from, next) => {
  console.log(localStorage.getItem('token'))
  // 先判断浏览器中是否已经有token了，有则true，否则false
  const isLogin = localStorage.getItem('token')
  // 然后判断要去往的页面，如果是去往login页面的，就直接放行
  // 如果不是去往login和register页面，则判断有没有token，如果有token就放行，否则就跳转login页面
  if (to.path === '/') {
    next(true)
  } else {
    if (isLogin) {
      if (from.fullPath === '/') {
        next(true)
      } else if (to.fullPath.split('/')[1] !== from.fullPath.split('/')[1]) {
        next(false)
      } else {
        next(true)
      }
    } else {
      next('/')
    }
  }
})
