<template>
    <Panel shadow>
      <div slot="title">{{$t('m.All_Board')}} {{$t('m.Board')}}</div>
    </Panel>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'ProblemList',
    components: {
      Pagination
    },
    data () {
      return {
        boardTableColumns: [
          {
            title: this.$i18n.t('m.Title'),
            width: 400,
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
              let t = params.row.difficulty
              let color = 'blue'
              if (t === 'Low') color = 'green'
              else if (t === 'High') color = 'yellow'
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
                    this.$router.push({name: 'board-detail', params: {boardID: params.row.created_by.username}})
                  }
                }
              }, params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Comment'),
            render: (h, params) => {
              return h(params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Views'),
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'board-detail', params: {boardID: params.row.views}})
                  }
                }
              }, params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Date'),
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'board-detail', params: {boardID: params.row.create_time}})
                  }
                }
              }, params.row.title)
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
    }
}
</script>

<style scoped lang="less">
</style>