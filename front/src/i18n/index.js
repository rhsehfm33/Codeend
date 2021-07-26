import Vue from 'vue'
import VueI18n from 'vue-i18n'
// iview UI
import ivkoKR from 'iview/dist/locale/ko-KR'
import ivenUS from 'iview/dist/locale/en-US'
import ivzhCN from 'iview/dist/locale/zh-CN'

// element UI
import elkoKR from 'element-ui/lib/locale/lang/ko'
import elenUS from 'element-ui/lib/locale/lang/en'
import elzhCN from 'element-ui/lib/locale/lang/zh-CN'
Vue.use(VueI18n)

const languages = [
  {value: 'ko-KR', label: '한국어', iv: ivkoKR, el: elkoKR},
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
  locale: 'ko-KR',
  messages: messages
})

export {languages}
