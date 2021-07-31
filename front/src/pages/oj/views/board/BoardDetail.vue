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
      <Comment></Comment>
    <ul>
    <li v-for="comment in comments"
        v-bind:key="comment.id"
    >
      <Card :comment="comment" :user="user" class="comment">
        <div v-if="isVisible">
          {{comment.created_by.username}}
          {{comment.create_time | localtime}}
        <div class="comment-content" v-if="isVisible">
          {{comment.content}}
          {{comment.id}}
        </div>
        <div v-if="comment.created_by.id === user.id" >
          <el-button type="primary" size="small" @click="editButton(comment.id)">수정</el-button>
          <el-button type="primary" size="small" @click="deleteComment(comment.id)">삭제</el-button>
        </div>
        </div>
        <div v-else>
          <textarea v-model="comment.content" 
                    cols="50" rows="3">
            </textarea>
          <el-button type="primary" size="small" class="comment-update-btn" @click="editComment(comment.id, comment.content)">수정</el-button>
          <el-button type="primary" size="small" v-on:click.prevent="goBack">취소</el-button>
        </div>
      </Card>
    </li>
    </ul>
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
        isVisible: true,
        user: {},
        mode: 'create',
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
        comment: {
          id: 0,
          content: ""
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapGetters(['isAuthenticated', 'user']),
      init () {
        const boardID = this.$route.params.boardID
        this.checkUser()
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
      checkUser () {
        api.getUserInfo(this.username).then(res => {
          this.user = res.data.data.user
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
        this.$router.push({name: 'write-board', query: {mode: 'edit', boardID: this.$route.params.boardID}})
      },
      editButton (id) {
        this.isVisible = false
        this.comment.id = id
      },
      editComment (id, content) {
        const data = {
          id: id,
          content: content
        }
        console.log(data)
        api.editComment(data).then(res => {
          this.isVisible = true
        })
      },
      deleteComment (id) {
        this.$confirm("Are you sure?").then(() => {
          api.deleteComment(id).then(res => {
            this.$router.go()
          })
        });
      },
      goBack () {
        this.isVisible = true
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