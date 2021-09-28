<template>
  <div>
    <Panel>
        <div slot="title" >
          {{board.title}}
          <div class="userInfo-container">
            <div class="user-container">
              <div class="font-box">
                <h5 style="font-weight:400;">{{board.created_by.username}}</h5>
              </div>
              <div class="font-box">
               <h5 style="font-weight:350;">{{board.create_time | localtime }}</h5>
              </div>
            </div>
            <div class="edit-box" v-if="this.user.id === this.board.created_by.id">
              <el-button type="primary" size="small" @click="editBoard()">수정</el-button>
              <el-button type="primary" size="small" @click="deleteBoard()">삭제</el-button>
            </div>
            <div v-else class="default-box"/>
          </div>
        </div>
      <div class="body-container">
        <p v-html=board.content></p>
      </div>
    </Panel>
    <div>
    <Comment/>
    <ul class="ul">
      <li v-for="comment in comments"
          v-bind:key="comment.id"
      >
        <div v-if="isVisible || comment.id !== ClickCommentID" class="comment-container">
          <div class="comment-user">
            <div class="comment-user-container">
              <p id="username">{{comment.created_by.username}}</p>
              <p id="create-time">{{comment.create_time | localtime}}</p>
            </div>
            <div class="editBtns" v-if="comment.created_by.id === user.id" >
              <el-button type="primary" size="small" @click="editButton(comment.id)">수정</el-button>
              <el-button type="primary" size="small" @click="deleteComment(comment.id)">삭제</el-button>
            </div>
          </div>
          <div class="comment-content">
            {{comment.content}}
          </div>
        </div>
        <div v-else-if="!isVisible && ClickCommentID === comment.id" >
          <textarea v-model="comment.content" 
                    cols="50" rows="3">
          </textarea>
          <el-button type="primary" size="small" class="comment-update-btn" @click="editComment(comment.id, comment.content)">수정</el-button>
          <el-button type="primary" size="small" v-on:click.prevent="goBack">취소</el-button>
        </div>
      </li>
    </ul>
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
        isVisible: true,
        ClickCommentID: 0,
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
        this.ClickCommentID = id
        this.comment.id = id
      },
      editComment (id, content) {
        const data = {
          id: id,
          content: content
        }
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
.ul {
  list-style:none;
}

.top-container {
  background-color: rgb(228, 228, 228);
}

.body-container {
  min-height: 500px;
  padding: 1rem;
  font-size: 1rem;
  background-color: rgb(248, 247, 247);
  border-width: 0.2rem;
  border-style: solid;
  border-color: rgb(228, 228, 228);
}

.userInfo-container {
  display: flex;
  justify-content: space-between;
}

.user-container {
  display: flex;
  width: 80%;
}

.edit-box {
  width: 20%;
  text-align: right;
  font-size: 1rem;
}

.default-box {
  width: 20%;
}

.font-box {
  // color: white;
  padding-right: 1rem; 
}

.comment-container {
  text-align: left;
  padding: 10px;
  margin-top: .5rem;
  background-color: rgb(248, 247, 247);
  border: 1px solid;
  border-width: 0.2rem;
  border-color: rgb(228, 228, 228);
}

.comment-user {
  display: flex;
  justify-content: space-between;
}

.comment-user-container {
  display : flex;
  align-items: center;
  width: 80%;
  font-size: 1.2rem;
  padding-bottom: 1rem;
}

#username {
  padding-right: .5rem;
  font-weight: 400px;
}

#create-time {
  font-size: 0.8rem;
  font-weight: 200px;
}

.editBtns {
  width: 20%;
  text-align: right;
  padding-right: 1rem;
}


</style>