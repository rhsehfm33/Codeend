const StudyList = () => import(/* webpackChunkName: "study" */ './StudyList.vue')
const Payment = () => import(/* webpackChunkName: "study" */ './children/Payment.vue')
const Study = () => import(/* webpackChunkName: "study" */ './Study.vue')

export {StudyList, Payment, Study}
