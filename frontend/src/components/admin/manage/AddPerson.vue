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
            <el-form-item label="角色">
              <el-select v-model="role" placeholder="选择角色">
                <el-option label="工作人员" value="工作人员"></el-option>
                <el-option label="老人" value="老人"></el-option>
                <el-option label="义工" value="义工"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="工作人员姓名"  v-if="role==='工作人员'">
              <el-input v-model="stuffform.name"></el-input>
            </el-form-item>
            <el-form-item label="性别"  v-if="role==='工作人员'">
              <el-input v-model="stuffform.gender"></el-input>
            </el-form-item>
            <el-form-item label="年龄"  v-if="role==='工作人员'">
              <el-input v-model="stuffform.age"></el-input>
            </el-form-item>
            <el-form-item label="身份证号码"  v-if="role==='工作人员'">
              <el-input v-model="stuffform.idcard"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone" v-if="role==='工作人员'">
              <el-input v-model="stuffform.phone"></el-input>
            </el-form-item>
            <el-form-item label="注册时间" v-if="role==='工作人员'">
              <el-date-picker
                v-model="stuffform.regdate"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>

            <el-form-item label="老人姓名" v-if="role==='老人'">
              <el-input v-model="olderform.name"></el-input>
            </el-form-item>
            <el-form-item label="性别"  v-if="role==='老人'">
              <el-input v-model="olderform.gender"></el-input>
            </el-form-item>
            <el-form-item label="年龄" v-if="role==='老人'">
              <el-input v-model="olderform.age"></el-input>
            </el-form-item>
            <el-form-item label="身份证号码" v-if="role==='老人'">
              <el-input v-model="olderform.idcard"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone" v-if="role==='老人'">
              <el-input v-model="olderform.phone"></el-input>
            </el-form-item>
            <el-form-item label="房间号" v-if="role==='老人'">
              <el-input v-model="olderform.room"></el-input>
            </el-form-item>
            <el-form-item label="第一联系人姓名" v-if="role==='老人'">
              <el-input v-model="olderform.r1name"></el-input>
            </el-form-item>
            <el-form-item label="第一联系人手机号" v-if="role==='老人'">
              <el-input v-model="olderform.r1phone"></el-input>
            </el-form-item>
            <el-form-item label="第二联系人姓名" v-if="role==='老人'">
              <el-input v-model="olderform.r2name"></el-input>
            </el-form-item>
            <el-form-item label="第二联系人手机号" v-if="role==='老人'">
              <el-input v-model="olderform.r2phone"></el-input>
            </el-form-item>
            <el-form-item label="注册时间" v-if="role==='老人'">
              <el-date-picker
                v-model="olderform.regdate"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="健康状态" prop="phone" v-if="role==='老人'">
              <el-input v-model="olderform.health"></el-input>
            </el-form-item>

            <el-form-item label="义工姓名"  v-if="role==='义工'">
              <el-input v-model="volunteerform.name"></el-input>
            </el-form-item>
            <el-form-item label="性别" v-if="role==='义工'">
              <el-input v-model="volunteerform.gender"></el-input>
            </el-form-item>
            <el-form-item label="年龄" v-if="role==='义工'">
              <el-input v-model="volunteerform.age"></el-input>
            </el-form-item>
            <el-form-item label="身份证号码" v-if="role==='义工'">
              <el-input v-model="volunteerform.idcard"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone" v-if="role==='义工'">
              <el-input v-model="volunteerform.phone"></el-input>
            </el-form-item>
            <el-form-item label="注册时间" v-if="role==='义工'">
              <el-date-picker
                v-model="volunteerform.regdate"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd">
              </el-date-picker>
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
  name: 'AddPerson',
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
      role: '工作人员',
      hasFace: false,
      uploadURL: this.localAPI + 'admin/uploadface',
      imgSrc: require('../../../assets/img3.jpg'),
      licenseImageUrl: '',
      stuffform: {
        name: '',
        phone: '',
        age: '',
        idcard: '',
        gender: '',
        regdate: '',
        file: ''
      },
      olderform: {
        name: '',
        phone: '',
        age: '',
        idcard: '',
        gender: '',
        regdate: '',
        r1name: '',
        r1phone: '',
        r2name: '',
        r2phone: '',
        health: '',
        room: '',
        file: ''
      },
      volunteerform: {
        name: '',
        phone: '',
        age: '',
        idcard: '',
        gender: '',
        regdate: '',
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
      if (this.role === '老人') {
        this.olderform.file = file
      } else if (this.role === '义工') {
        this.volunteerform.file = file
      } else if (this.role === '工作人员') {
        this.stuffform.file = file
      }
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
      let idcard = ''
      let f = ''
      if (this.role === '老人') {
        idcard = this.olderform.idcard
        f = this.olderform.file.raw
      } else if (this.role === '义工') {
        idcard = this.volunteerform.idcard
        f = this.volunteerform.file.raw
      } else if (this.role === '工作人员') {
        idcard = this.stuffform.idcard
        f = this.stuffform.file.raw
      }
      formData.append('idcard', idcard)
      formData.append('img', f)
      console.log(formData.get('idcard'))
      console.log(formData.get('img'))
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
      let regURL = ''
      if (this.role === '老人') {
        formData.append('name', this.olderform.name)
        formData.append('phone', this.olderform.phone)
        formData.append('age', this.olderform.age)
        formData.append('idcard', this.olderform.idcard)
        formData.append('gender', this.olderform.gender)
        formData.append('regdate', this.olderform.regdate)
        formData.append('r1name', this.olderform.r1name)
        formData.append('r1phone', this.olderform.r1phone)
        formData.append('r2name', this.olderform.r2name)
        formData.append('r2phone', this.olderform.r2phone)
        formData.append('health', this.olderform.health)
        formData.append('room', this.olderform.room)
        regURL = this.localAPI + 'admin/addo'
      } else if (this.role === '义工') {
        formData.append('name', this.volunteerform.name)
        formData.append('phone', this.volunteerform.phone)
        formData.append('age', this.volunteerform.age)
        formData.append('idcard', this.volunteerform.idcard)
        formData.append('gender', this.volunteerform.gender)
        formData.append('regdate', this.volunteerform.regdate)
        regURL = this.localAPI + 'admin/addv'
      } else if (this.role === '工作人员') {
        formData.append('name', this.stuffform.name)
        formData.append('phone', this.stuffform.phone)
        formData.append('age', this.stuffform.age)
        formData.append('idcard', this.stuffform.idcard)
        formData.append('gender', this.stuffform.gender)
        formData.append('regdate', this.stuffform.regdate)
        regURL = this.localAPI + 'admin/adds'
      }
      console.log(formData.get('idcard'))
      axios.post(regURL, formData, {'headers': this.headers}).then(res => {
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
