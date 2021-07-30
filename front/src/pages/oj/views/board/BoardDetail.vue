<template>
  <div>
    <Panel class="board-container">
      <div class="top-container" >
        <p>{{board.title}}</p>
        <p>{{board.created_by.username}}</p>
        <p>{{board.create_time | localtime }}</p>
        <p>{{board.last_update_time | localtime}}</p>
      </div>
      <Card class="body-container">
        <p v-html=board.content></p>
      </Card>
    </Panel>
    <Comment v-bind:boardID="this.board.id"></Comment>
  </div>
</template>

<script>
  import api from '@oj/api'
  import Comment from './Comment.vue'
  import { mapActions } from 'vuex'

  export default {
    name: 'BoardDetail',
    components: {
      Comment
    },
    data () {
      return {
        user: {},
        mode: 'create',
        board: {
          created_by: {
            username: ''
          },
          comment: [
          ],
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
      ...mapActions(['getProfile', 'changeModalStatus']),
      init () {
        const boardID = this.$route.params.boardID
        api.getBoardDetail(boardID).then(res => {
          const board = res.data.data
          this.board = board
          console.log(`보드 아이디 : ${this.board.id}`)
        })
      }
    }
}
</script>

<style scoped lang="less">
.board-container {
  background-color: yellow;
  padding: 0;
}

.top-container {
  background-color: aqua;
}

.body-container {
  height: 500px;
}
</style>