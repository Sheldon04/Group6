<template>
  <div>
    <div>
      <el-container>
        <el-header class="header">
          <banner></banner>
        </el-header>
        <el-aside>
          <my-dropdown></my-dropdown>
          <my-sidenav-admin></my-sidenav-admin>
        </el-aside>
        <el-main class="main">
          <el-row :gutter="20">
            <el-col :span="20">
              <el-card header="表1" style="font-weight: bold;">
                <div ref="chart1" style="height: 350px;">
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="20">
              <el-card header="表2" style="font-weight: bold;">
                <div ref="chart2" style="height: 450px;">
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="20">
              <el-card header="表3" style="font-weight: bold;">
                <div ref="chart3" style="height: 450px;">
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MyDropdown from '../../public/Dropdown'
import MySidenavAdmin from '../../public/SideNavAdmin'
import Banner from '../../public/Banner'
export default {
  name: 'AttackInfoUser',
  components: {Banner, MySidenavAdmin, MyDropdown},
  mounted () {
    this.initChart1()
    this.initChart2()
    this.initChart3()
  },
  data () {
    return {
      imgSrc: require('../../../assets/img3.jpg'),
      options: [],
      value: '',
      data: []
    }
  },
  methods: {
    initChart1 () {
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.echarts.init(this.$refs.chart1)

      let base = +new Date(2021, 1, 1)
      let oneDay = 24 * 3600 * 1000

      let data = [[base, Math.random() * 10]]

      for (var i = 1; i < 1000; i++) {
        var now = new Date(base += oneDay)
        // console.log(now.getFullYear())
        // console.log(now.getMonth())
        // console.log(now.getDate())
        console.log([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'))
        data.push([
          [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
          Math.abs(Math.round((Math.random() - 0.5) * 20 + data[i - 1][1]))
        ])
      }

      let option = {
        backgroundColor: '#2c343c',
        tooltip: {
          trigger: 'axis',
          position: function (pt) {
            return [pt[0], '10%']
          }
        },
        title: {
          left: 'center',
          text: '入侵大数据监控折线图',
          textStyle: {
            color: '#ccc'
          }
        },
        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'time',
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '100%']
        },
        dataZoom: [{
          type: 'inside',
          start: 0,
          end: 20
        }, {
          start: 0,
          end: 20
        }],
        series: [
          {
            name: '入侵数量',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {},
            data: data
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option)
    },
    initChart2 () {
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.echarts.init(this.$refs.chart2)

      let option = {
        backgroundColor: '#2c343c',

        title: {
          text: '入侵报警级别饼状图',
          left: 'center',
          top: 20,
          textStyle: {
            color: '#ccc'
          }
        },

        tooltip: {
          trigger: 'item'
        },

        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {}
          }
        },
        visualMap: {
          show: false,
          min: 80,
          max: 600,
          inRange: {
            colorLightness: [0, 1]
          }
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
              {value: 400, name: '普通报警'},
              {value: 350, name: '中等报警'},
              {value: 200, name: '严重报警'}
            ].sort(function (a, b) { return a.value - b.value }),
            roseType: 'radius',
            label: {
              color: 'rgba(255, 255, 255, 0.3)'
            },
            labelLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.3)'
              },
              smooth: 0.2,
              length: 10,
              length2: 20
            },
            itemStyle: {
              color: '#c23531',
              shadowBlur: 200,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            },

            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
              return Math.random() * 200
            }
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option)
    },
    initChart3 () {
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.echarts.init(this.$refs.chart3)

      let option = {
        backgroundColor: '#2c343c',
        title: {
          text: '入侵时间分布雷达图',
          textStyle: {
            color: '#ccc'
          }
        },
        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip: {
          trigger: 'item'
        },
        radar: {
          // shape: 'circle',
          indicator: [
            {name: '0点-4点', max: 6500},
            {name: '4点-8点', max: 16000},
            {name: '8点-12点', max: 30000},
            {name: '12点-16点', max: 38000},
            {name: '16点-20点', max: 52000},
            {name: '20点-24点', max: 25000}
          ]
        },
        series: [{
          name: '入侵次数',
          type: 'radar',
          data: [
            {
              value: [4200, 3000, 20000, 35000, 50000, 18000],
              itemStyle: {
                normal: {
                  color: '#c23531',
                  lineStyle: {
                    color: '#c23531'
                  }
                }
              }
            }
          ]
        }]
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option)
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

.user-menu {
  left: 50px;
  top: 5px;
}

.main {
  width: 1200px;
  height: 1000px;
  left: 280px;
  top: 130px;
  position: absolute;
}

</style>
