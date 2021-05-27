<template>
  <Panel class="introduce-div">
    <div class="introduce-top-div">
      <h1>Codeend Online Judge</h1>
      <p class="p1">프로그래밍 문제를 풀고 온라인으로 채점받을 수 있는 곳입니다!</p>
      <div class="btn-div">
        <Button class="btn-primary"
                @click="handleBtnClick('register')"
                >{{$t('m.Home_Start')}}
        </Button>
      </div>
    </div>
  </Panel>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import login from '@oj/views/user/Login'
  import register from '@oj/views/user/Register'

  export default {
    components: {
      login,
      register
    },
    mounted () {
      this.getProfile()
    },
    methods: {
      ...mapActions(['getProfile', 'changeModalStatus']),
      handleRoute (route) {
        if (route && route.indexOf('admin') < 0) {
          this.$router.push(route)
        } else {
          window.open('/admin/')
        }
      },
      handleBtnClick (mode) {
        this.changeModalStatus({
          visible: true,
          mode: mode
        })
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole']),

      activeMenu () {
        return '/' + this.$route.path.split('/')[1]
      },
      modalVisible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      }
    }
  }
</script>

<style>

*{
  box-sizing: border-box;
}
.introduce-div{
  margin: 2%;
}
.introduce-top-div {
    padding: 10%;
    text-align: center;
}
.btn-div{
  margin: 2%;
}
.btn-primary{
  color: white;
  text-align: center;
  background-color: #0078FF;
  border-color: #0078FF
}
.p1 {
  padding-left: 60px;
  padding-right: 60px;
  text-align: center;
}
</style>