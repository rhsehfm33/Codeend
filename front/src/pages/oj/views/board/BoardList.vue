<template>
  <Panel class="container">
      <div>
        <div class="menu">
        <Menu mode="horizontal" @on-select="handleRoute" :active-name="activeMenu" width="auto">
          <Menu-item name="/boards/all">
            {{$t('m.All_Board')}}
          </Menu-item>
          <Menu-item name="/boards/free">
            {{$t('m.Free')}}
          </Menu-item>
          <Menu-item name="/boards/question">
            {{$t('m.Question')}}
          </Menu-item>
          <Menu-item name="/boards/write">
            {{$t('m.Write')}}
          </Menu-item>
        </Menu>
        </div>
        <div>
          <router-view></router-view>
        </div>
      </div>
  </Panel>
</template>

<script>
  export default {
    name: 'boardList',
    methods: {
      handleRoute (route) {
        this.$router.push(route)
      }
    },
    computed: {
      activeMenu () {
        return this.$route.path
      }
    }
  }
</script>
<style lang="less" scoped>
  .container {
    width: 90%;
    min-width: 800px;
    margin: auto;
  }
  .menu {
    flex: 1 0 150px;
    border-radius: 20px
  } 
</style>

