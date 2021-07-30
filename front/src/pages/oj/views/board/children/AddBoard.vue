<template>
  <div class="setting-main">
    <div class="flex-container">
      <div class="form-container">
        <p class="section-title">{{$t('m.Write')}}</p>
        <Form class="setting-content" ref="board" :model="board">
          <FormItem prop="board_title">
            <Input placeholder="제목을 입력하세요." v-model="board.title" type="text"/>
          </FormItem>
          <FormItem prop="board_category">
            <Select v-model="board.category" placeholder="게시판을 선택하세요.">
              <Option :label="$t('m.Free')+$t('m.Board')" value="Free"></Option>
              <Option :label="$t('m.Question')+$t('m.Board')" value="Question"></Option>
            </Select>
          </FormItem>
          <FormItem required>
            <Simditor v-model="board.content"/>
          </FormItem>
          <Button type="primary" @click="submitPost">{{$t('m.Post')}}</Button>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  import Simditor from '../../../../admin/components/Simditor.vue'
  import { mapActions } from 'vuex'

  export default {
    mixins: [FormMixin],
    components: {
      Simditor
    },
    data () {
      return {
        currentAnnouncementId: null,
        // mode: 'create',
        // 공지 (new | edit) model
        board: {
          id: '',
          title: '',
          category: '',
          content: ''
        },
        created_by: {
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapActions(['getProfile']),
      init () {
        api.getUserInfo(this.username).then(res => {
          this.created_by = res.data.data.user
        })
      },
      submitPost () {
        let data = {
          id: this.created_by.id,
          title: this.board.title,
          category: this.board.category,
          content: this.board.content
        }
        api.createBoard(data).then(res => {
          this.$router.push({name: 'all-board'})
        })
      }
    }
  }
</script>

<style lang="less" scoped>

  .flex-container {
    text-align: center;
    background-color: gainsboro;
    .form-container {
      flex: 1;
      width: 250px;
      padding-right: 5%;
    }
  }
</style>