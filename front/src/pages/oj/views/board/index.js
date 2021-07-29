const BoardList = () => import(/* webpackChunkName: "board" */ './BoardList.vue')
const BoardDetail = () => import(/* webpackChunkName: "board" */ './BoardDetail.vue')
const AllBoard = () => import(/* webpackChunkName: "board" */ './children/AllBoard.vue')
const FreeBoard = () => import(/* webpackChunkName: "board" */ './children/FreeBoard.vue')
const QuestionBoard = () => import(/* webpackChunkName: "board" */ './children/QuestionBoard.vue')
const AddBoard = () => import(/* webpackChunkName: "board" */ './children/AddBoard.vue')

export {BoardList, BoardDetail, AllBoard, FreeBoard, QuestionBoard, AddBoard}
