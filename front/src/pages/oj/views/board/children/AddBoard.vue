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
          <FormItem prop="board_problemID">
            <Input placeholder="문제 번호를 입력하세요." v-model="board.problemID" type="text"/>
          </FormItem>
          <FormItem required>
            <Simditor v-model="board.content"/>
          </FormItem>
          <div v-if="this.mode === 'create'">
          <el-button type="primary" @click="submitPost">{{$t('m.Post')}}</el-button>
          <el-button type="primary" @click="goBack">{{$t('m.Back')}}</el-button>
          </div>
          <div v-else>
          <el-button type="primary" @click="submitPost">{{$t('m.Post')}}</el-button>
          <el-button type="primary" @click="deleteBoard()">{{$t('m.Delete')}}</el-button>
          </div>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  import Simditor from '../../../../admin/components/Simditor.vue'
  import { mapGetters } from 'vuex'

  export default {
    mixins: [FormMixin],
    components: {
      Simditor
    },
    data () {
      return {
        mode: 'create',
        board: {
          problemID: '',
          id: '',
          title: '',
          category: '',
          content: ''
        },
        created_by: {
          id: -1
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      // ...mapActions(['getProfile']),
      ...mapGetters(['user']),
      init () {
        if (this.$route.query.mode) {
          this.mode = this.$route.query.mode
        }
        api.getUserInfo(this.username).then(res => {
          this.created_by.id = res.data.data.user.id
        })
      },
      submitPost () {
        let data = {
          problem_id: this.board.problemID,
          id: this.created_by.id,
          title: this.board.title,
          category: this.board.category,
          content: this.board.content
        }
        let funcName = this.mode === 'create' ? 'createBoard' : 'editBoard'
        api[funcName](data).then(res => {
          this.$router.push({name: 'all-board'})
        })
      },
      goBack () {
        this.$router.go(-1)
      },
      deleteBoard () {
        const boardID = this.$route.query.boardID
        this.$confirm("Are you sure?").then(() => {
          api.deleteBoard(boardID).then(res => {
            this.$router.push({name: 'all-board'})
          })
        });
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