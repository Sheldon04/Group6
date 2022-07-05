<template>
  <div>
    <div>
      <el-container>
        <el-header class="header">
          <banner></banner>
        </el-header>
        <el-aside width="200px">
          <my-dropdown></my-dropdown>
          <my-sidnav-user></my-sidnav-user>
        </el-aside>
        <el-main class="main">
          <table>
            <tr>
              <td>按日期选择</td>
              <td>
                <el-date-picker
                  v-model="date"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions"
                  format="yyyy 年 MM 月 dd 日"
                  value-format="yyyy-MM-dd">
                </el-date-picker>
              </td>
              <td>按时间范围选择</td>
              <td>
                <el-time-picker
                  is-range
                  v-model="timespan"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  placeholder="选择时间范围"
                  value-format="HH:mm:ss">
                </el-time-picker>
              </td>
              <td>
                <el-button @click="search">查找</el-button>
              </td>
            </tr>
          </table>
          <br>
          <br>
          <el-table
            v-loading="loading"
            :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
            style="width: 1200px"
            :row-class-name="tableRowClassName">
            <el-table-column
              prop="date"
              label="日期"
              width="200"
              align="center">
              <template slot-scope="scope">
                <el-icon name="date"></el-icon>
                <span style="margin-left: 10px">{{ scope.row.date }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="time"
              label="时间"
              width="200"
              align="center">
              <template slot-scope="scope">
                <el-icon name="time"></el-icon>
                <span style="margin-left: 10px">{{ scope.row.time }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="level"
              label="报警级别"
              width="150"
              align="center">
            </el-table-column>
            <el-table-column
              prop="camera_id"
              label="摄像头"
              width="150"
              align="center">
            </el-table-column>
            <el-table-column
              prop="area"
              label="报警区域"
              width="150"
              align="center">
            </el-table-column>
            <el-table-column
              prop="invation_num"
              label="入侵数量"
              width="150"
              align="center">
            </el-table-column>
            <el-table-column
              fixed="right"
              label="操作"
              width="100"
              align="center">
              <template slot-scope="scope">
                <el-button @click="handleClick(scope.row)" type="text" size="small">查看详情</el-button>
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
      <el-dialog
        @close="detailClose"
        title="入侵详情"
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

<style scoped>
.main {
  left: 200px;
  top: 100px;
  position: absolute;
}
.el-menu {
  width: 200px;
  height: 800px;
}
</style>

<style>
.header {
  background-color: #A2BCC6FF;
  height: 100px !important;
}
.el-table .warning-row {
  background: #fbede5;
}

.el-table .common-row {
  background: #fbfbe5;
}
</style>

<script>
import axios from 'axios'
import MyDropdown from '../public/Dropdown'
import MySidnavUser from '../public/SideNavUser'
import Banner from '../public/Banner'
export default {
  name: 'AttackListAdmin',
  components: {Banner, MySidnavUser, MyDropdown},
  mounted () {
    const auth = 'Token ' + localStorage.getItem('token')
    const header = {'Authorization': auth}
    axios.get('http://127.0.0.1:8000/api/attacklistuser/all', {'headers': header}).then(response => {
      this.tableData = response.data
      this.loading = false
    })
  },
  methods: {
    async search () {
      // let keywords = []
      // keywords.push(this.date)
      // if (this.timespan.length !== 0) {
      //   keywords = keywords.concat(this.timespan)
      // }
      let formData = new FormData()
      formData.append('date', this.date) // 2021-7-10
      formData.append('time_span', this.timespan) // 8:00:15,9:00:00
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/attacklistuser', formData, {'headers': header}).then(response => {
        this.tableData = response.data
      })
      console.log(formData.get('date'))
      console.log(formData.get('time_span'))
    },
    tableRowClassName ({row, index}) {
      if (row.level === 3) {
        return 'warning-row'
      } else if (row.level === 2) {
        return 'common-row'
      }
      return ''
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
    handleClick (row) {
      this.detailVisible = true
      let date = row.date
      let time = row.time
      let formData = new FormData()
      formData.append('date', date)
      formData.append('time', time)
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/attacklistuser/detail', formData, {'headers': header}).then(response => {
        console.log(response.data)
        this.imgs = response.data
      })
    },
    detailClose () {
      this.detailVisible = false
      this.imgs = []
    }
  },
  data () {
    return {
      loading: true,
      currentPage: 1, // 当前页码
      total: 0, // 总条数
      pageSize: 10, // 每页的数据条数
      imgSrc: require('../../assets/img3.jpg'),
      options: [],
      date: '2021-7-21',
      timespan: ['00:00:00', '23:59:59'],
      tableData: [],
      detailVisible: false,
      imgs: [],
      pickerOptions: {
        disabledDate (time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: '今天',
          onClick (picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: '昨天',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: '一周前',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      }
    }
  }
}
</script>
