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
          <el-calendar v-loading="loading" :first-day-of-week=7>
            <template
              slot="dateCell"
              slot-scope="{date, data}">
              <div @click="handle_click(data.day.split('-'))">
                <p class="date_cell">{{ data.day.split('-').slice(1).join('-') }}</p>
                <el-popover
                  placement="right"
                  width="200"
                  trigger="click">
                  <el-table v-loading="dia_loading" :data="detail_invasion_data">
                    <el-table-column width="100" property="time" label="时间"></el-table-column>
                    <el-table-column label="操作">
                      <template slot-scope="scope">
                        <el-button
                          size="mini" type="text"
                          @click="handleSee(scope.$index, scope.row, data.day)">查看</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <div slot="reference" class="date_cell">
                    <el-badge v-if="parseInt(data.day.split('-')[1]) === cur_month" :value="month_invasion_data[parseInt(data.day.split('-')[2])]" class="item">
                      <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[parseInt(data.day.split('-')[2])] > 0 && month_invasion_data[parseInt(data.day.split('-')[2])] <= 5" type="warning">
                        有事件
                      </el-tag>
                      <el-tag v-if="parseInt(data.day.split('-')[1]) === cur_month && month_invasion_data[parseInt(data.day.split('-')[2])] > 5" type="danger">
                        有事件
                      </el-tag>
                    </el-badge>
                  </div>
                </el-popover>
              </div>
            </template>
          </el-calendar>
        </el-main>
      </el-container>
      <el-dialog id="video_player" width="800" height="360" :visible.sync="dialogMediaVisible">
        <img id="1" ref="imgs" style="-webkit-user-select: none;background-color: hsl(0, 0%, 25%);" authsrc="http://127.0.0.1:8000/api/invationrecord/getvideo" src="" type="video/mp4" width="680" height="340">
      </el-dialog>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import axios from 'axios'
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'

export default {
  name: 'Monitor',
  components: {Banner, MySidenavAdmin, MyDropdown},
  data () {
    return {
      loading: true,
      dia_loading: false,
      dialogMediaVisible: false,
      imgSrc: require('../../../assets/img3.jpg'),
      options: [],
      value: '',
      cur_month: -1,
      cur_year: 0,
      cur_day: 0,
      month_invasion_data: {},
      detail_invasion_data: []
    }
  },
  methods: {
    set_cur_month () {
      let nowDate = new Date()
      this.cur_month = nowDate.getMonth() + 1
      this.cur_year = nowDate.getFullYear()
    },
    handle_click (date) {
      if (parseInt(date[1]) !== this.cur_month) {
        this.cur_year = parseInt(date[0])
        this.cur_month = parseInt(date[1])
      }
      if (this.month_invasion_data[parseInt(date[2])] > 0) {
        this.dia_loading = true
        console.log(date[0] + '-' + date[1] + '-' + date[2])
        let formData = new FormData()
        formData.append('date', date[0] + '-' + date[1] + '-' + date[2]) // 2021-7-10
        const auth = 'Token ' + localStorage.getItem('token')
        const header = {'Authorization': auth}
        axios.post('http://127.0.0.1:8000/api/attacklistuser/invasiontime', formData, {'headers': header}).then(response => {
          // console.log(response.data)
          this.detail_invasion_data = response.data
          this.dia_loading = false
        })
      }
    },
    handleSee (index, row, day) {
      this.dialogMediaVisible = true
      setTimeout(() => {
        var img = document.getElementById(1)
        var url = img.getAttribute('authsrc')
        var request = new XMLHttpRequest()
        request.responseType = 'blob'
        request.open('get', url + '?date=' + day + '&time=' + row.time, true)
        const auth = 'Token ' + localStorage.getItem('token')
        console.log(auth)
        // const header = {'Authorization': auth}
        request.setRequestHeader('Authorization', auth)
        request.onreadystatechange = e => {
          if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
            console.log(request)
          }
        }
        request.send(null)
        img.src = 'http://127.0.0.1:8000/api/invationrecord/getvideo' + '?date=' +
          day + '&time=' + row.time
      }, 0)
    }
  },
  mounted () {
    this.$nextTick(() => {
      // 点击上个月
      let prevBtn1 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(1)')
      prevBtn1.addEventListener('click', () => {
        if (this.cur_month - 1 === 0) {
          this.cur_year -= 1
        }
        this.cur_month = (this.cur_month + 11) % 12
      })
      // 点击今天
      let prevBtn2 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(2)')
      prevBtn2.addEventListener('click', () => {
      })
      // 点击下个月
      let prevBtn3 = document.querySelector('.el-calendar__button-group .el-button-group>button:nth-child(3)')
      prevBtn3.addEventListener('click', () => {
        if (this.cur_month + 1 === 13) {
          this.cur_year += 1
        }
        this.cur_month = this.cur_month % 12 + 1
      })
    })
    this.set_cur_month()
  },
  watch: {
    // eslint-disable-next-line camelcase
    cur_month (new_month, old_month) {
      this.loading = true
      let formData = new FormData()
      formData.append('month', this.cur_year + '-' + this.cur_month) // 2021-7-10
      const auth = 'Token ' + localStorage.getItem('token')
      const header = {'Authorization': auth}
      axios.post('http://127.0.0.1:8000/api/invationrecord/getmonth', formData, {'headers': header}).then(response => {
        console.log(response.data)
        this.month_invasion_data = response.data
        this.loading = false
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
.el-menu {
  width: 200px;
  height: 800px;
}
.submenu-title {
  font-size: 18px !important;
}

.main {
  left: 200px;
  top: 100px;
  position: absolute;
}

.budge{
  width: 10px;
  height: 10px;
  border-radius: 5px;
  margin: 5px auto;
}

.red{
  background-color: #c9413f;
}
.green{
  background-color: #25b591;
}
.orange{
  background-color: #ee915c;
}

.date_cell {
  display: inline-block;
}

.user-menu {
  left: 50px;
  top: 5px;
}

</style>
