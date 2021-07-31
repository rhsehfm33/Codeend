<template>
  <Panel class="comment-container">
    <p>댓글 창!</p>
    <div></div>
    <Form class="setting-content" ref="comment" :model="comment">
      <FormItem prop="board_title">
        <textarea placeholder="댓글을 입력하세요." 
                  v-model="comment.content" 
                  v-on:keypress.enter="submitComment"  
                  type="text"
                  v-bind:disabled="isAuthenticated === false ? true : false"
                  />
      </FormItem>
      <div>
      <el-button type="primary" @click="submitComment">댓글 등록</el-button>
      </div>
    </Form>
  </Panel> 
</template>

<script>
  import api from '@oj/api'
  import { mapGetters } from 'vuex'

  export default {
    data () {
      return {
        boardID: "",
        comment: []
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
      },
      submitComment () {
        this.boardID = parseInt((this.$route.params.boardID))
        let data = {
          board_id: this.boardID,
          content: this.comment.content
        }
        api.createComment(data).then(res => {
          this.$router.go()
        })
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated', 'isAdminRole'])
    }
  }
</script>

<style>
</style>