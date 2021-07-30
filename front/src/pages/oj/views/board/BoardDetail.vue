<template>
  <div>
    <Panel class="board-container">
      <div class="top-container">
        <p>{{board.title}}</p>
        <p>{{board.created_by.username}}</p>
        <p>{{board.create_time}}</p>
      </div>
      <div class="body-container">
        <p v-html=board.content></p>
      </div>
    </Panel>
    <Panel class="comment-container">
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'
import { mapActions } from 'vuex'

  export default {
    name: 'BoardDetail',
    data () {
      return {
        user: {},
        boardID: '',
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
        this.boardID = this.$route.params.boardID
        api.getBoardDetail(1).then(res => {
          let board = res.data.data.results
          this.board = board
          console.log(this.board)
        })
      }
    }
}
</script>

<style scoped lang="less">
</style>