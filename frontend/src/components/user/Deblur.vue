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
          <el-tabs type="border-card" class="border-card1">
            <el-tab-pane>
              <span slot="label"><i class="el-icon-date"></i>提交工单</span>
              <el-upload
                class="avatar-uploader"
                :action="submitURL"
                :limit="1"
                :headers="headers"
                :on-remove="removeChange"
                :on-error="uploadError"
                :on-change="fileChange"
                :before-upload="beforeAvatarUpload"
                :auto-upload="false"
                align="center">
                <img v-if="licenseImageUrl" :src="licenseImageUrl" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                <div class="el-upload__tip" slot="tip">在此处上传需要处理的图片</div>
              </el-upload>
              <br>
              <el-input
                class="textarea"
                type="textarea"
                :rows="10"
                placeholder="在此处输入描述信息"
                v-model="textarea">
              </el-input>
              <br>
            </el-tab-pane>
            <el-button type="primary" @click="submit" class="submit-button">提交</el-button>
          </el-tabs>
          <el-table
            v-loading = 'loading'
            class="border-card2"
            :data="tableData"
            stripe
            :default-sort = "{prop: 'id', order: 'ascending'}">
            <el-table-column
              prop="id"
              label="ID"
              width="80"
              sortable>
            </el-table-column>
            <el-table-column
              prop="date"
              label="创建时间"
              width="160"
              sortable
              align="center">
            </el-table-column>
            <el-table-column
              label="状态"
              prop="status"
              width="160"
              align="center">
              <template slot-scope="scope">
                <span v-if="scope.row.status === 0">未完成</span>
                <span v-if="scope.row.status === 1">已完成</span>
              </template>
            </el-table-column>
            <el-table-column
              align="center"
              label="操作"
              width="160">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleSee(scope.$index, scope.row)">查看</el-button>
                <el-button
                  v-if="scope.row.status === 0"
                  size="mini"
                  @click="handleDownload(scope.$index, scope.row)"
                  disabled>下载</el-button>
                <el-button
                  v-if="scope.row.status === 1"
                  size="mini"
                  @click="handleDownload(scope.$index, scope.row)">下载</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
      <el-dialog
        @close="detailClose"
        title="工单详情"
        :visible.sync="detailVisible"
        center
        class="detail-dialog">
        <el-carousel style="width: 100%" :interval="5000" arrow="always">
          <el-carousel-item v-for="img in imgs" :key="img">
            <el-image
              style="width: 960px; height: 540px ; max-width: 100%; max-height: 100%;"
              :src="img"
            ></el-image>
          </el-carousel-item>
        </el-carousel>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../public/Dropdown'
import MySidnavUser from '../public/SideNavUser'
import Banner from '../public/Banner'
import axios from 'axios'
export default {
  name: 'Deblur',
  created () {
    axios.get('http://127.0.0.1:8000/api/deblur/gettasks', {'headers': this.headers}).then(response => {
      this.loading = true
      console.log(response.data)
      this.tableData = response.data
      this.loading = false
    })
  },
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  components: {Banner, MySidnavUser, MyDropdown},
  data () {
    return {
      submitURL: this.localAPI + 'deblur/submit',
      licenseImageUrl: '',
      textarea: '',
      tableData: [],
      loading: true,
      file: '',
      detailVisible: false,
      imgs: []
    }
  },
  methods: {
    // 图片下载
    download (href, name) {
      let eleLink = document.createElement('a')
      eleLink.download = name
      eleLink.href = href
      eleLink.click()
      eleLink.remove()
    },
    handleDownload (index, row) {
      let formData = new FormData()
      formData.append('id', row.id)
      console.log(formData.get('id'))
      axios.post('http://127.0.0.1:8000/api/deblur/download', formData, {'headers': this.headers}).then(res => {
        console.log(res.data.detail.url)
        let url = 'http://127.0.0.1:8000/media/' + res.data.detail.url
        let image = new Image()
        image.setAttribute('crossOrigin', 'anonymous')
        image.src = url
        image.onload = () => {
          let canvas = document.createElement('canvas')
          canvas.width = image.width
          canvas.height = image.height
          let ctx = canvas.getContext('2d')
          ctx.drawImage(image, 0, 0, image.width, image.height)
          canvas.toBlob((blob) => {
            let url = URL.createObjectURL(blob)
            this.download(url, name)
            // 用完释放URL对象
            URL.revokeObjectURL(url)
          })
        }
      })
    },
    fileChange (file) {
      this.file = file
    },
    beforeAvatarUpload (file) {
      // eslint-disable-next-line no-redeclare
      const isJPG = file.type === 'image/jpeg'
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt10M) {
        this.$message.error('上传头像图片大小不能超过 10MB!')
      }
      return isJPG && isLt10M
    },
    // eslint-disable-next-line handle-callback-err
    uploadError (err, file, filelist) {
      this.$message.error('上传失败')
    },
    removeChange (file, fileList) {
      console.log('你要移除的文件为', file.name)
    },
    submit () {
      let formData = new FormData()
      formData.append('token', localStorage.getItem('token'))
      formData.append('img', this.file.raw)
      console.log(formData.get('token'))
      console.log(formData.get('img'))
      axios.post(this.submitURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '提交成功',
            type: 'success'
          })
          axios.get('http://127.0.0.1:8000/api/deblur/gettasks', {'headers': this.headers}).then(response => {
            this.loading = true
            console.log(response.data)
            this.tableData = response.data
            this.loading = false
          })
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
          console.log(errorInfo)
        }
      })
    },
    handleSee (index, row) {
      this.detailVisible = true
      let formData = new FormData()
      formData.append('id', row.id)
      console.log(formData.get('id'))
      axios.post('http://127.0.0.1:8000/api/deblur/show', formData, {'headers': this.headers}).then(res => {
        console.log(res.data.detail.urls)
        this.imgs = res.data.detail.urls
      })
    },
    detailClose () {
      this.detailVisible = false
      this.imgs = []
    }
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
  width: 1200px;
  height: 680px;
  position: absolute;
}

.border-card1 {
  width: 400px;
  height: 620px;
  left: 10px;
  top: 20px;
  position: absolute;
}

.border-card2 {
  width: 600px;
  height: 600px;
  left: 500px;
  top: 20px;
  position: absolute;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
