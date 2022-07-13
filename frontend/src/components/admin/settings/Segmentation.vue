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
          <el-tooltip class="item" effect="dark" content="数字越大表示该区域警戒等级越高" placement="top-end">
            <el-button>   区域警戒等级  </el-button>
          </el-tooltip>
          <el-select v-model="level" placeholder="警戒等级">
            <el-option label="高(3)" value="3"></el-option>
            <el-option label="中(2)" value="2"></el-option>
            <el-option label="低(1)" value="1"></el-option>
          </el-select>
          <el-button @click="addArea" type="primary" plain :disabled="isDisabled">添加一个区域</el-button>
          <el-button type="success" @click="submit" :disabled="!isDisabled">提交修改</el-button>
          <br>
          <br>
          <canvas id="canvas" width="1280" height="720"></canvas>
          <img class="cam1" width="1280" height="720" id="cam1" :src="camSrc1">
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import axios from 'axios'
import Banner from '../../public/Banner'
export default {
  name: 'Segmentation',
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  mounted () {
    // eslint-disable-next-line no-unused-vars,no-undef
    this.canvas = new fabric.Canvas('canvas')
    let imgElement = document.getElementById('cam1')
    // eslint-disable-next-line no-undef
    let imgInstance = new fabric.Image(imgElement, {
      left: 0,
      top: 0,
      angle: 0,
      opacity: 0.85
    })
    imgInstance.set('selectable', false)
    this.canvas.add(imgInstance)

    this.$notify({
      title: '提示',
      message: '单击画布开始划分区域',
      duration: 0
    })
  },
  components: {Banner, MySidenavAdmin, MyDropdown},
  data () {
    return {
      uploadURL: this.localAPI + 'admin/segmentation',
      canvas: '',
      rect: '',
      context: {},
      level: 3,
      imgSrc: require('../../../assets/img3.jpg'),
      camSrc1: require('../../../assets/camera1.jpg'),
      isDisabled: false
    }
  },
  methods: {
    addArea () {
      // eslint-disable-next-line no-unused-vars,no-undef
      this.rect = new fabric.Rect({
        top: 50, // 距离画布上边的距离
        left: 100, // 距离画布左侧的距离，单位是像素
        width: 100, // 矩形的宽度
        height: 70, // 矩形的高度
        fill: 'transparent', // 填充的颜色
        stroke: 'orange', // 边框原色
        strokeWidth: 1, // 边框大小
        rx: 8, // 圆角半径
        ry: 4 // 圆角半径
      })
      this.canvas.add(this.rect)
      this.isDisabled = true
      this.$notify({
        title: '提示',
        message: '添加下一个区域之前，请提交修改',
        duration: 0
      })
    },
    submit () {
      let formData = new FormData()
      let rect = this.canvas.getObjects()[1]
      formData.append('top', rect.aCoords.tl.y)
      formData.append('left', rect.aCoords.tl.x)
      formData.append('width', rect.aCoords.tr.x - rect.aCoords.tl.x)
      formData.append('height', rect.aCoords.bl.y - rect.aCoords.tl.y)
      console.log(rect.aCoords.tl.x)
      console.log(rect.aCoords.tl.y)
      console.log(rect.aCoords.tr.x)
      console.log(rect.aCoords.tr.y)
      console.log(rect.aCoords.br.x)
      console.log(rect.aCoords.br.y)
      console.log(rect.aCoords.bl.x)
      console.log(rect.aCoords.bl.y)
      axios.post(this.uploadURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('添加成功')
        this.licenseImageUrl = this.localMedia + res.data
        this.hasFace = true
        console.log(this.licenseImageUrl)
        // eslint-disable-next-line handle-callback-err
      }).catch(err => {
        this.$message.error('添加失败')
      })
    }
  }
}
</script>

<style scoped>
.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}
.main {
  left: 200px;
  top: 100px;
  position: absolute;
}

canvas {
  border: 1px dashed black;
}

.cam1 {
  display: none;
}
</style>
