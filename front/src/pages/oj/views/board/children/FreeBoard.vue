<template>
    <Panel shadow>
      <div slot="title">{{$t('m.Free')}} {{$t('m.Board')}}</div>
      <div slot="extra">
        <ul class="filter">
          <!-- <li>
            <Dropdown @on-click="filterByCategory">
              <span>{{$t('m.Category')}}
                <Icon type="arrow-down-b"></Icon>
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="All">{{$t('m.All')}}</Dropdown-item>
                <Dropdown-item name="Free">{{$t('m.Free')}}</Dropdown-item>
                <Dropdown-item name="Question" >{{$t('m.Question')}}</Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li> -->
          <li>
            <Input v-model="query.keyword"
                   @on-enter="filterByKeyword"
                   @on-click="filterByKeyword"
                   placeholder="keyword"
                   icon="ios-search-strong"/>
          </li>
        </ul>
      </div>
      <Table style="width: 100%; font-size: 1.4rem;"
             :columns="boardTableColumns"
             :data="boardList"
             :loading="loadings.table"
             disabled-hover>
      </Table>
      <Pagination :total="total" 
    :page-size.sync="query.limit" 
    @on-change="pushRouter" 
    @on-page-size-change="pushRouter" 
    :current.sync="query.page" 
    :show-sizer="true">
    </Pagination>
    </Panel>
</template>

<script>
  import filters from '@/utils/filters'
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'FreeBoard',
    components: {
      Pagination
    },
    data () {
      return {
        boardTableColumns: [
          {
            title: this.$i18n.t('m.ProblemNumber'),
            key: '_id',
            width: 100,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'problem-details', params: {problemID: params.row.problem_id}})
                  }
                },
                style: {
                  padding: '2px 0'
                }
              }, params.row.problem_id)
            }
          },
          {
            title: this.$i18n.t('m.Title'),
            width: 300,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'board-detail', params: {boardID: params.row.id}})
                  }
                },
                style: {
                  padding: '2px 0',
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
              let t = params.row.category
              let color = 'blue'
              if (t === 'Free') color = 'green'
              else if (t === 'Question') color = 'yellow'
              return h('Tag', {
                props: {
                  color: color
                }
              }, this.$i18n.t('m.' + params.row.category))
            }
          },
          {
            title: this.$i18n.t('m.Created_By'),
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'user-home', query: {username: params.row.created_by.username}})
                  }
                },
                style: {
                  padding: '0',
                  // overflowX: 'auto',
                  textAlign: 'left',
                  width: '100%'
                }
              }, params.row.created_by.username)
            }
          },
          {
            title: this.$i18n.t('m.Comment'),
            render: (h, params) => {
              return h('span', params.row.total_comments)
            }
          },
          {
            title: this.$i18n.t('m.Views'),
            render: (h, params) => {
              return h('span', params.row.views)
            }
          },
          {
            title: this.$i18n.t('m.Date'),
            render: (h, params) => {
              return h('span', filters.localtime(params.row.last_update_time))
            }
          }
        ],
        boardList: [],
        limit: 20,
        loadings: {
          // 임시로 로딩 멈춤
          table: false
        },
        routeName: '',
        query: {
          keyword: '',
          category: '',
          page: 1,
          limit: 10
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.query.difficulty = query.difficulty || ''
        this.query.category = "Free"
        this.query.keyword = query.keyword || ''
        this.query.page = parseInt(query.page) || 1
        if (this.query.page < 1) {
          this.query.page = 1
        }
        this.query.limit = parseInt(query.limit) || 10
        this.getBoardList()
        console.log(this.boardList)
      },
      pushRouter () {
        this.$router.push({
          name: 'free-board',
          query: utils.filterEmptyValue(this.query)
        })
      },
      getBoardList () {
        let offset = (this.query.page - 1) * this.query.limit
        this.loadings.table = true
        api.getBoardList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.boardList = res.data.data.results
        }, res => {
          this.loadings.table = false
        })
      },
      filterByCategory (category) {
        this.query.category = category
        this.query.page = 1
        this.pushRouter()
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
