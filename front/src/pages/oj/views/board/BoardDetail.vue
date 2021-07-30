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
    <div 
      v-for="comment in comments"
      :key="comment.id">
      <Card :comment="comment">
        {{comment.content}}
        {{comment.create_time}}
        {{comment.created_by.username}}
      </Card>
      </div>
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
          title: '',
          category: '',
          views: '',
          create_time: ''
        },
        comments: []
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
          const comments = res.data.data.comment
          this.board = board
          this.comments = comments
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