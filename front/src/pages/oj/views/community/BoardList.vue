<template>
  <Row type="flex" :gutter="18">
    <Col :span=19>
    <Panel shadow>
      <div slot="title">자유 게시판</div>
      <div slot="extra">
        <ul class="filter">
          <li>
            <Dropdown @on-click="filterByDifficulty">
              <span>{{$t('m.Category')}}
                <Icon type="arrow-down-b"></Icon>
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="">{{$t('m.All')}}</Dropdown-item>
                <Dropdown-item name="Low">{{$t('m.Low')}}</Dropdown-item>
                <Dropdown-item name="Mid" >{{$t('m.Mid')}}</Dropdown-item>
                <Dropdown-item name="High">{{$t('m.High')}}</Dropdown-item>
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
             :columns="boardListTableColumns"
             :data="boardList"
             :loading="loadings.table"
             disabled-hover><tr></tr>
      </Table>
    </Panel>
    <Pagination :total="total" :page-size.sync="query.limit" @on-change="pushRouter" @on-page-size-change="pushRouter" :current.sync="query.page" :show-sizer="true">
      </Pagination>
    </Col>
  </Row>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'BoardList',
    components: {
      Pagination
    },
    data () {
      return {
        boardListTableColumns: [
          {
            title: this.$i18n.t('m.Title'),
            key: '_id',
            width: 400,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  // 제목 클릭하면 상세 화면으로 라우터를 통해 이동함
                  click: () => {
                    this.$router.push({name: 'board-details', params: {boardID: params.row._id}})
                  }
                },
                style: {
                  padding: '2px 0 0 10px',
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
              return h(params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Writer'),
            render: (h, params) => {
              return h(params.row.created_by)
            }
          },
          {
            title: this.$i18n.t('m.Comment'),
            render: (h, params) => {
              return h(params.row.comment)
            }
          },
          {
            title: this.$i18n.t('m.Views'),
            render: (h, params) => {
              return h(params.row.views)
            }
          },
          {
            title: this.$i18n.t('m.Date'),
            render: (h, params) => {
              // last_update_time 업데이트될 경우 변경
              return h(params.row.create_time)
            }
          }
        ],
        boardList: [],
        limit: 20,
        total: 0,
        loadings: {
          table: true,
          tag: true
        },
        routeName: '',
        query: {
          keyword: '',
          difficulty: '',
          tag: '',
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
        this.getBoardList()
      },
      pushRouter () {
        this.$router.push({
          name: 'board-list',
          query: utils.filterEmptyValue(this.query)
        })
      },
      getBoardList () {
        let offset = (this.query.page - 1) * this.query.limit
        this.loadings.table = true
        api.getBoardList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.total = res.data.data.total
          this.boardList = res.data.data.results
          if (this.isAuthenticated) {
            this.addStatusColumn(this.boardListTableColumns, res.data.data.results)
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
