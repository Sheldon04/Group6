<template>
  <div>
    <el-dropdown class="user-menu" placement="bottom-start">
  <span class="el-dropdown-link">
    <el-avatar shape="square" :size="80" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
    <i class="el-icon-arrow-down el-icon--right"></i>
  </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item split-button @click.native="personal_info">个人信息</el-dropdown-item>
        <el-dropdown-item split-button @click.native="changepass">修改密码</el-dropdown-item>
        <el-dropdown-item split-button @click.native="logout">注销</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <el-dialog v-loading="loading" title="个人信息" :visible.sync="dialogPersonInfoVisible" width="600px">
      <el-table
        :show-header="false"
        :data="statDatas"
        :span-method="objectSpanMethod"
        :cell-style="columnStyle"
        style="width: 100%; margin-top: 20px">
        <el-table-column prop="key"></el-table-column>
        <el-table-column prop="value"></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPersonInfoVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="修改密码" :visible.sync="dialogChangePassVisible">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'my-dropdown',
  data () {
    let validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    let validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      loading: true,
      dialogPersonInfoVisible: false,
      dialogChangePassVisible: false,
      statDatas: [],
      ruleForm: {
        pass: '',
        checkPass: ''
      },
      rules: {
        pass: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    personal_info () {
      console.log(localStorage.getItem('username'))
      let formData = new FormData()
      formData.append('username', localStorage.getItem('username')) // 2021-7-10
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/admin/getuserbyname', formData, {'headers': header}).then(response => {
        this.loading = true
        console.log(response.data)
        this.statDatas = response.data
        this.loading = false
        this.dialogPersonInfoVisible = true
      })
    },
    logout () {
      localStorage.removeItem('token')
      this.$router.push('/')
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('username', localStorage.getItem('username')) // 2021-7-10
          formData.append('password', this.ruleForm.pass) // 2021-7-10
          const auth = 'Token ' + localStorage.getItem('token')
          const header = {'Authorization': auth}
          axios.post('http://127.0.0.1:8000/api/changepass', formData, {'headers': header}).then(response => {
            console.log(response.data)
            if (response.data.result) {
              this.$message({
                message: '修改密码成功',
                type: 'success'
              })
              this.logout()
            } else {
              this.$message.error(response.data.errorInfo)
            }
          })
        } else {
          this.$message({
            message: '输入不合法，请检查您的输入',
            type: 'warning'
          })
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    changepass () {
      this.dialogChangePassVisible = true
    }
  }
}
</script>

<style scoped>
.user-menu {
  left: 50px;
  top: -5px;
}
</style>
