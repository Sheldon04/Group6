/* eslint-disable */
<template>
  <div>
  <h1>Welcome</h1>
    <div class="background">
      <span>WatchDogs</span>
    </div>
    <div>
      <footer id="footer" style="width: 100%; height: 150px">
        <table>
          <tr>
            <td width="900px"></td>
            <td rowspan="3" style="text-align: left">
              <p>·Copyright © 2021 WatchDogs.All rights reserved.</p>
              <p>·© 2021 WatchDogs.All rights reserved.</p>
              <p>·© 2021 WatchDogs.版权所有。</p>
            </td>
          </tr>
          <tr>
            <td style="text-align: center"><el-button type="text" style="font-size: larger;color: white" @click="aboutUs">关于我们</el-button></td>
          </tr>
          <tr>
            <td style="text-align: center"><el-button type="text" style="font-size: larger;color: white" @click="contactUs">联系我们</el-button></td>
          </tr>
        </table>
      </footer>
    </div>
    <!--flex弹性盒子模型，justify-content：主抽 -->
    <div style="display: flex;justify-content: center;margin-top: 800px" class="mycard">
      <el-card style="width: 400px;background-color: transparent" id="el_card">
        <div slot="header" class="clearfix">
          <span>登录</span>
        </div>
        <table id="table_login">
          <tr>
<!--            <td>用户名</td>-->
            <td>
              <el-input v-model="user.username" placeholder="请输入用户名"></el-input>
            </td>
          </tr>
          <br>
          <tr>
<!--            <td>密码</td>-->
            <td>
              <el-input type="password" v-model="user.password" placeholder="请输入密码"
                        @keydown.enter.native="submitForm"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <br>
<!--          <tr>-->
<!--            <td colspan="2" id="choose">-->
<!--              <el-checkbox-group-->
<!--                v-model="checkedRoles"-->
<!--                :min="0"-->
<!--                :max="1">-->
<!--                <el-checkbox v-for="role in roles" :label="role" :key="role" style="margin: 3px 40px 5px 40px;color: white">{{ role }}</el-checkbox>-->
<!--              </el-checkbox-group>-->
<!--            </td>-->
<!--          </tr>-->
          <tr>
            <!-- 占两行-->
            <td colspan="2">
              <!-- 点击事件的两种不同的写法v-on:click和 @click-->
              <!--<el-button style="width: 300px" type="primary" v-on:click="doLogin">登录</el-button>-->
              <el-button style="width: 100%;background-color: snow;color: cornflowerblue" type="primary" @click="submitForm">登录</el-button>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <!--              <el-link href="https://element.eleme.io" target="_blank" style="width: 300px" >没有账号？注册</el-link>-->
              <el-button style="width: 300px" @click="register" type="text">没有账号？注册</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
    <!--    <div class="background">-->
    <!--      <img :src="imgSrc" width="100%" height="100%" alt="" />-->
    <!--    </div>-->
    <el-dialog title="注册新用户" :visible.sync="dialogRegisterVisible" width="600px" style="text-align: left">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style="border-radius: 100px">
        <el-form-item label="用户名" prop="username">
          <el-input type="text" v-model="ruleForm.username" suffix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="ruleForm.pass"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="ruleForm.checkPass"></el-input>
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input type="text" v-model="ruleForm.email" suffix-icon="el-icon-message" style="width: 350px"></el-input>
          <el-button @click="sendCode">验证码</el-button>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input type="text" v-model="ruleForm.code" style="width: 100px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button style="margin: 10px 80px 10px 40px" type="primary" @click="submitRegisterForm('ruleForm')">提交</el-button>
          <el-button style="margin: 10px 80px 10px 40px" @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>

</template>

<style>

h1 {
  position: absolute;
  text-align: center;
  width: 100%;
  letter-spacing: 10px;
  color: white;
  font-size: 12vw;
}
.background {
  background-image: url('../assets/mountain.jpg');
  background-size: cover;
  background-position: 50% 50%;
  height: 200vh;
  font: 900 16rem '';
  line-height: 130vh;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  text-align: center;
  overflow: hidden;

}

.background::before {
  content: '';
  background-size: cover;
  background-image: inherit;
  background-position: 50% 50%;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: -99;
}

.mycard {
  left: 38%;
  top: 10%;
  position: absolute;
  text-align: center;
  z-index: 99;
  background-color: transparent;

}

#table_login{
  text-align: center;
  width: 100%;
  background-color: transparent;
  height: 300px;
}

.clearfix {
  font-size: larger;
  font-weight: bold;
  height: 20px;
}

#choose {
  height: 30px;
}

#el_card {
  z-index: 2;
  background-position: center top;
  background-size: cover;
  overflow: hidden;
}

#el_card:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(218, 224, 223, 0.8);
  z-index: -1;
  background-image:url("../assets/mountain.jpg");
  background-position: center top;
  background-size: cover;
  background-attachment: scroll;
  -webkit-filter: blur(20px);
  -moz-filter: blur(20px);
  -ms-filter: blur(20px);
  -o-filter: blur(20px);
  filter: blur(20px);
  margin: -30px;
}

#footer {
  color: white;
  position: absolute;
  top: 1400px;
  z-index: 20;
  background-position: center top;
  background-size: cover;
  overflow: hidden;
}

