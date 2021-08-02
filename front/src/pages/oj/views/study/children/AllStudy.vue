<template> 
<Row type="flex" :gutter="18">
  <Col :span=19>
  <Panel shadow style="width: 100%">
    <div slot="title">{{$t('m.Study_Title')}}</div>
    <div slot="extra">
      <ul class="filter">
        <li>
          <Input v-model="query.keyword" @on-enter="filterByKeyword"
                @on-click="filterByKeyword"
                placeholder="keyword"
                icon="ios-search-strong"/>
        </li>
      </ul>
    </div>
        <div class="grid-item">
        <Card v-for="(study, i) in studyList" :key="i" class="card-item">
          <router-link class="router-link" :to="{ name: 'study-details', params: { studyID: study.id, teacher: study.created_by.username }}">
          <div class="card-header">
            <span># 주제</span>
            <div class="status">
              <Button class="statusBtn">{{study.status}}</Button>
            </div>
          </div>
            <div class="title-container margin-bottom">
              제목 : <h3>{{ study.title }}</h3>
            </div>
            <div class="margin-bottom">
              주제 : 
              {{study.subject}}
            </div>
            <div class="margin-bottom">
              작성자 : 
              {{ study.created_by.username}}
            </div>
            <div class="margin-bottom">
              {{ study.price}}원
            </div>
            <div> 태그 
               <Button v-for="(tag, i) in study.tags" :key="i">
                 {{tag}}</Button>
            </div>
            <div>신청 인원/모집인원 : {{study.total_students}}/{{study.max_students}}</div>
            </router-link> 
        </Card> 
      </div>
  </Panel>
  </Col>
    <Col :span="4" style="width: 20%">
    <Panel shadow>
      <div slot="title" class="taglist-title">{{$t('m.Tags')}}</div>
      <Button v-for="(tag, i) in tagList" :key="i"
              @click="filterByTag(tag.name)"
              type="ghost"
              :disabled="query.tag === tag"
              shape="circle"
              class="tag-btn">{{tag.name}}
      </Button>
    </Panel>
    <Spin v-if="loadings.tag" fix size="large"></Spin>
    </Col>
  </Row>
</template>

<script>
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'study-list',
    components: {
      Pagination
    },
    data () {
      return {
        // 스터디 리스트 목록
        tagList: [],
        studyList: [],
        mode: 'create',
        limit: 20,
        loadings: {
          table: true,
          tag: true
        },
        routeName: '',
        query: {
          keyword: '',
          status: '',
          tag: '',
          page: 1,
          limit: 10
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init (simulate = false) {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.query.keyword = query.keyword || ''
        this.query.tag = query.tag || ''
        this.query.page = parseInt(query.page) || 1
        if (this.query.page < 1) {
          this.query.page = 1
        }
        this.query.limit = parseInt(query.limit) || 10
        if (!simulate) {
          this.getTagList()
        }
        this.getStudyList()
      },
      getStudyList () {
        let offset = (this.query.page - 1) * this.query.limit
        this.loadings.table = true
        api.getStudyList(offset, this.limit, this.query).then(res => {
          this.table = false
          this.studyList = res.data.data.results
          console.log(this.studyList)
        }, res => {
          this.loadings.table = false
        })
      },
      getTagList () {
        api.getStudyTagList().then(res => {
          this.tagList = res.data.data
          this.loadings.tag = false
        }, res => {
          this.loadings.tag = false
        })
      },
      filterByTag (tagName) {
        this.query.tag = tagName
        this.query.page = 1
        this.pushRouter()
      },
      filterByKeyword () {
        this.query.page = 1
        this.pushRouter()
      },
      pushRouter () {
        this.$router.push({
          name: 'study-list',
          query: utils.filterEmptyValue(this.query)
        })
      }
    }
  }
</script>

<style>
span {
  height: 2em;
  line-height: 2em;
  display: block;
}
  .card-header {
    height: 2em;
    display: flex;
    justify-content: space-between;
  }
  .subject-container {
    display: flex;
    justify-items: center;
  }

  .margin-bottom {
    margin-bottom: 0.5rem;
  }
  .container {
    width: 90%;
    min-width: 50rem;
    margin: auto;
    justify-content: center;
    align-content: center;
  }

.card-item {
  margin: 1rem;
  width: 16rem;
  height: 14rem;
  min-height: 15rem;
  min-width: 10rem;
  box-shadow: 2px 1px 2px;
  border-radius: 1.5rem;
  margin: 1rem auto;
  margin-bottom: 3rem;
  transition: all 0.5s;
  transition-delay: 0.1s;
}

.card-item:hover {
  width: 17rem;
  height: 16rem;
}

.grid-item {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

.title-container {
  display: flex;
  justify-content: left; 

}

.status {
}

.statusBtn {
  font-weight: bold;
}
</style>