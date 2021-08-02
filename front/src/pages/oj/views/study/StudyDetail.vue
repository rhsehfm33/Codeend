<template>
  <div>
    <Panel class="container">
        <div slot="title" >
          {{study.title}} <Button>{{study.status}}</Button>
          <div class="userInfo-container">
            <div class="user-container">
              <div class="font-box">
                <h5 style="font-weight:400;">{{study.created_by.username}}</h5>
              </div>
              <div class="font-box">
                <!-- study.last_update_time -->
               <h5 style="font-weight:350;">{{study.create_time | localtime }}</h5>
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
        <div class="flex-container">
        <h4>스터디 가격</h4> : {{study.price}}원
        </div>
        <div class="flex-container">
        <h4>스터디 주제</h4> : {{study.subject}}
        </div>   
        <div class="flex-container">
        <h4>스터디 목표</h4> : {{study.purpose}}
        </div>
        <div class="flex-container">
        <h4>스터디 일정</h4> : {{study.schedule}}
        </div>  
        <div class="flex-container">
        <h4>스터디 이유</h4> : {{study.reason}}
        </div>
        <div class="flex-container">
        <h4>스터디 알림</h4> : {{study.notice}}
        </div> 
        <div class="flex-container">
        <h4>스터디 커리큘럼</h4> : {{study.curriculum}}
        </div>   
        <div class="flex-container">
        <h4>스터디 일정</h4> : {{study.schedule}}
        </div>   
        <div class="flex-container">
        <h4>스터디 모집 인원</h4> : {{study.max_student}}
        <h4>현재 신청 인원</h4> : {{study.total_students}}
        </div>
        <div class="flex-container">
        <h4>태그 : </h4><Button v-for="tag in study.tags" :key="tag">{{tag}}</Button>
        </div>
        <div> 내용!
        <p v-html=study.content></p>
        </div>
      </div>
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { mapGetters } from 'vuex'

  export default {
    name: 'StudyDetail',
    data () {
      return {
        isVisible: true,
        ClickCommentID: 0,
        user: {},
        mode: 'create',
        study: {
          created_by: {
            id: 0,
            username: ''
          },
          title: '',
          category: '',
          views: '',
          create_time: ''
        },
        comment: {
          id: 0,
          content: ""
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapGetters(['isAuthenticated', 'user']),
      init () {
        console.log(this.$route.params)
        const studyID = this.$route.params.studyID
        const teacher = this.$route.params.teacher
        this.checkUser()
        this.getStudy(studyID, teacher)
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
        this.$router.push({name: 'add-study', query: {mode: 'edit', studyID: this.$route.params.studyID, teacher: this.study.created_by.username}})
      },
      editButton (id) {
        this.isVisible = false
        this.ClickCommentID = id
        this.comment.id = id
      },
      editComment (id, content) {
        const data = {
          id: id,
          content: content
        }
        api.editComment(data).then(res => {
          this.isVisible = true
        })
      },
      deleteComment (id) {
        this.$confirm("Are you sure?").then(() => {
          api.deleteComment(id).then(res => {
            this.$router.go()
          })
        });
      },
      goBack () {
        this.isVisible = true
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

.ul {
  list-style:none;
}

.top-container {
  background-color: rgb(228, 228, 228);
}

.body-container {
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

.flex-container {
  display: flex;
  justify-content: left;
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
  // color: white;
  padding-right: 1rem; 
}

.comment-container {
  text-align: left;
  padding: 10px;
  margin-top: .5rem;
  background-color: rgb(248, 247, 247);
  border: 1px solid;
  border-width: 0.2rem;
  border-color: rgb(228, 228, 228);
}

.comment-user {
  display: flex;
  justify-content: space-between;
}

.comment-user-container {
  display : flex;
  align-items: center;
  width: 80%;
  font-size: 1.2rem;
  padding-bottom: 1rem;
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