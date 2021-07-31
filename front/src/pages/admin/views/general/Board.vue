<template>
  <div class="view">
    <Panel :title="$t('m.BoardList') ">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="8">
            <!-- 게시글 삭제 버튼 -->
            <el-button v-show="selectedBoard.length"
                       type="warning" icon="el-icon-fa-trash"
                       @click="deleteBoard(selectedBoardIDs)">삭제
            </el-button>
          </el-col>
          <el-col :span="selectedBoard.length ? 16: 24">
            <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords"></el-input>
          </el-col>
        </el-row>
      </div>
      <el-table
        v-loading="loadingTable"
        element-loading-text="loading"
        @selection-change="handleSelectionChange"
        ref="table"
        :data="boardList"
        style="width: 100%">
        <!-- 체크 항목 -->
        <el-table-column type="selection" width="55"></el-table-column>
        <!-- board id -->
        <el-table-column prop="id" label="ID"></el-table-column>
        <!-- board title -->
        <el-table-column prop="board.title" label="제목"></el-table-column>
        <el-table-column prop="admin_type" label="카테고리">
          <template slot-scope="scope">
            {{ scope.row.admin_type }}
          </template>
        </el-table-column>
        <el-table-column prop="username" label="글쓴이"></el-table-column>        
        <el-table-column prop="comment" label="댓글"></el-table-column>
        <el-table-column prop="views" label="조회수"></el-table-column>
        <el-table-column prop="create_time" label="생성일">
          <template slot-scope="scope">
            {{scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="마지막 작성일">
          <template slot-scope="scope">
            {{scope.row.last_login | localtime }}
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="삭제" width="200">
          <template slot-scope="{row}">
            <icon-btn name="Delete" icon="trash" 
                      @click.native="deleteBoard([row.id])">
            </icon-btn>
          </template>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="currentChange"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
  </div>
</template>

<script>
  import api from '../../api.js'

  export default {
    name: 'Board',
    data () {
      return {
        // 한 페이지에 표시되는 게시글 수
        pageSize: 10,
        // 총 게시글 수
        total: 0,
        // 게시글 목록
        boardList: [],
        uploadBoardList: [],
        uploadBoardListPage: [],
        uploadBoardListCurrentPage: 1,
        uploadBoardListPageSize: 15,
        // 키워드를 검색
        keyword: '',
        // 현재 사용자 모델
        user: {},
        // 현재 게시글 모델
        board: {},
        loadingTable: false,
        loadingGenerate: false,
        // 현재 페이지 번호
        currentPage: 0,
        selectedBoard: []
      }
    },
    mounted () {
      // 게시글 목록 조회
      this.getBoardList(1)
    },
    methods: {
      // 페이지 번호 바꾸는 함수
      currentChange (page) {
        this.currentPage = page
        this.getBoardList(page)
      },
      // 게시글 목록 조회
      getBoardList (page) {
        // this.loadingTable = true
        this.loadingTable = false
        api.getBoardList((page - 1) * this.pageSize, this.pageSize, this.keyword).then(res => {
          this.loadingTable = false
          this.total = res.data.data.total
          this.boardList = res.data.data.results
        }, res => {
          this.loadingTable = false
        })
      },
      // 게시글 삭제
      deleteBoard (ids) {
        this.$confirm('게시글을 삭제하시나요?', '확인', {
          type: 'warning'
        }).then(() => {
          // 게시글 삭제 api
          api.deleteBoard(ids.join(',')).then(res => {
            this.getBoardList(this.currentPage)
          }).catch(() => {
            this.getBoardList(this.currentPage)
          })
        })
      },
      // 게시글 선택 변경
      handleSelectionChange (val) {
        this.selectedBoard = val
      },
      // 게시글 초기화
      handleResetData () {
        this.uploadBoardList = []
      }
    },
    computed: {
      selectedBoardIDs () {
        let ids = []
        for (let board of this.selectedBoard) {
          ids.push(board.id)
        }
        return ids
      }
    },
    watch: {
      'keyword' () {
        this.currentChange(1)
      },
      // user 의 admin 타입
      'user.admin_type' () {
        if (this.user.admin_type === 'Super Admin') {
          this.user.problem_permission = 'All'
        } else if (this.user.admin_type === 'Regular User') {
          this.user.problem_permission = 'None'
        }
      },
      'uploadBoardListCurrentPage' (page) {
        this.uploadBoardListPage = this.uploadBoardList.slice((page - 1) * this.uploadBoardListPageSize, page * this.uploadBoardListPageSize)
      }
    }
  }
</script>

<style scoped lang="less">
</style>
