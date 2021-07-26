import utils from '@/utils/utils'

export default {
  data () {
    return {
      statusColumn: false
    }
  },
  methods: {
    getACRate (ACCount, TotalCount) {
      return utils.getACRate(ACCount, TotalCount)
    },
    addStatusColumn (tableColumns, dataProblems) {
      if (this.statusColumn) return
      // 문제 제출 기록이 있는 경우에만 추가
      let needAdd = dataProblems.some((item, index) => {
        if (item.my_status !== null && item.my_status !== undefined) {
          return true
        }
      })
      if (!needAdd) {
        return
      }
      tableColumns.splice(0, 0, {
        width: 60,
        title: ' ',
        render: (h, params) => {
          let status = params.row.my_status
          if (status === null || status === undefined) {
            return undefined
          }
          return h('Icon', {
            props: {
              type: status === 0 ? 'checkmark-round' : 'minus-round',
              size: '16'
            },
            style: {
              color: status === 0 ? '#19be6b' : '#ed3f14'
            }
          })
        }
      })
      this.statusColumn = true
    }
  }
}
