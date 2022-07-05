<template>
  <div>
    <div>
      <el-container>
        <el-header class="header">
          <banner></banner>
        </el-header>
        <el-aside width="200px" class="side">
          <my-dropdown></my-dropdown>
          <my-sidnav-user></my-sidnav-user>
        </el-aside>
        <el-main class="main">
          <img style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" src="http://127.0.0.1:8000/api/video" width="1080" height="720">
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../public/Dropdown'
import MySidnavUser from '../public/SideNavUser'
import Banner from '../public/Banner'
export default {
  name: 'MonitorAdmin',
  components: {Banner, MySidnavUser, MyDropdown},
  data () {
    return {
      imgSrc: require('../../assets/img3.jpg')
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.el-menu {
  width: 200px;
  height: 800px;
}

.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}
.side {
  top: 100px;
}
.main {
  left: 250px;
  top: 130px;
  position: absolute;
}
</style>
