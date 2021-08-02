<template>
<div class="container">
  <Panel shadow>
        <div class="menu">
        <Menu mode="horizontal" @on-select="handleRoute" :active-name="activeMenu" width="auto">
          <Menu-item name="/studies/all">
            {{$t('m.All')}}
          </Menu-item>
          <Menu-item name="/studies/recruiting">
            {{$t('m.Open')}}
          </Menu-item>
          <Menu-item name="/studies/recruited">
            {{$t('m.Completed')}}
          </Menu-item>
          <Menu-item name="/studies/write">
            {{$t('m.Write')}}
          </Menu-item>
        </Menu>
        </div>
  </Panel>
    <router-view></router-view>
</div>         
</template>

<script>
  export default {
    name: 'studyList',
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

