<template>
  <div id="header">
    <Menu theme="light" mode="horizontal" @on-select="handleRoute" :active-name="activeMenu" class="oj-menu">
      <!-- logo 클릭하면 index 페이지로 이동  -->
       <router-link to="/" tag="div" class="logo"><span>{{website.website_name}}</span></router-link>
    <div class="category-div"> 
      <Menu-item name="/problem" class="oj-menu-item">
        문제
      </Menu-item>

      <Menu-item name="/contest" class="oj-menu-item">
        대회
      </Menu-item>

      <!-- <Menu-item name="/status">
        {{$t('m.NavStatus')}}
      </Menu-item> -->
      
      <!-- <Submenu name="rank">
        <template slot="title">
          랭크
        </template>
        <Menu-item name="/acm-rank">
          {{$t('m.ACM_Rank')}}
        </Menu-item>
        <Menu-item name="/oi-rank">
          {{$t('m.OI_Rank')}}
        </Menu-item>
      </Submenu> -->

      <Submenu name="community" class="oj-menu-item">
        <template slot="title">
          커뮤니티
        </template>
        <Menu-item name="/announcements" class="oj-menu-item">
          공지 게시판
        </Menu-item>
        <Menu-item name="/general-forum" class="oj-menu-item">
          자유 게시판
        </Menu-item>
        <Menu-item name="/question" class="oj-menu-item">
         질문 게시판
        </Menu-item>
      </Submenu>

      <!-- <Submenu name="about">
        <template slot="title">
          {{$t('m.About')}}
        </template>
        <Menu-item name="/about">
          {{$t('m.Judger')}}
        </Menu-item>
        <Menu-item name="/FAQ">
          {{$t('m.FAQ')}}
        </Menu-item>
      </Submenu> -->

      <Menu-item name="/recruit" class="oj-menu-item">
        채용공고
      </Menu-item>

      <Menu-item name="/lecture" class="oj-menu-item">
        학습강의
      </Menu-item>
    </div>

      <!-- 로그인 인증일 경우 -->
      <template v-if="!isAuthenticated">
        <div class="btn-menu">
          <Button type="ghost"
                  ref="loginBtn"
                  shape="circle"
                  @click="handleBtnClick('login')">{{$t('m.Login')}}
          </Button>
          <!-- <Button v-if="website.allow_register"
                  type="ghost"
                  shape="circle"
                  @click="handleBtnClick('register')"
                  style="color: white; background-color: #2db7f5;">{{$t('m.Register')}}
          </Button> -->
        </div>
      </template>
      <template v-else class="display">
        <Dropdown class="drop-menu" @on-click="handleRoute" placement="bottom" trigger="click">
          <Button type="text" class="drop-menu-title">{{ user.username }}
            <Icon type="arrow-down-b"></Icon>
          </Button>
          <Dropdown-menu slot="list">
            <Dropdown-item name="/user-home">{{$t('m.MyHome')}}</Dropdown-item>
            <Dropdown-item name="/status?myself=1">{{$t('m.MySubmissions')}}</Dropdown-item>
            <Dropdown-item name="/setting/profile">{{$t('m.Settings')}}</Dropdown-item>
            <Dropdown-item v-if="isAdminRole" name="/admin">{{$t('m.Management')}}</Dropdown-item>
            <Dropdown-item divided name="/logout">{{$t('m.Logout')}}</Dropdown-item>
          </Dropdown-menu>
        </Dropdown>
      </template>
    </Menu>
    <Modal v-model="modalVisible" :width="400">
      <div slot="header" class="modal-title">{{$t('m.Welcome_to')}} {{website.website_name_shortcut}}</div>
      <component :is="modalStatus.mode" v-if="modalVisible"></component>
      <div slot="footer" style="display: none"></div>
    </Modal>
  </div>
  
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

<style lang="less" scoped>
  #header {
    display: block;
    min-width: 280px;
    position: fixed;
    top: 0;
    left: 0;
    height: auto;
    width: 100%;
    z-index: 1000;
    background-color: rgb(255, 255, 255);
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    .logo {
      font-weight: bold;
      margin-left: 2%;
      margin-right: 2%;
      float: left;
      font-size: 1.2rem;
      line-height: 60px;
    }
    .oj-menu-item {
      font-size: 1.1rem;
    }
    .oj-menu {
      display: flex;
      justify-content: space-between;
      font-size: 1.1rem;
    }
    .drop-menu {
      float: right;
      margin-right: 30px;
      position: absolute;
      right: 10px;
      &-title {
        font-size: 1.1rem;
      }
    }
    .btn-menu {
      font-size: 1.1rem;
      float: right;
      margin-right: 90px;

    }
  }
  .modal {
    &-title {
      font-size: 1.1rem;
      font-weight: 600;
    }
  }
</style>
