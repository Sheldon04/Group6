import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Monitor from '../components/user/MonitorUser'
import TracebackUser from '../components/user/TracebackUser'
import AttackListUser from '../components/user/AttackListUser'
import AttackInfoUser from '../components/user/AttackInfoUser'
import MonitorAdmin from '../components/admin/detection/MonitorAdmin'
import TracebackUserAdmin from '../components/admin/detection/TracebackAdmin'
import AttackListUserAdmin from '../components/admin/detection/AttackListAdmin'
import AttackInfoUserAdmin from '../components/admin/detection/AttackInfoAdmin'
import FaceRegistration from '../components/admin/manage/FaceRegistration'
import StuffManage from '../components/admin/manage/StuffManage'
import Segmentation from '../components/admin/settings/Segmentation'
import WhiteList from '../components/admin/settings/WhiteList'
import Deblur from '../components/user/Deblur'
import AboutUs from '../components/AboutUs'
import Contact from '../components/Contact'
import FallListAdmin from '../components/admin/detection/FallListAdmin'
import EmoListAdmin from '../components/admin/detection/EmoListAdmin'
import InteractionListAdmin from '../components/admin/detection/InteractionListAdmin'
import UnkownListAdmin from '../components/admin/detection/UnkownListAdmin'
import VolunteerManage from '../components/admin/manage/VolunteerManage'
import OlderManage from '../components/admin/manage/OlderManage'
import AddPerson from '../components/admin/manage/AddPerson'
import CameraSettings from '../components/admin/settings/CameraSettings'

Vue.use(Router)

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/user/monitor',
      name: 'Monitor',
      component: Monitor
    },
    {
      path: '/user/traceback',
      name: 'TracebackUser',
      component: TracebackUser
    },
    {
      path: '/user/attacklist',
      name: 'AttackListUser',
      component: AttackListUser
    },
    {
      path: '/user/attackinfo',
      name: 'AttackInfoUser',
      component: AttackInfoUser
    },
    {
      path: '/admin/monitor',
      name: 'MonitorAdmin',
      component: MonitorAdmin
    },
    {
      path: '/admin/traceback',
      name: 'TracebackUserAdmin',
      component: TracebackUserAdmin
    },
    {
      path: '/admin/attacklist',
      name: 'AttackListUserAdmin',
      component: AttackListUserAdmin
    },
    {
      path: '/admin/attackinfo',
      name: 'AttackInfoUserAdmin',
      component: AttackInfoUserAdmin
    },
    {
      path: '/admin/facereg',
      name: 'FaceRegistration',
      component: FaceRegistration
    },
    {
      path: '/admin/stuffmanage',
      name: 'StuffManage',
      component: StuffManage
    },
    {
      path: '/admin/volunteermanage',
      name: 'VolunteerManage',
      component: VolunteerManage
    },
    {
      path: '/admin/oldermanage',
      name: 'OlderManage',
      component: OlderManage
    },
    {
      path: '/admin/addperson',
      name: 'AddPerson',
      component: AddPerson
    },
    {
      path: '/admin/whitelist',
      name: 'WhiteList',
      component: WhiteList
    },
    {
      path: '/admin/segmentation',
      name: 'Segmentation',
      component: Segmentation
    },
    {
      path: '/admin/falllist',
      name: 'FallListAdmin',
      component: FallListAdmin
    },
    {
      path: '/admin/emolist',
      name: 'EmoListAdmin',
      component: EmoListAdmin
    },
    {
      path: '/admin/interactionlist',
      name: 'InteractionListAdmin',
      component: InteractionListAdmin
    },
    {
      path: '/admin/unkownlist',
      name: 'UnkownListAdmin',
      component: UnkownListAdmin
    },
    {
      path: '/admin/cameralist',
      name: 'CameraSettings',
      component: CameraSettings
    },
    {
      path: '/user/deblur',
      name: 'Deblur',
      component: Deblur
    },
    {
      path: '/aboutus',
      name: 'AboutUs',
      component: AboutUs
    },
    {
      path: '/contactus',
      name: 'Contact',
      component: Contact
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    return {x: 0, y: 0}
  }
})
export default router
