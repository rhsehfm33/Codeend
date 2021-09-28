<template>
    <Panel shadow>
      <div slot="title">{{$t('m.All_Board')}} {{$t('m.Board')}}
      </div>
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
    :page-size.sync="limit" 
    @on-change="changeRoute" 
    @on-page-size-change="changeRoute" 
    :current.sync="page" 
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

  const limit = 10

  export default {
    name: 'all-board',
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
            width: 120,
            render: (h, params) => {
              let t = params.row.category
              let color = 'blue'
              if (t === 'Free') color = 'green'
              else if (t === 'Question') color = 'yellow'
              return h('Tag', {
                props: {
                  color: color
                },
                style: {
                  overflowX: 'auto'
                }
              }, this.$i18n.t('m.' + params.row.category))
            }
          },
          {
            title: this.$i18n.t('m.Created_By'),
            width: 120,
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
                  overflowX: 'auto'
                }
              }, params.row.created_by.username)
            }
          },
          {
            title: this.$i18n.t('m.Comment'),
            width: 100,
            textAlign: 'left',
            render: (h, params) => {
              return h('span', {
                style: {
                  width: '100%'
                }
              }, params.row.total_comments)
            }
          },
          {
            title: this.$i18n.t('m.Views'),
            width: 100,
            render: (h, params) => {
              return h('span', {
                style: {
                  textAlign: 'center',
                  width: '100%'
                }
              }, params.row.views)
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
        limit: limit,
        total: 0,
        page: 1,
        query: {
          keyword: '',
          category: ''
        },
        loadings: {
          table: true
        },
        comment: ''
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        let route = this.$route.query
        this.query.keyword = route.keyword || ''
        this.page = parseInt(route.page) || 1
        this.limit = parseInt(route.limit) || 10
        this.getBoardList(this.page)
      },
      changeRoute () {
        let query = Object.assign({}, this.query)
        query.page = this.page
        query.limit = this.limit
        this.$router.push({
          name: 'all-board',
          query: utils.filterEmptyValue(query)
        })
      },
      getBoardList (page = 1) {
        let offset = (page - 1) * this.limit
        this.loadings.table = true
        api.getBoardList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.boardList = res.data.data.results
          this.total = res.data.data.total
        }, res => {
          this.loadings.table = false
        })
      },
      filterByCategory (category) {
        this.query.category = category
        this.query.page = 1
        // this.pushRouter()
        this.changeRoute()
      },
      filterByKeyword () {
        this.query.page = 1
        // this.pushRouter()
        this.changeRoute()
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
