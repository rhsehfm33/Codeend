<template>
  <div>
    <div>
        <Menu mode="horizontal" @on-select="handleRoute" :active-name="activeMenu">
          <Menu-item name="/board">
            {{$t('m.All_Board')}}
          </Menu-item>
          <Menu-item name="/board/free">
            {{$t('m.Free')}}
          </Menu-item>
          <Menu-item name="/board/question">
            {{$t('m.Question')}}
          </Menu-item>
          <Menu-item name="/board/write">
            {{$t('m.Write')}}
          </Menu-item>
        </Menu>
    </div>
        <router-view></router-view>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'

  export default {
    mounted () {
      this.getProfile()
    },
    methods: {
      ...mapActions(['getProfile', 'changeModalStatus']),
      handleRoute (route) {
        // if (route && route.indexOf('admin') < 0) {
        this.$router.push(route)
        // } else {
        //   window.open('/admin/')
        // }
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
</style>