<template>
  <div>
    <Panel shadow style="width:100%; margin-top:1rem;">
        <div slot="title" >
          <div class="title-container">
          <div>{{study.title}}</div>
          <div><Button type="primary">{{study.status}}</Button></div>
          </div>
          <div class="userInfo-container">
            <div class="user-container">
              <div class="font-box">
                <h5 style="font-weight:400;">{{study.created_by.username}}</h5>
              </div>
              <div class="font-box">
                <!-- study.last_update_time -->
               <span class="time">{{study.create_time | localtime }}</span>
              </div>
            </div>
            <div class="edit-box" v-if="this.user.id === this.study.created_by.id">
              <el-button type="primary" size="small" @click="editStudy()">수정</el-button>
              <el-button type="primary" size="small" @click="deleteStudy()">삭제</el-button>
            </div>
            <div v-else class="default-box"/>
          </div>
        </div>
      <div class="body-container">
        <ul class="content-list">
          <li>
            <b>스터디 주제 :</b> {{study.subject}} 
          </li>
          <li>
            <b>스터디 목표 :</b> {{study.purpose}}
          </li>
          <li>
            <b>스터디 가격 :</b> {{study.price}}원
          </li>
          <li>
            <b>스터디 모집 인원 :</b> {{study.total_students}} / {{study.max_student}}
          </li>
          <li>
            <b>예상 스터디 일정(횟수) :</b> {{study.schedule}}
          </li>
          <li>
            <b>예상 커리큘럼 :</b> {{study.curriculum}}
          </li>
          <li>
            <b>스터디 주의 사항 :</b> {{study.notice}}
          </li>
          <li>
            <b>스터디 기타 소개 :</b> <p v-html=study.content></p>
          </li>
        </ul>
        <div class="tag-container">
          연관 태그 <Button style="padding:0 0.5rem 0 0.5rem; border:0; outline: 0;" v-for="tag in study.tags" :key="tag">#{{tag}}</Button>
        </div> 
      </div>
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { mapGetters } from 'vuex'

  export default {
    name: 'study-details',
    data () {
      return {
        isVisible: true,
        ClickCommentID: 0,
        user: {},
        mode: 'create',
        study: {
          content: '',
          create_time: '',
          created_by: {
            id: 0,
            username: ''
          },
          curriculum: '',
          category: '',
          id: '',
          last_update_time: '',
          max_students: '',
          notice: '',
          price: '',
          purpose: '',
          reason: '',
          schedule: '',
          status: '',
          subject: '',
          tags: [],
          title: '',
          students: []
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapGetters(['isAuthenticated', 'user']),
      init () {
        this.study.id = this.$route.query.studyID
        this.study.created_by.username = this.$route.query.teacher
        this.checkUser()
        this.getStudy(this.study.id, this.study.created_by.username)
      },
      getStudy (studyID, teacher) {
        api.getStudyDetail(studyID, teacher).then(res => {
          const study = res.data.data
          this.study = study
          console.log(this.study)
        })
      },
      checkUser () {
        api.getUserInfo(this.username).then(res => {
          this.user = res.data.data.user
        })
      },
      deleteStudy () {
        const studyID = this.$route.params.studyID
        this.$confirm("Are you sure?").then(() => {
          api.deleteStudy(studyID).then(res => {
            this.$router.push({name: 'study-list'})
          })
        });
      },
      editStudy () {
        this.$router.push({name: 'add-study', query: {mode: 'edit', studyID: this.study.id, teacher: this.study.created_by.username}})
      },
      editButton (id) {
        this.isVisible = false
        this.ClickCommentID = id
        this.comment.id = id
      },
      goBack () {
        this.isVisible = true
      }
    },
    watch: {
      '$route' () {
        this.init()
      }
    }
  }
</script>

<style scoped lang="less">
.container {
  width: 90%;
  min-width: 800px;
  margin: auto;  
}

.title-container {
  display: flex;
  justify-content: space-between;
}

span.time {
  font-size: 1rem;
  color: rgb(172, 172, 172);
}

ul.content-list li {
  list-style: none;
  min-width: 50rem;
  padding: 5px 0px 5px 5px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgb(228, 228, 228);
}

ul.content-list li:last-child {
    border-bottom: 0px;
}


.top-container {
  background-color: rgb(228, 228, 228);
}

.body-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 500px;
  padding: 1rem;
  font-size: 1rem;
  background-color: rgb(248, 247, 247);
  border-width: 0.2rem;
  border-style: solid;
  border-color: rgb(228, 228, 228);
}

.userInfo-container {
  display: flex;
  justify-content: space-between;
}

.user-container {
  display: flex;
  width: 80%;
}

.edit-box {
  width: 20%;
  text-align: right;
  font-size: 1rem;
}

.default-box {
  width: 20%;
}

.font-box {
  padding-right: 1rem; 
}

.tag-container {
  width: 50%;
  background-color: rgb(219, 219, 219);
  border-radius: 0.3rem;
  padding: 0.3rem;
}

#username {
  padding-right: .5rem;
  font-weight: 400px;
}

#create-time {
  font-size: 0.8rem;
  font-weight: 200px;
}

.editBtns {
  width: 20%;
  text-align: right;
  padding-right: 1rem;
}


</style>