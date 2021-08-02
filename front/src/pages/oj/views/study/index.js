const StudyList = () => import(/* webpackChunkName: "study" */ './Study.vue')
const Study = () => import(/* webpackChunkName: "study" */ './StudyDetail.vue')
const Payment = () => import(/* webpackChunkName: "study" */ './children/Payment.vue')
const AllStudy = () => import(/* webpackChunkName: "study" */ './children/AllStudy.vue')
const AddStudy = () => import(/* webpackChunkName: "study" */ './children/AddStudy.vue')
const Recruiting = () => import(/* webpackChunkName: "study" */ './children/OpenStudy.vue')
const Recruited = () => import(/* webpackChunkName: "study" */ './children/CloseStudy.vue')

export {StudyList, Payment, Study, AddStudy, AllStudy, Recruiting, Recruited}
