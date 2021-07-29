import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import storage from '@/utils/storage'
import {STORAGE_KEY} from '@/utils/constants'
import {sync} from 'vuex-router-sync'
import {types, default as store} from '../../../store'

// vueRouter 미들웨어 사용
Vue.use(VueRouter)

const router = new VueRouter({
  // url 해시 사용 안함
  mode: 'history',
  // 클라이언트 측 라우팅을 사용할 때 새로운 경로로 이동할 때
  // 맨 위로 스크롤하거나 실제 페이지를 다시 로드하는 것처럼
  // 컨텐츠 항목의 스크롤 위치를 유지
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return {x: 0, y: 0}
    }
  },
  routes
})

router.beforeEach((to, from, next) => {
  // to: 라우트 = 대상 라우트 객체로 이동함
  // from: 라우트 = 현재 라우트로 오기전 라우트
  // next함수 : 훅을 해결하기 위해 호출
  Vue.prototype.$Loading.start()
  // 대상 라우트 객체의 meta 필드에 접근하기 위해 to.matched. 사용함
  // record: routes 설정의 각 라우트 객체
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 이 라우트는 인증이 필요하고 로그인 한 경우 확인함
    // 로그인하지 않으면 에러창과 모달창을 팝업해줌
    if (!storage.get(STORAGE_KEY.AUTHED)) {
      Vue.prototype.$error('Please login first')
      store.commit(types.CHANGE_MODAL_STATUS, {mode: 'login', visible: true})
      // 그리고 home으로 라우트함
      next({
        name: 'home'
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

router.afterEach((to, from, next) => {
  Vue.prototype.$Loading.finish()
})

sync(store, router)

export default router
