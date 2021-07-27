<template>
  <Row type="flex" justify="space-around">
    <Col :span="22">
    <Panel shadow>
      <div slot="title">{{$t('m.Forum')+' '+$t('m.Board')}}</div>
      <!-- 검색창 -->
      <div slot="extra">
        <ul class="filter">
        <li>
            <Dropdown @on-click="filterByDifficulty">
              <span>{{$t('m.Board')}}
                <Icon type="arrow-down-b"></Icon>
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="Notice">{{$t('m.Notice')}}</Dropdown-item>
                <Dropdown-item name="Forum" >{{$t('m.Forum')}}</Dropdown-item>
                <Dropdown-item name="Question">{{$t('m.Question')}}</Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li>          
          <li>
            <Input v-model="query.keyword"
                   @on-enter="filterByKeyword"
                   @on-click="filterByKeyword"
                   placeholder="keyword"
                   icon="ios-search-strong"/>
          </li>
        </ul>
      </div>
      <div>
      </div>
      <Table style="width: 100%; font-size: 1.4rem;"
             :columns="TotalListTableColumns"
             :data="problemList"
             :loading="loadings.table"
             disabled-hover><tr></tr>
      </Table>
    </Panel>
    <!-- 페이지 변경 -->
    <Pagination :total="total" :page-size.sync="query.limit" @on-change="pushRouter" @on-page-size-change="pushRouter" :current.sync="query.page" :show-sizer="true">
      </Pagination>
    </Col>
  </Row>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import time from '@/utils/time'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'ProblemList',
    components: {
      Pagination
    },
    data () {
      return {
        TotalListTableColumns: [
          {
            title: this.$i18n.t('m.Title'),
            width: 500,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'forum-details', params: {problemID: params.row._id}})
                  }
                },
                style: {
                  padding: '2px 0 0',
                  overflowX: 'auto',
                  textAlign: 'left',
                  width: '100%'
                }
              }, params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Category'),
            render: (h, params) => {
            }
          },
          {
            title: this.$i18n.t('m.Writer'),
            render: (h, params) => {
            }
          },
          {
            title: this.$i18n.t('m.Comment')
          },
          {
            title: this.$i18n.t('m.Views')
          },
          {
            title: this.$i18n.t('m.Date'),
            render: (h, params) => {
              return h('span', time.utcToLocal(params.row.create_time))
            }
          }
        ],
        problemList: [],
        limit: 20,
        total: 0,
        loadings: {
          table: true
        },
        routeName: '',
        query: {
          keyword: '',
          page: 1,
          limit: 10
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init (simulate = false) {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.query.keyword = query.keyword || ''
        this.query.page = parseInt(query.page) || 1
        if (this.query.page < 1) {
          this.query.page = 1
        }
        this.query.limit = parseInt(query.limit) || 10
        this.getProblemList()
      },
      pushRouter () {
        this.$router.push({
          name: 'problem-list',
          query: utils.filterEmptyValue(this.query)
        })
      },
      getProblemList () {
        let offset = (this.query.page - 1) * this.query.limit
        this.loadings.table = true
        api.getProblemList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.total = res.data.data.total
          this.problemList = res.data.data.results
          if (this.isAuthenticated) {
            this.addStatusColumn(this.TotalListTableColumns, res.data.data.results)
          }
        }, res => {
          this.loadings.table = false
        })
      },
      filterByKeyword () {
        this.query.page = 1
        this.pushRouter()
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated'])
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.init(true)
        }
      },
      'isAuthenticated' (newVal) {
        if (newVal === true) {
          this.init()
        }
      }
    }
  }
</script>

<style scoped lang="less">
</style>
