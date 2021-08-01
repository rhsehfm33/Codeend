<template>
  <div class="study-list-container">
    <Panel>
        <Card v-for="(study, i) in studyList" :key="i" class="card-item">
          <div class="list-title-container">
          {{ study.title }}
          </div>
        </Card>
      <!-- 보드 생성 -->
      <!-- <AddBoard v-if="isAddBoard" /> -->
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'

  export default {
    data () {
      return {
        limit: 20,
        query: {
          keyword: '',
          category: '',
          page: 1,
          limit: 10
        },
        studyList: []
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.getStudyList()
      },
      getStudyList () {
        let offset = (this.query.page - 1) * this.query.limit
        api.getBoardList(offset, this.limit, this.query).then(res => {
          this.studyList = res.data.data.results
          console.log(this.studyList)
        }, res => {
          console.log("성공")
        })
      }
    }
  }
</script>

<style>
.study-list-container {
  display: flex;
  justify-content: center;
  align-content: center;
}

.card-item {
  margin: 10px;
}

.list-title-container {
  display: flex;
  justify-content: center; 
}
</style>