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
          <el-form ref="form" :model="form" status-icon :rules="rules" label-width="130px" class="demo-form">
            <el-form-item label="注册人姓名">
              <el-input v-model="form.username"></el-input>
            </el-form-item>
            <el-form-item label="手机" prop="phone">
              <el-input v-model="form.phone"></el-input>
            </el-form-item>
            <el-form-item label="权限">
              <el-select v-model="form.level" placeholder="权限">
                <el-option label="高(3)" value="3"></el-option>
                <el-option label="中(2)" value="2"></el-option>
                <el-option label="低(1)" value="1"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="准入时间">
                <el-time-picker
                  is-range
                  v-model="form.timespan"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  placeholder="选择时间范围"
                  value-format="HH:mm:ss">
                </el-time-picker>
            </el-form-item>
            <el-form-item label="上传头像">
              <el-upload
                class="avatar-uploader"
                :limit="1"
                :action="uploadURL"
                :headers="headers"
                :on-remove="removeChange"
                :on-error="uploadError"
                :on-change="fileChange"
                :before-upload="beforeAvatarUpload"
                :auto-upload="false">
                <img v-if="licenseImageUrl" :src="licenseImageUrl" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
              </el-upload>
              <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitReg">立即注册</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'

export default {
  name: 'FaceRegistration',
  components: {Banner, MySidenavAdmin, MyDropdown},
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  data () {
    let validatePhone = (rule, value, callback) => {
      let reg = 11 && /^((13|14|15|17|18)[0-9]{1}\d{8})$/
      if (value === '') {
        callback(new Error('请输入手机号码'))
      } else {
        if (!reg.test(this.form.phone)) {
          callback(new Error('请输入正确的手机号码!'))
        }
        callback()
      }
    }
    return {
      hasFace: false,
      uploadURL: this.localAPI + 'admin/uploadface',
      regURL: this.localAPI + 'admin/whitelist/add',
      imgSrc: require('../../../assets/img3.jpg'),
      licenseImageUrl: '',
      form: {
        username: '',
        phone: '',
        area: '',
        timespan: ['00:00:00', '23:59:59'],
        level: '',
        file: ''
      },
      rules: {
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    fileChange (file) {
      this.form.file = file
    },
    beforeAvatarUpload (file) {
      // eslint-disable-next-line no-redeclare
      const isJPG = file.type === 'image/jpeg'
      const isLt10M = file.size / 1024 / 1024 < 10
      if (this.form.phone === '') {
        this.$message.error('请先输入手机号')
        return false
      }
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
    // eslint-disable-next-line handle-callback-err
    submitUpload () {
      let formData = new FormData()
      formData.append('phone', this.form.phone)
      formData.append('face', this.form.file.raw)
      console.log(formData.get('face'))
      console.log(formData.get('phone'))
      console.log(this.form.timespan)
      axios.post(this.uploadURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('上传成功')
        this.licenseImageUrl = this.localMedia + res.data
        this.hasFace = true
        console.log(this.licenseImageUrl)
        // eslint-disable-next-line handle-callback-err
      }).catch(err => {
        this.$message.error('上传失败')
      })
    },
    submitReg () {
      let formData = new FormData()
      formData.append('name', this.form.username)
      formData.append('phone_number', this.form.phone)
      formData.append('time_span', this.form.timespan)
      formData.append('level', this.form.level)
      console.log(formData.get('time_span'))
      console.log(formData.get('phone'))
      axios.post(this.regURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true && this.hasFace === true) {
          this.$message({
            showClose: true,
            message: '注册成功',
            type: 'success'
          })
        } else {
          let msg = errorInfo
          if (this.hasFace === false) {
            msg = '未上传人脸照片'
          }
          this.$message({
            showClose: true,
            message: msg,
            type: 'error'
          })
          console.log(formData.get('name'))
          console.log(formData.get('phone_number'))
          console.log(formData.get('time_span'))
        }
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
.demo-form {
  top: 25%;
  left: 30%;
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
