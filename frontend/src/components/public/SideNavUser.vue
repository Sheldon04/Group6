<template>
  <el-menu
    :default-active=activeIndex
    class="el-menu-vertical-demo"
    @select="handleSelect">
    <el-menu-item index="/user/monitor">
      <i class="el-icon-camera"></i>
      <span slot="title">实时监控</span>
    </el-menu-item>
    <el-menu-item index="/user/traceback">
      <i class="el-icon-refresh"></i>
      <span slot="title">入侵回放</span>
    </el-menu-item>
    <el-menu-item index="/user/attacklist">
      <i class="el-icon-document"></i>
      <span slot="title">查看记录</span>
    </el-menu-item>
    <el-menu-item index="/user/attackinfo">
      <i class="el-icon-setting"></i>
      <span slot="title">入侵统计</span>
    </el-menu-item>
    <el-menu-item index="/user/deblur">
      <i class="el-icon-upload"></i>
      <span slot="title">模糊图像处理</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'my-sidnav-user',
  data () {
    return {
      activeIndex: this.$route.path
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      this.$router.push(key)
    }
  }
}
</script>

<style scoped>

</style>
