<template>
 <div class="div1" >

  <div class="container content-sm">
		<h2 class="title-center">Codeend Online Judge</h2>
		<p class="p1">프로그래밍 문제를 풀고 온라인으로 채점받을 수 있는 곳입니다!</p>
	</div>

  <Button
      class="btn-primary"
      ref="loginBtn"
      shape="rect"
      @click="handleBtnClick('login')">{{$t('m.Start')}}
  </Button>

 </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import login from '@oj/views/user/Login'

  export default {
    components: {
      login
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
.div1{
  background-color: #FFFFFF;
  height: 300px;
  width:1300px;
  text-align: center;
}
.content-sm {
    padding-top: 60px;
    padding-bottom: 60px;
}
.container {
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
}
.btn-primary{
  color: white;
  text-align: center;
  background-color: #0078FF;
  border-color: #0078FF
}
.title-center{
  text-align: center;
}
.p1 {
  padding-left: 60px;
  padding-right: 60px;
  text-align: center;
}
</style>
