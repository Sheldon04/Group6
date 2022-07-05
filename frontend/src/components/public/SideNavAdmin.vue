<template>
  <el-menu
    :default-active=activeIndex
    class="el-menu"
    @select="handleSelect">
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-view"></i>
        <span>入侵检测</span>
      </template>
      <el-menu-item index="/admin/monitor">
        <i class="el-icon-camera"></i>
        实时监控
      </el-menu-item>
      <el-menu-item index="/admin/traceback">
        <i class="el-icon-refresh"></i>
        入侵回放
      </el-menu-item>
      <el-menu-item index="/admin/attacklist">
        <i class="el-icon-document"></i>
        查看记录
      </el-menu-item>
      <el-menu-item index="/admin/attackinfo">
        <i class="el-icon-setting"></i>
        入侵统计
      </el-menu-item>
    </el-submenu>
    <el-submenu index="2">
      <template slot="title">
        <i class="el-icon-user"></i>
        <span>用户管理</span>
      </template>
      <el-menu-item index="/admin/facereg">
        <i class="el-icon-camera"></i>
        人脸识别注册
      </el-menu-item>
      <el-menu-item index="/admin/usermanage">
        <i class="el-icon-document"></i>
        用户信息管理
      </el-menu-item>
    </el-submenu>
    <el-submenu index="3">
      <template slot="title">
        <i class="el-icon-setting"></i>
        <span>监控设置</span>
      </template>
      <el-menu-item index="/admin/whitelist">
        <i class="el-icon-document-checked"></i>
        可信名单管理
      </el-menu-item>
      <el-menu-item index="/admin/segmentation">
        <i class="el-icon-crop"></i>
        监控区域划分
      </el-menu-item>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  name: 'my-sidenav-admin',
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
