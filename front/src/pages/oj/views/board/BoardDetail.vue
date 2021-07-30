<template>
  <div>
    <Panel class="board-container">
      <div class="top-container" >
        <p>{{board.title}}</p>
        <p>{{board.created_by.username}}</p>
        <p>{{board.create_time | localtime }}</p>
        <p>{{board.last_update_time | localtime}}</p>
        <div v-if="this.user.id === this.board.created_by.id">
        <el-button type="primary" size="small" @click="editBoard()">수정</el-button>
        <el-button type="primary" size="small" @click="deleteBoard()">삭제</el-button>
        </div>
      </div>
      <Card class="body-container">
        <p v-html=board.content></p>
      </Card>
    </Panel>
      <Comment v-bind:boardID=this.board.id></Comment>
    <div 
      v-for="comment in comments"
      :key="comment.id">
      <Card :comment="comment">
        {{comment.content}}
        {{comment.create_time | localtime}}
        {{comment.created_by.username}}
      </Card>
      </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import Comment from './Comment.vue'
import { mapGetters } from 'vuex'

  export default {
    name: 'BoardDetail',
    components: {
      Comment
    },
    data () {
      return {
        mode: 'create',
        isVisibie: false,
        board: {
          created_by: {
            id: 0,
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
      ...mapGetters(['isAuthenticated', 'user']),
      init () {
        const boardID = this.$route.params.boardID
        this.checkUserID()
        this.getBoard(boardID)
      },
      getBoard (boardID) {
        api.getBoardDetail(boardID).then(res => {
          const board = res.data.data
          const comments = res.data.data.comment
          this.board = board
          this.comments = comments
        })
      },
      checkUserID () {
        api.getUserInfo(this.username).then(res => {
          this.user.id = res.data.data.user.id
        })
      },
      deleteBoard () {
        const boardID = this.$route.params.boardID
        this.$confirm("Are you sure?").then(() => {
          api.deleteBoard(boardID).then(res => {
            this.$router.push({name: 'all-board'})
          })
        });
      },
      editBoard () {
        this.$router.push({name: 'write-board', query: {mode: 'edit'}})
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