#footer:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(200, 200, 200, 0.8);
  z-index: -1;
  background-image:url("../assets/mountain.jpg");
  background-position: center top;
  background-size: cover;
  background-attachment: fixed;
  -webkit-filter: blur(20px);
  -moz-filter: blur(20px);
  -ms-filter: blur(20px);
  -o-filter: blur(20px);
  filter: blur(20px);
}

</style>

<script>

import axios from 'axios'

export default {
  mounted () {
    window.addEventListener('scroll', this.handleScroll, true)
  },

  // 单页面中不支持前面的data:{}方式
  data () {
    let validateName = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入用户名'))
      } else {
        callback()
      }
    }
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
    // let validateEmail = (rule, value, callback) => {
    //   let regEmail = /^[A-Za-zd]+([-_.][A-Za-zd]+)*@([A-Za-zd]+[-.])+[A-Za-zd]{2,5}$/
    //   if (value === '') {
    //     callback(new Error('邮箱不能为空'))
    //   } else if (!regEmail.test(value)) {
    //     callback(new Error('邮箱格式不正确!'))
    //   } else {
    //     callback()
    //   }
    // }
    let validateCode = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('验证码不能为空'))
      } else {
        callback()
      }
    }
    const rolesOptions = ['用户', '管理员']
    // 相当于以前的function data(){},这是es5之前的写法，新版本可以省略掉function
    return {
      dialogRegisterVisible: false,
      user: {
        is_superuser: 0, // or 'admin'
        username: '',
        password: ''
        // 为了登录方便，可以直接在这里写好用户名和密码的值
      },
      checkedRoles: [],
      roles: rolesOptions,
      ruleForm: {
        username: '',
        email: '',
        pass: '',
        checkPass: '',
        code: '',
        validCode: ''
      },
      rules: {
        username: [
          {validator: validateName, trigger: 'blur'}
        ],
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ],
        email: [],
        code: [
          {validator: validateCode, trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    handleScroll: function () {
      const scrollY = window.scrollY
      const background = document.querySelector('.background')
      if (scrollY !== 0) {
        background.style.backgroundPosition = `calc(50% + ${scrollY}px) calc(50% + ${scrollY}px)`
      } else {
        background.style.backgroundPosition = ''
      }
    },
    aboutUs () {
      let { href } = this.$router.resolve({ path: '/aboutus' })
      window.open(href, '_blank')
    },
    contactUs () {
      let { href } = this.$router.resolve({ path: '/contactus' })
      window.open(href, '_blank')
    },
    async submitForm () {
      // if (this.checkedRoles.length !== 0 && this.checkedRoles[0] === '用户') {
      //   this.user.is_superuser = '0'
      //   console.log('????????????!!!!!!!!!!')
      // } else {
      //   this.user.is_superuser = '1'
      //   console.log('----------------------')
      // }
      this.user.is_superuser = '1'
      axios.post('http://127.0.0.1:8000/api/user/login', this.user).then(response => {
        const {result, detail, errorInfo} = response.data
        if (result === true) {
          // 登录成功
          // 设置token
          localStorage.setItem('token', detail.token)
          // 跳转页面
          if (this.user.is_superuser === '1') {
            this.$router.push('/admin/monitor')
          } else {
            this.$router.push('/user/monitor')
          }
          localStorage.setItem('username', this.user.username)
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
          console.log('?????????failed???????')
        }
      })
    },
    submitRegisterForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid && this.ruleForm.validCode === this.ruleForm.code) {
          let formData = new FormData()
          formData.append('username', this.ruleForm.username) // 2021-7-10
          formData.append('password', this.ruleForm.pass) // 2021-7-10
          formData.append('phone_number', this.ruleForm.phone_number) // 2021-7-10
          formData.append('email', this.ruleForm.email) // 2021-7-10
          const auth = 'Token ' + localStorage.getItem('token')
          const header = {'Authorization': auth}
          axios.post('http://127.0.0.1:8000/api/adduser', formData, {'headers': header}).then(response => {
            console.log(response.data)
            if (response.data.result) {
              this.$message({
                message: '注册成功',
                type: 'success'
              })
              this.dialogRegisterVisible = false
              this.ruleForm = ''
            } else {
              this.$message.error(response.data.errorInfo)
            }
          })
        } else {
          if (this.ruleForm.validCode !== this.ruleForm.code) {
            this.$message({
              message: '验证码错误',
              type: 'warning'
            })
          } else {
            this.$message({
              message: '输入不合法，请检查您的输入',
              type: 'warning'
            })
          }
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    register () {
      console.log('tt')
      this.dialogRegisterVisible = true
    },
    sendCode () {
      let code = ''
      for (let i = 0; i < 6; i++) {
        code += Math.floor(Math.random() * 10)
      }
      this.ruleForm.validCode = code
      let formData = new FormData()
      formData.append('code', code)
      formData.append('email', this.ruleForm.email)
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/sendemail', formData, {'headers': header}).then(response => {
        console.log(response.data)
        if (response.data.result) {
          this.$message({
            message: '发送成功',
            type: 'success'
          })
        } else {
          this.$message.error(response.data.errorInfo)
        }
      })
    }

  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll, true)
  }
}

</script>
