<template>
  <Panel style="padding:0">
    <div slot="title" style="font-size:1rem;">댓글</div>
    <div class="comment-container">
    <Form class="setting-content" ref="comment" :model="comment">
      <FormItem prop="board_title">
        <textarea type="text" class="comment-input" placeholder="댓글을 입력하세요." 
                  v-model="comment.content" 
                  v-on:keypress.enter="submitComment"
                  v-bind:disabled="isAuthenticated === false ? true : false"
                  rows="3"
                  />
      </FormItem>
      <div class="addBtn">
      <el-button type="primary" @click="submitComment">댓글 등록</el-button>
      </div>
    </Form>
    </div>
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
.comment-container {
  padding: 0 1rem 0 1rem;
}

.comment-input {
    display: block;
    resize: auto; 
    width:100%;
    -webkit-writing-mode: horizontal-tb !important;
    text-rendering: auto;
    color: -internal-light-dark(black, white);
    letter-spacing: normal;
    word-spacing: normal;
    text-transform: none;
    text-indent: 0px;
    text-shadow: none;
    display: inline-block;
    text-align: start;
    appearance: auto;
    flex-direction: column;
    cursor: text;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    column-count: initial !important;
    margin: 0em;
    border: 1px solid;
    border-width: 0.2rem;
    border-color: rgb(228, 228, 228);
}

.addBtn {
  text-align: right;
  padding-right: 1rem;
  padding-bottom: 1rem;
}
</style>