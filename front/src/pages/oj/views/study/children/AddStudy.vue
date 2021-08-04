<template>
    <Panel shadow class="container">
        <div class="section-title">{{$t('m.Write')}}</div>
        <div class="form-container">
        <Form class="setting-content" ref="study" :model="study">
          <FormItem prop="study_title" label="제목">
            <Input placeholder="스터디 제목" v-model="study.title" type="text">
              {{this.study.title}}
            </Input>
          </FormItem>
          <div class="category-box">
          <FormItem prop="study_subject" label="주제">
            <Input placeholder="스터지 주제" v-model="study.subject" type="text">
              {{this.study.subject}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_purpose" label="목표">
            <Input placeholder="스터디 목표" v-model="study.purpose" type="text">
              {{this.study.purpose}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_schedule" label="일정 (ex. 주 2회)">
            <Input placeholder="스터디 일정" v-model="study.schedule" type="text">
              {{this.study.schedule}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_curriculum" label="커리큘럼">
            <Input placeholder="스터디 커리큘럼" v-model="study.curriculum" type="text">
              {{this.study.curriculum}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_students" label="최대 모집 인원">
            <Input placeholder="모집 인원" v-model="study.max_students" type="text">
              {{this.study.max_students}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_reason" label="모집 이유">
            <Input placeholder="스터디 모집 이유" v-model="study.reason" type="text">
              {{this.study.reason}}
            </Input>
          </FormItem>
          </div>
          <div class="category-box">
          <FormItem prop="study_notice" label="주의사항">
            <Input placeholder="스터디 주의사항" v-model="study.notice" type="text">
              {{this.study.notice}}
            </Input>
          </FormItem>
          </div>
          <div>
          <FormItem prop="study_price" label="가격">
            <Input placeholder="스터디 가격"  
                  v-model="study.price" type="text">
                  {{this.study.price}}</Input>
          </FormItem>
          </div>
          <div class="tag-container">
            <el-form-item :label="$t('m.Tag')" required>
                <el-tag
                  class="tag"
                  v-for="tag in study.tags"
                  :closable="true"
                  :close-transition="false"
                  :key="tag"
                  type="success"
                  @close="closeTag(tag)"
                >{{tag}}</el-tag>
              <Input
                v-if="inputVisible"
                size="mini"
                class="input-new-tag"
                popper-class="problem-tag-poper"
                v-model="tagInput"
                :trigger-on-focus="false"
                @keyup.enter.native="addTag"
                @select="addTag">
              </Input>
              <el-button class="button-new-tag" v-else size="small" @click="inputVisible = true">+ {{$t('m.New_Tag')}}</el-button>
            </el-form-item>
          </div>
          <div class="category-box" v-if="this.mode=='edit'">
          <FormItem prop="study_status" label="모집 상태">
            <Select v-model="study.status" placeholder="게시판을 선택하세요.">
              <Option selected :label="모집중" value="Recruiting">모집중</Option>
              <Option :label="모집완료" value="Recruited">모집완료</Option>
            </Select>
          </FormItem>
          </div>
          <div class="simditor-box">
          <FormItem required>
            <Simditor v-model="study.content">
              {{this.study.content}}
              </Simditor>
          </FormItem>
          </div>
          <div v-if="this.mode === 'create'" class="create-box">      
          <el-button type="primary" class="createBtn" @click="submitPost">{{$t('m.Post')}}</el-button>
          <el-button type="primary" @click="goBack">{{$t('m.Back')}}</el-button>
          </div>
          <div v-else class="edit-box">
          <el-button type="primary" @click="submitPost">{{$t('m.Post')}}</el-button>
          <el-button type="primary" @click="deleteStudy()">{{$t('m.Delete')}}</el-button>
          </div>
        </Form>
        </div>
    </Panel>
</template>

<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  import Simditor from '../../../../admin/components/Simditor.vue'

  export default {
    name: "add-study",
    mixins: [FormMixin],
    components: {
      Simditor
    },
    data () {
      return {
        nowUserID: '',
        mode: 'create',
        created_by: {
          id: 1,
          username: ''
        },
        studyID: '',
        study: {
          title: '',
          content: '',
          subject: '',
          purpose: '',
          schedule: '',
          curriculum: '',
          max_students: '',
          reason: '',
          notice: '',
          tags: [],
          status: 'Recruiting',
          price: '',
          students: ''
        },
        tagInput: '',
        inputVisible: false,
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
      this.getStudyList()
    },
    methods: {
      init () {
        console.log(this.$route.query)
        if (this.$route.query.studyID) {
          this.studyID = this.$route.query.studyID
        }
        if (this.$route.query.teacher) {
          this.created_by.username = this.$route.query.teacher
        }
        if (this.$route.query.mode) {
          this.mode = this.$route.query.mode
        }
        if (this.mode === 'edit') {
          api.getStudyDetail(this.$route.query.studyID, this.created_by.username).then(res => {
            const study = res.data.data
            console.log("edit:")
            this.created_by.id = study.created_by.id
            this.getUserCheck(this.created_by.id)
            this.study.title = study.title
            this.study.content = study.content
            this.study.subject = study.subject
            this.study.purpose = study.purpose
            this.study.schedule = study.schedule
            this.study.curriculum = study.curriculum
            this.study.max_students = parseInt(study.max_students)
            this.study.reason = study.reason
            this.study.notice = study.notice
            this.study.tags = study.tags
            this.study.status = study.status
            this.study.price = parseInt(study.price)
            this.study.students = study.students
          })
        }
      },
      // getStudy (studyID, teacher) {
      //   api.getStudyDetail(studyID, teacher).then(res => {
      //     const study = res.data.data
      //     this.study = study
      //   })
      // },
      // 문제 검색 관련
      getStudyList () {
        let offset = (this.query.page - 1) * this.query.limit
        api.getStudyList(offset, this.limit, this.query).then(res => {
          this.total = res.data.data.total
          this.studyList = res.data.data.results
        })
      },
      getUserCheck (createdByID) {
        this.nowUserID = this.$store.getters.user.id
        if (this.nowUserID !== createdByID) {
          this.$router.push({name: 'home'})
        }
      },
      // querySearch (queryString, cb) {
      //   api.getStudyTagList({ keyword: queryString }).then(res => {
      //     let tagList = []
      //     for (let tag of res.data.data) {
      //       tagList.push({value: tag.name})
      //     }
      //     cb(tagList)
      //   }).catch(() => {
      //   })
      // },
      addTag () {
        let inputValue = this.tagInput
        if (inputValue) {
          this.study.tags.push(inputValue)
        }
        this.inputVisible = false
        this.tagInput = ''
      },
      closeTag (tag) {
        this.study.tags.splice(this.study.tags.indexOf(tag), 1)
      },
      submitPost () {
        let data = {
          id: this.studyID,
          created_by: this.created_by.id,
          title: this.study.title,
          content: this.study.content,
          subject: this.study.subject,
          purpose: this.study.purpose,
          schedule: this.study.schedule,
          curriculum: this.study.curriculum,
          max_students: this.study.max_students,
          reason: this.study.reason,
          notice: this.study.notice,
          tags: this.study.tags,
          status: this.study.status,
          price: this.study.price,
          students: this.study.students
        }
        let funcName = this.mode === 'create' ? 'createStudy' : 'editStudy'
        api[funcName](data).then(res => {
          this.$router.push({name: 'study-list'})
        })
      },
      goBack () {
        this.$router.go(-1)
      },
      deleteStudy () {
        const studyID = this.$route.query.studyID
        this.$confirm("Are you sure?").then(() => {
          api.deleteStudy(studyID).then(res => {
            this.$router.push({name: 'study-list'})
          })
        });
      }
    }
  }
</script>

<style lang="less" scoped>
  .container {
    display: flex;
    justify-content: center;
    flex-direction: column;
    width: 100%;
    min-width: 800px;
    // 글쓰기 중앙 정렬
    text-align: center;
    background-color: rgb(248,247,247);
    border-width: 0.2rem;
    border-style: solid;
    border-color: rgb(228, 228, 228);
    padding: 10px;
  }

  .form-container {
    display: flex;
    justify-content: center;
  }

  .section-title {
    text-align: center;
  }

  .category-box {
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

  .tag-container {
    display: flex;
    justify-content: left;
    flex-direction: row;
    padding-bottom: 1rem;
  }

  .input-new-tag {
    width: 10rem;
  }

  .tag {
    padding: 0.5rem;
    margin-left: 0.5rem;
    border-radius: 0.5rem;
    background-color: skyblue;
    opacity: 5;
  }
</style>