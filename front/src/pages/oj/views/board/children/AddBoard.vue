<template>
  <div class="setting-main">
    <div class="flex-container">
      <div class="form-container">
        <p class="section-title">{{$t('m.Write')}}</p>
        <Form class="setting-content" ref="board" :model="board">
          <div class="input-box">
          <FormItem prop="board_title">
            <p style="display:inline-block; color:red;">*</p>
            <label for="board.title">{{$t('m.EnterTitle')}}</label>
            <Input v-model="board.title" type="text">
              {{this.board.title}}
            </Input>
          </FormItem>
          </div>
          <div class="input-box">
          <FormItem prop="board_category">
            <p style="display:inline-block; color:red;">*</p>
            <label fro="board.category">{{$t('m.ChooseCategory')}}</label>
            <Select v-model="board.category">
              <Option :label="$t('m.Free')+$t('m.Board')" value="Free"></Option>
              <Option :label="$t('m.Question')+$t('m.Board')" value="Question"></Option>
            </Select>
          </FormItem>
          </div>
          <div class="input-box">
          <FormItem prop="board_problemID">
            <p style="display:inline-block; color:red;">*</p>
            <label for="board.problemID">{{$t('m.EnterNumber')}}</label>
            <Input v-model="board.problemID" type="text">
                  {{this.board.problemID}}</Input>
            <!-- <Input v-model="query.keyword"
                   placeholder="문제 번호를 입력하세요."
                   icon="ios-search-strong">
                   {{this.board.problemID}}</Input> -->
          </FormItem>
          </div>
          <div class="simditor-box">
          <FormItem required>
            <Simditor v-model="board.content">
              {{this.board.content}}
              </Simditor>
          </FormItem>
          </div>
          <div v-if="this.mode === 'create'" class="create-box">      
          <el-button type="primary" class="createBtn" @click="submitPost">{{$t('m.Post')}}</el-button>
          <el-button type="primary" @click="goBack">{{$t('m.Back')}}</el-button>
          </div>
          <div v-else class="edit-box">
          <el-button el-bg-green type="primary" @click="submitPost">{{$t('m.Post')}}</el-button>
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

  export default {
    mixins: [FormMixin],
    components: {
      Simditor
    },
    data () {
      return {
        nowUserID: '',
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
        },
        query: {
          keyword: '',
          difficulty: '',
          tag: '',
          page: 1,
          limit: 10
        }
      }
    },
    mounted () {
      this.init()
      this.getProblemList()
    },
    methods: {
      init () {
        if (this.$route.query.mode) {
          this.mode = this.$route.query.mode
        }
        if (this.mode === 'edit') {
          api.getBoardDetail(this.$route.query.boardID).then(res => {
            const board = res.data.data
            this.created_by.id = board.created_by.id
            this.getUserCheck(this.created_by.id)
            this.board.problemID = board.problem._id
            this.board.id = board.id
            this.board.title = board.title
            this.board.category = board.category
            this.board.content = board.content
          })
        }
      },
      // 문제 검색 관련
      getProblemList () {
        let offset = (this.query.page - 1) * this.query.limit
        api.getProblemList(offset, this.limit, this.query).then(res => {
          this.total = res.data.data.total
          this.problemList = res.data.data.results
        })
      },
      getUserCheck (createdByID) {
        this.nowUserID = this.$store.getters.user.id
        if (this.nowUserID !== createdByID) {
          this.$router.push({name: 'home'})
        }
      },
      submitPost () {
        let data = {
          problem_id: this.board.problemID,
          id: this.board.id,
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
    display: flex;
    justify-content: center;
    // 글쓰기 중앙 정렬
    text-align: center;
    background-color: rgba(255, 255, 255, 0);
    border-width: 0.2rem;
    border-style: solid;
    border-color: rgb(228, 228, 228);
    padding: 10px;
    .form-container {
      width: 80%;
    }
  }

  .input-box {
    text-align: left;
  }

  .simditor-box {
    text-align: start;
  }

  .create-box {
    display: flex;
    justify-content: space-around;
  }

  .edit-box {
    display: flex;
    justify-content: space-around;
  }
</style>