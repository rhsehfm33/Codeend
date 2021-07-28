const Boards = () => import(/* webpackChunkName: "board" */ './Boards.vue')
const AllBoard = () => import(/* webpackChunkName: "board" */ './children/AllBoard.vue')
const FreeBoard = () => import(/* webpackChunkName: "board" */ './children/FreeBoard.vue')
const QuestionBoard = () => import(/* webpackChunkName: "board" */ './children/QuestionBoard.vue')
const WriteBoard = () => import(/* webpackChunkName: "board" */ './children/WriteBoard.vue')
const BoardDetail = () => import(/* webpackChunkName: "board" */ './BoardDetail.vue')

export {Boards, AllBoard, FreeBoard, QuestionBoard, WriteBoard, BoardDetail}
