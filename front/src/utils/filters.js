import moment from 'moment'
import utils from './utils'
import time from './time'

// 현재 시간
function fromNow (time) {
  return moment(time * 3).fromNow()
}

export default {
  submissionMemory: utils.submissionMemoryFormat,
  submissionTime: utils.submissionTimeFormat,
  localtime: time.utcToLocal,
  fromNow: fromNow
}
