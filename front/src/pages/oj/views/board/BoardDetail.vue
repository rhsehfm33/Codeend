<template>
  <div>
    <Panel class="board-container">
      <div class="top-container">
        <p v-html=board.title></p>
        <p v-html=board.created_by.username></p>
        <p v-html=board.create_time></p>
      </div>
      <div class="body-container">
        <p v-html=board.content></p>
      </div>
    </Panel>
    <Panel class="comment-container">
      <!-- <Card
        v-for="comment in comments"
        :key=""
        :card="card"
        :boardId="board.boardId"
      /> -->
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'

  export default {
    name: 'BoardDetail',
    data () {
      return {
        board: {
          boardId: '',
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
        api.getBoardDetail(this.boardId).then(res => {
          let board = res.data.data
          this.board = board
        })
      }
    }
}
</script>

<style scoped lang="less">
</style>