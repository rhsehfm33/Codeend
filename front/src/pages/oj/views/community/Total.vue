<template>
  <div>
    <div>
      <router-link to="total">{{$t('m.Total_Community')}}</router-link>
      <router-link to="announcements">{{$t('m.Announcements_Community')}}</router-link>
      <router-link to="forum">{{$t('m.Forum')}}</router-link>
      <router-link to="question">{{$t('m.Question')}}</router-link>   
    </div>
    <panel>
      <div slot="title">전체 게시판</div>
              <div class="panel">
          <transition name="fadeInUp">
            <router-view></router-view>
          </transition>
        </div>
      <div class="content markdown-body">
      </div>
        <Pagination v-if="!isContest"
                key="page"
                :total="total"
                :page-size="limit"
                @on-change="getAnnouncementList">
        </Pagination> 
        <router-view></router-view>
    </panel>
  </div>
</template>

<script>
  import api from '@oj/api'
  import Pagination from '@oj/components/Pagination'
  export default {
    name: 'Announcement',
    components: {
      Pagination
    },
    data () {
      return {
        limit: 10,
        total: 10,
        btnLoading: false,
        announcements: [],
        announcement: '',
        listVisible: true
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        if (this.isContest) {
          this.getContestAnnouncementList()
        } else {
          this.getAnnouncementList()
        }
      },
      getAnnouncementList (page = 1) {
        this.btnLoading = true
        api.getAnnouncementList((page - 1) * this.limit, this.limit).then(res => {
          this.btnLoading = false
          this.announcements = res.data.data.results
          this.total = res.data.data.total
        }, () => {
          this.btnLoading = false
        })
      },
      getContestAnnouncementList () {
        this.btnLoading = true
        api.getContestAnnouncementList(this.$route.params.contestID).then(res => {
          this.btnLoading = false
          this.announcements = res.data.data
        }, () => {
          this.btnLoading = false
        })
      },
      goAnnouncement (announcement) {
        this.announcement = announcement
        this.listVisible = false
      },
      goBack () {
        this.listVisible = true
        this.announcement = ''
      }
    },
    computed: {
      title () {
        if (this.listVisible) {
          return this.isContest ? this.$i18n.t('m.Contest_Announcements') : this.$i18n.t('m.Announcements')
        } else {
          return this.announcement.title
        }
      },
      isContest () {
        return !!this.$route.params.contestID
      }
    }
  }
</script>

<style lang="less" scoped>

.category-container{
    display: inline-block;
    min-width: 280px;
    height: auto;
    width: 100%;
    z-index: 1000;
    background-color: white;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
}
  .content {
    font-size: 16px;
    margin: 0 50px 40px 50px;
    > ul {
      list-style: disc;
      li {
        font-size: 16px;
        margin-top: 20px;
        &:first-child {
          margin-top: 0;
        }
        p {
          font-size: 14px;
          margin-top: 5px;
        }
      }
    }
  }
</style>
