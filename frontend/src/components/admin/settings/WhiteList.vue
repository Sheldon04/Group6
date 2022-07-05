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
            v-loading = 'loading'
            class="main_table"
            :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize).filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
            stripe
            style="width: 1200px"
            :default-sort = "{prop: 'id', order: 'descending'}">
            <el-table-column
              prop="id"
              label="ID"
              type="index"
              sortable>
            </el-table-column>
            <el-table-column
              prop="name"
              label="姓名"
              width="120"
              align="center">
            </el-table-column>
            <el-table-column
              prop="phone_number"
              label="手机号"
              width="140"
              align="center">
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
              label="权限信息"
              prop="level"
              width="120"
              align="center">
            </el-table-column>
            <el-table-column
              label="最早进入"
              prop="time_start"
              width="140"
              align="center">
            </el-table-column>
            <el-table-column
              label="最晚离开"
              prop="time_end"
              width="140"
              align="center">
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
                  @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
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
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="phone_number">
            <el-input v-model="editForm.phone_number" auto-complete="off" disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="权限">
            <el-select v-model="editForm.level" placeholder="权限">
              <el-option label="高(3)" value="3"></el-option>
              <el-option label="中(2)" value="2"></el-option>
              <el-option label="低(1)" value="1"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="准入时间">
            <el-time-picker
              is-range
              v-model="editForm.timespan"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              placeholder="选择时间范围"
              value-format="HH:mm:ss">
            </el-time-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="handleCancel('editForm')">取消</el-button>
          <el-button type="primary" @click.native="handleUpdate('editForm')">更新</el-button>
        </div>
      </el-dialog>
      <el-dialog title="人脸照片更新"
                 :visible.sync="editFormVisible_face"
                 :close-on-click-modal="false"
                 class="edit-face"
                 @close="faceUploadClose">
        <el-form>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editName" auto-complete="off" disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="phone_number">
            <el-input v-model="editPhone" auto-complete="off" disabled="true"></el-input>
          </el-form-item>
        </el-form>
        <el-upload
          class="avatar-uploader"
          :limit="1"
          :action="updateFaceURL"
          :headers="headers"
          :on-remove="removeChange"
          :on-error="uploadError"
          :on-change="fileChange"
          :before-upload="beforeAvatarUpload"
          :auto-upload="false"
          align="center">
          <img v-if="newLicenseImageUrl" :src="newLicenseImageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible_face = false">取消</el-button>
          <el-button type="primary" @click.native="handleFaceUpload()">更新</el-button>
        </div>
      </el-dialog>
      <el-dialog
        title="警告"
        :visible.sync="confirmDialogVisible"
        width="30%"
        center>
        <span>确认删除白名单中的这一用户吗？</span>
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
  name: 'WhiteList',
  components: {Banner, MySidenavAdmin, MyDropdown},
  computed: {
    headers () {
      return {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    }
  },
  mounted () {
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': header}).then(response => {
      this.tableData = response.data
      this.loading = false
    })
    this.editForm.timespan = []
  },
  data () {
    return {
      editForm: {},
      editURL: this.localAPI + 'admin/whitelist/edit',
      editFormVisible: false, // 默认不显示编辑弹层
      delURL: this.localAPI + 'admin/whitelist/del',
      faceURL: this.localAPI + 'admin/getface',
      updateFaceURL: this.localAPI + 'admin/updateface',
      confirmDialogVisible: false,
      phone_to_delete: '',
      editPhone: '',
      editName: '',
      editFormVisible_face: false,
      file: '',
      seeDialogVisible: false,
      faceLoading: true,
      licenseImageUrl: '',
      newLicenseImageUrl: '',
      loading: true,
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      imgSrc: require('../../../assets/img3.jpg'),
      search: '',
      tableData: []
    }
  },
  methods: {
    // 点击编辑
    handleEdit (index, row) {
      this.editFormVisible = true
      row.timespan = []
      row.timespan.push(row.time_start)
      row.timespan.push(row.time_end)
      this.editForm = Object.assign({}, row) // 这句是关键！！！
      console.log(row.timespan)
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
      formData.append('name', this.editForm.name)
      formData.append('phone_number', this.editForm.phone_number)
      formData.append('time_span', this.editForm.timespan)
      formData.append('level', this.editForm.level)
      axios.post(this.editURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '编辑成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': this.headers}).then(response => {
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
      this.phone_to_delete = row.phone_number
    },
    handleDeleteConfirm () {
      this.confirmDialogVisible = false
      let formData = new FormData()
      formData.append('phone_number', this.phone_to_delete)
      console.log(this.phone_to_delete)
      axios.post(this.delURL, formData, {'headers': this.headers}).then(res => {
        const {result, errorInfo} = res.data
        if (result === true) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success'
          })
          this.loading = true
          axios.get('http://127.0.0.1:8000/api/admin/whitelist/all', {'headers': this.headers}).then(response => {
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
    handleSizeChange (val) {
      console.log(`每页 ${val} 条`)
      this.currentPage = 1
      this.pageSize = val
    },
    handleCurrentChange (val) {
      console.log(`当前页: ${val}`)
      this.currentPage = val
    },
    fileChange (file) {
      this.file = file
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
    handleFaceUploadOpen (index, row) {
      this.editFormVisible_face = true
      this.editPhone = row.phone_number
      this.editName = row.name
    },
    handleFaceUpload () {
      let formData = new FormData()
      formData.append('phone_number', this.editPhone)
      formData.append('face', this.file.raw)
      console.log(formData.get('face'))
      console.log(formData.get('phone_number'))
      axios.post(this.updateFaceURL, formData, {'headers': this.headers}).then(res => {
        this.$message.success('上传成功')
        this.newLicenseImageUrl = this.localMedia + res.data
        console.log(this.newLicenseImageUrl)
        // eslint-disable-next-line handle-callback-err
      }).catch(err => {
        this.$message.error('上传失败')
      })
    },
    handleFace (index, row) {
      this.faceLoading = true
      this.seeDialogVisible = true
      let formData = new FormData()
      formData.append('phone_number', row.phone_number)
      console.log(formData.get('phone_number'))
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
    faceClose () {
      this.seeDialogVisible = false
      this.licenseImageUrl = ''
    },
    faceUploadClose () {
      this.editFormVisible_face = false
      this.file = ''
      this.newLicenseImageUrl = ''
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
