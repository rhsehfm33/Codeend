import Vue from 'vue'
import VueI18n from 'vue-i18n'
// ivew UI
import ivenUS from 'iview/dist/locale/en-US'
import ivzhCN from 'iview/dist/locale/zh-CN'
import ivKo from 'iview/dist/locale/ko-KR'

// element UI
import elenUS from 'element-ui/lib/locale/lang/en'
import elzhCN from 'element-ui/lib/locale/lang/zh-CN'
import elko from 'element-ui/lib/locale/lang/ko'

Vue.use(VueI18n)

const languages = [
  {value: 'ko-KO', label: '한국어', iv: ivKo, el: elko},
  {value: 'en-US', label: 'English', iv: ivenUS, el: elenUS},
  {value: 'zh-CN', label: '简体中文', iv: ivzhCN, el: elzhCN}
]
const messages = {}

// combine admin and oj
for (let lang of languages) {
  let locale = lang.value
  let m = require(`./oj/${locale}`).m
  Object.assign(m, require(`./admin/${locale}`).m)
  let ui = Object.assign(lang.iv, lang.el)
  messages[locale] = Object.assign({m: m}, ui)
}
// load language packages
export default new VueI18n({
  locale: 'ko-KO',
  messages: messages
})

export {languages}
