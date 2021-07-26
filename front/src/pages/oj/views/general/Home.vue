<template>
  <div>
    <!-- 로그인하지 않을 경우 화면 -->
      <template v-if="!isAuthenticated">
          <HomeStart class="home-start"/>
      </template>
      <!-- 로그인했을 경우 화면 -->
      <template v-else>
        <Row type="flex" justify="space-around">
          <Col :span="22">
         <Announcements class="announcement"></Announcements>
          </Col>
        </Row>
      </template>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import Announcements from '../general/Announcements'
  import HomeStart from '../../components/HomeStart'
  import api from '@oj/api'
  import time from '@/utils/time'
  import { CONTEST_STATUS } from '@/utils/constants'

export default {
    name: 'home',
    components: {
      Announcements,
      HomeStart
    },
    data () {
      return {
        contests: [],
        index: 0
      }
    },
    mounted () {
      let params = {status: CONTEST_STATUS.NOT_START}
      api.getContestList(0, 5, params).then(res => {
        this.contests = res.data.data.results
      })
    },
    methods: {
      getDuration (startTime, endTime) {
        return time.duration(startTime, endTime)
      },
      goContest () {
        this.$router.push({
          name: 'contest-details',
          params: {contestID: this.contests[this.index].id}
        })
      }
    },
    computed: {
      ...mapGetters(['modalStatus', 'user', 'isAuthenticated', 'isAdminRole']),

      activeMenu () {
        return '/' + this.$route.path.split('/')[1]
      },
      modalVisible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      }
    }
  }
</script>

<style lang="less" scoped>
  .announcement {
    margin-top: 20px;
  }
  .home-start{
    margin-top: 20px;   
  }
</style>
