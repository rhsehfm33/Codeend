<template>
  <Panel class="comment-container">
    <p>댓글 창!</p>
    <Form class="setting-content" ref="comment" :model="comment">
      <FormItem prop="board_title">
        <Input placeholder="댓글을 입력하세요." v-model="comment.content" type="text"/>
      </FormItem>
      <Button type="primary" @click="submitComment">댓글 등록</Button>
    </Form>
  </Panel> 
</template>

<script>
  import api from '@oj/api'

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
        console.log(this.$route.params.boardID)
      },
      submitComment () {
        let data = {
          id: this.$route.params.boardID,
          content: this.comment.content
        }
        api.createComment(data).then(res => {
          this.$router.push({name: 'board-detail'})
        })
      }
    }
  }
</script>

<style>

</style>