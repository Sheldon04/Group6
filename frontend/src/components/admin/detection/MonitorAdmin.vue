<template>
 <div>
   <div>
     <el-container>
       <el-header class="header">
         <banner></banner>
       </el-header>
       <el-aside width="200px">
         <my-dropdown></my-dropdown>
         <my-sidenav-admin></my-sidenav-admin>
       </el-aside>
       <el-main class="main">
           <el-select v-model="role" placeholder="选择监控">
             <el-option label="监控一" value="监控一"></el-option>
             <el-option label="监控二" value="监控二"></el-option>
             <el-option label="监控三" value="监控三"></el-option>
           </el-select>
<!--         <FlvLive width="1080" height="720" v-if="role==='监控一'" :url="url"></FlvLive>-->
         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://10.16.255.139:8081/video" width="1080" height="720" v-if="role==='监控一'">
<!--         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://10.166.155.20:8081/video" width="1080" height="720" v-if="role==='监控二'">-->
<!--         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://10.166.155.20:8081/video" width="1080" height="720" v-if="role==='监控三'">-->
<!--         <iframe src="http://admin:123456@192.168.0.3:8081/audio.opus" width="1080" height="720" v-if="role==='监控一'"></iframe>-->
<!--         <iframe src="https://blog.51cto.com/topic/vueyemianzhongqianruhtmlyemian.html" width="1080" height="720" v-if="role==='监控二'"></iframe>-->
<!--         <iframe src="https://blog.csdn.net/qq_45801837/article/details/121396196" width="1080" height="720" v-if="role==='监控三'"></iframe>-->
       </el-main>
     </el-container>
   </div>
 </div>
</template>

<script>
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'
import FlvLive from '../../public/FlvLive'
export default {
  name: 'MonitorAdmin',
  components: {FlvLive, Banner, MySidenavAdmin, MyDropdown},
  data () {
    return {
      imgSrc: require('../../../assets/img3.jpg'),
      role: '监控一',
      url: 'http://192.168.0.3:8081/live.flv'
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}
.submenu-title {
  font-size: 18px !important;
}

.main {
  left: 250px;
  top: 130px;
  position: absolute;
}

.user-menu {
  left: 50px;
  top: 5px;
}

</style>
