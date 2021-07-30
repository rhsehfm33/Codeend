<template>
  <div>
    <Panel class="board-container">
      <div class="top-container">
        <p>{{board.title}}</p>
        <p>{{board.created_by.username}}</p>
        <p>{{board.create_time}}</p>
        <p>{{board.last_update_time}}</p>
      </div>
      <div class="body-container">
        <p v-html=board.content></p>
      </div>
    </Panel>
    <Panel class="comment-container">
      <p>{{board.comment}}</p>
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'

  export default {
    name: 'BoardDetail',
    data () {
      return {
        user: {},
        board: {
          created_by: {
            username: ''
          },
          comment: [],
          title: '',
          category: '',
          views: '',
          create_time: ''
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        const boardID = this.$route.params.boardID
        api.getBoardDetail(boardID).then(res => {
          const board = res.data.data
          this.board = board
        })
      }
    }
}
</script>

<style scoped lang="less">
</style>