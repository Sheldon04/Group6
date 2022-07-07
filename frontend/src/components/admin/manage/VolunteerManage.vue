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
          <el-table
            v-loading="loading"
            :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize).filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
            stripe
            style="width: 1200px"
            :default-sort = "{prop: 'id', order: 'descending'}">
            <el-table-column
              prop="id"
              label="ID"
              width="60"
              align="center"
              sortable>
            </el-table-column>
            <el-table-column
              prop="name"
              label="姓名"
              width="150"
              align="center"
              sortable>
            </el-table-column>
            <el-table-column
              prop="gender"
              label="性别"
              width="100"
              align="center"
              sortable>
            </el-table-column>
            <el-table-column
              prop="age"
              label="年龄"
              width="100"
              align="center"
              sortable>
            </el-table-column>
            <el-table-column
              prop="face_info"
              label="人脸信息"
              width="120"
              align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" inline @click="handleFace(scope.$index, scope.row)">查看</el-button>
                <el-button type="text" size="small" inline @click="handleFaceUploadOpen(scope.$index, scope.row)">更新</el-button>
              </template>
            </el-table-column>
            <el-table-column
              prop="phone"
              label="手机号"
              align="center"
              width="200"
              sortable>
            </el-table-column>
            <el-table-column
              prop="regdate"
              label="注册日期"
              align="center"
              width="200"
              sortable>
            </el-table-column>
            <el-table-column
              align="center"
              width="300">
              <template slot="header" slot-scope="scope">
                <div>
                  <div class="search">
                    <el-input
                      v-model="search"
                      size="mini"
                      prefix-icon="el-icon-search"
                      placeholder="输入关键字搜索"/>
                  </div>
                  <div class="search"><el-button icon="el-icon-search" size="mini" circle></el-button></div>
                </div>
              </template>
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)">更多</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
                         :current-page="currentPage"
                         :page-sizes="[10,20,50,100]"
                         :page-size="pageSize"
                         layout="total, sizes, prev, pager, next, jumper"
                         :total="tableData.length">
          </el-pagination>
        </el-main>
      </el-container>
      <el-dialog title="编辑"
                 :visible.sync="editFormVisible"
                 :close-on-click-modal="false"
                 class="edit-form"
                 :before-close="handleClose">
        <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
          <el-form-item label="ID" prop="id">
            <el-input v-model="editForm.id" auto-complete="off" disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="first_name">
            <el-input v-model="editForm.gender" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="年龄" prop="last_name">
            <el-input v-model="editForm.age" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="email">
            <el-input v-model="editForm.phone" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="身份证号" prop="email">
            <el-input v-model="editForm.idcard" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="handleCancel('editForm')">取消</el-button>
          <el-button type="primary" @click.native="handleUpdate('editForm')">更新</el-button>
        </div>
      </el-dialog>
      <el-dialog
        title="警告"
        :visible.sync="confirmDialogVisible"
        width="30%"
        center>
        <span>确认删除这一用户吗？</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="confirmDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleDeleteConfirm">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog
        @close="faceClose"
        title="人脸照片"
        :visible.sync="seeDialogVisible"
        width="25%"
        center>
        <el-image
          style="width: 300px; height: 300px"
          :src="licenseImageUrl"
          :fit="fit"
          v-loading="faceLoading"></el-image>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'
export default {
  name: 'VolunteerManage',
  components: {Banner, MySidenavAdmin, MyDropdown},
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  mounted () {
    const url = 'http://127.0.0.1:8000/api/admin/getallv'
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get(url, {'headers': header}).then(response => {
      console.log(response.data.result)
      this.tableData = response.data
      this.loading = false
    })
  },
  data () {
    return {
      loading: true,
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      search: '',
      imgSrc: require('../../../assets/img3.jpg'),
      tableData: [],
      editForm: {},
      editFormVisible: false,
      id_to_delete: '',
      editURL: this.localAPI + 'admin/editv',
      delURL: this.localAPI + 'admin/delv',
      faceURL: this.localAPI + 'admin/getface',
      confirmDialogVisible: false,
      faceLoading: false,
      seeDialogVisible: false,
      editFormVisible_face: true,
      licenseImageUrl: '',
      newLicenseImageUrl: ''
    }
  },
  methods: {
    faceClose () {
      this.seeDialogVisible = false
      this.licenseImageUrl = ''
    },
    faceUploadClose () {
      this.editFormVisible_face = false
      this.file = ''
      this.newLicenseImageUrl = ''
    },
    handleFace (index, row) {
      this.faceLoading = true
      this.seeDialogVisible = true
      let formData = new FormData()
      formData.append('idcard', row.idcard)
      console.log(formData.get('idcard'))
      axios.post(this.faceURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('获取成功')
        this.licenseImageUrl = this.localMedia + res.data
        this.faceLoading = false
        console.log(this.licenseImageUrl)
        // eslint-disable-next-line handle-callback-err
      }).catch(err => {
        this.$message.error('获取失败')
      })
    },
    handleFaceUploadOpen (index, row) {
      this.editFormVisible_face = true
      // this.editPhone = row.phone_number
      // this.editName = row.name
    },
    // 点击编辑
    handleEdit (index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row) // 这句是关键！！！
    },
    // 点击关闭dialog
    handleClose (done) {
      /* done();
      location.reload(); */
      this.editFormVisible = false
    },
    // 点击取消
    handleCancel (formName) {
      this.editFormVisible = false
    },
    // 点击更新
    handleUpdate (forName) {
      // 更新的时候就把弹出来的表单中的数据写到要修改的表格中
      // var postData = {
      //   name: this.editForm.name;
      // }
      // 这里再向后台发个post请求重新渲染表格数据
      let formData = new FormData()
      formData.append('id', this.editForm.id)
      formData.append('name', this.editForm.name)
      formData.append('phone', this.editForm.phone)
      formData.append('age', this.editForm.age)
      formData.append('idcard', this.editForm.idcard)
      formData.append('gender', this.editForm.gender)
      formData.append('regdate', this.editForm.regdate)
      axios.post(this.editURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '编辑成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/getallv', {'headers': this.headers}).then(response => {
            this.tableData = response.data
            this.loading = false
          })
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
        }
      })
      this.editFormVisible = false
    },
    handleDelete (index, row) {
      this.confirmDialogVisible = true
      this.id_to_delete = row.id
    },
    handleDeleteConfirm () {
      this.confirmDialogVisible = false
      let formData = new FormData()
      formData.append('id', this.id_to_delete)
      console.log(this.id_to_delete)
      axios.post(this.delURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/getallv', {'headers': this.headers}).then(response => {
            this.tableData = response.data
            this.loading = false
          })
        } else {
          this.$message({
            showClose: true,
            message: errorInfo,
            type: 'error'
          })
        }
      })
    },
    formatter (row, index) {
      if (row.is_superuser === true) {
        row.Registrationstate = '是'
      }
      if (row.is_superuser === false) {
        row.Registrationstate = '否'
      }
      return row.Registrationstate
    },
    handleSizeChange (val) {
      console.log(`每页 ${val} 条`)
      this.currentPage = 1
      this.pageSize = val
    },
    handleCurrentChange (val) {
      console.log(`当前页: ${val}`)
      this.currentPage = val
    },
    filterHandler (value, row, column) {
      const property = column['property']
      return row[property] === value
    }
  }
}
</script>

<style scoped>
.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}

.submenu-title {
  font-size: 18px !important;
}

.main {
  left: 200px;
  top: 100px;
  position: absolute;
}

.user-menu {
  left: 50px;
  top: 5px;
}

.search {
  display: inline-block;
}

</style>
