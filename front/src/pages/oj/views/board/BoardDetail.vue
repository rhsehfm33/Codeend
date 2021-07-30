<template>
  <div>
    <Panel class="board-container">
      <div class="top-container" >
        <p>{{board.title}}</p>
        <p>{{board.created_by.username}}</p>
        <p>{{board.create_time | localtime }}</p>
        <p>{{board.last_update_time | localtime}}</p>
        <div v-if="this.isVisibie">
        <el-button type="primary" size="small" @click="editBoard()" icon="el-icon-plus">수정</el-button>
        <el-button type="primary" size="small" @click="deleteBoard()" icon="el-icon-plus">삭제</el-button>
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
        api.getBoardDetail(boardID).then(res => {
          const board = res.data.data
          const comments = res.data.data.comment
          this.board = board
          this.comments = comments
          this.checkUserID()
        })
      },
      checkUserID () {
        const createdByID = this.$data.board.created_by.id
        // todos: 지금 유저 아이디 가져오기
        const nowUserID = this.$data
        console.log(createdByID)
        console.log(nowUserID)
        if (nowUserID === createdByID) {
          // console.log("일치!")
          this.isVisibie = true
        } else {
          console.log("불일치")
          this.isVisibie = false
        }
      },
      deleteBoard () {
        const boardID = this.$route.params.boardID
        api.deleteBoard(boardID).then(res => {
          this.init()
        })
      },
      editBoard () {
        console.log(this.board)
        const boardID = this.$route.params.boardID
        let data = {
          id: boardID,
          title: "",
          category: "",
          content: this.board.content
        }
        api.editBoard(data).then(res => {
          this.init()
        })
      }
    }
    // computed: {
    //   ...mapGetters(['isAuthenticated', 'user']),
    //   checkUser () {
    //     const nowUserId = this.user.id
    //     const createdById = this.board.created_by.id
    //     if (!this.isAuthenticated) {
    //       // console.log("no")
    //       this.isDisabled = true
    //     } else if (nowUserId === createdById) {
    //       // console.log("일치!")
    //       this.isVisibie = true
    //     } else {
    //       console.log("불일치")
    //     }
    //   }
    // }
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