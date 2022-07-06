<template>
  <el-menu
    :default-active=activeIndex
    class="el-menu"
    @select="handleSelect">
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-view"></i>
        <span>智能监控</span>
      </template>
      <el-menu-item index="/admin/monitor">
        <i class="el-icon-camera"></i>
        实时监控
      </el-menu-item>
      <el-menu-item index="/admin/traceback">
        <i class="el-icon-refresh"></i>
        监控回放
      </el-menu-item>
      <el-menu-item index="/admin/falllist">
        <i class="el-icon-document"></i>
        摔倒记录
      </el-menu-item>
      <el-menu-item index="/admin/emolist">
        <i class="el-icon-document"></i>
        情绪记录
      </el-menu-item>
      <el-menu-item index="/admin/interactionlist">
        <i class="el-icon-document"></i>
        互动记录
      </el-menu-item>
      <el-menu-item index="/admin/attacklist">
        <i class="el-icon-document"></i>
        闯入记录
      </el-menu-item>
      <el-menu-item index="/admin/unkownlist">
        <i class="el-icon-document"></i>
        陌生人记录
      </el-menu-item>
    </el-submenu>
    <el-submenu index="2">
      <template slot="title">
        <i class="el-icon-user"></i>
        <span>信息管理</span>
      </template>
      <el-menu-item index="/admin/stuffmanage">
        <i class="el-icon-document"></i>
        工作人员管理
      </el-menu-item>
      <el-menu-item index="/admin/volunteermanage">
        <i class="el-icon-document"></i>
        义工管理
      </el-menu-item>
      <el-menu-item index="/admin/oldermanage">
        <i class="el-icon-document"></i>
        老人管理
      </el-menu-item>
    </el-submenu>
    <el-submenu index="3">
      <template slot="title">
        <i class="el-icon-setting"></i>
        <span>监控管理</span>
      </template>
      <el-menu-item index="/admin/monitorinfo">
        <i class="el-icon-document-checked"></i>
        监控信息
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
