<template>
  <div>
    <!-- 로그인하지 않을 경우 화면 -->
      <template v-if="!isAuthenticated">
        <div>
          <div class="btn-menu">
          <Button type="ghost"
                  ref="loginBtn"
                  shape="circle"
                  @click="handleBtnClick('register')">{{$t('m.Home_Start')}}
          </Button>
        </div>
        </div>
      </template>
      <!-- 로그인했을 경우 화면-->
      <template v-else>
        <Row type="flex" justify="space-around">
          <Col :span="22">
          <panel shadow v-if="contests.length" class="contest">
            <div slot="title">
              <Button type="text"  class="contest-title" @click="goContest">{{contests[index].title}}</Button>
            </div>
            <Carousel v-model="index" trigger="hover" autoplay :autoplay-speed="6000" class="contest">
              <CarouselItem v-for="(contest, index) of contests" :key="index">
                <div class="contest-content">
                  <div class="contest-content-tags">
                    <Button type="info" shape="circle" size="small" icon="calendar">
                      {{contest.start_time | localtime('YYYY-M-D HH:mm') }}
                    </Button>
                    <Button type="success" shape="circle" size="small" icon="android-time">
                      {{getDuration(contest.start_time, contest.end_time)}}
                    </Button>
                    <Button type="warning" shape="circle" size="small" icon="trophy">
                      {{contest.rule_type}}
                    </Button>
                  </div>
                  <div class="contest-content-description">
                    <blockquote v-html="contest.description"></blockquote>
                  </div>
                </div>
              </CarouselItem>
            </Carousel>
          </panel>
         <Announcements class="announcement"></Announcements>
          </Col>
        </Row>
      </template>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import login from '@oj/views/user/Login'
  import Announcements from './Announcements.vue'
  import api from '@oj/api'
  import time from '@/utils/time'
  import { CONTEST_STATUS } from '@/utils/constants'

  export default {
    name: 'home',
    components: {
      login,
      Announcements
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
      ...mapActions(['changeModalStatus']),
      handleBtnClick (mode) {
        this.changeModalStatus({
          visible: true,
          mode: mode
        })
      },
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
      ...mapGetters(['isAuthenticated'])
    }
  }
</script>

<style lang="less" scoped>
  .contest {
    &-title {
      font-style: italic;
      font-size: 21px;
    }
    &-content {
      padding: 0 70px 40px 70px;
      &-description {
        margin-top: 25px;
      }
    }
  }

  .announcement {
    margin-top: 20px;
  }
</style>
