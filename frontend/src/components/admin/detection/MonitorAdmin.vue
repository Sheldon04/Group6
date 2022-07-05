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
         <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://10.166.155.20:8081/video" width="1080" height="720">
       </el-main>
     </el-container>
   </div>
 </div>
</template>

<script>
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'
export default {
  name: 'MonitorAdmin',
  components: {Banner, MySidenavAdmin, MyDropdown},
  data () {
    return {
      imgSrc: require('../../../assets/img3.jpg')
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
