import api from '@oj/api'

export default {
  data () {
    return {
      captchaSrc: ''
    }
  },
  methods: {
    validateForm (formName) {
      return new Promise((resolve, reject) => {
        this.$refs[formName].validate(valid => {
          if (!valid) {
            this.$error('오류를 확인해주세요.')
          } else {
            resolve(valid)
          }
        })
      })
    },
    getCaptchaSrc () {
      api.getCaptcha().then(res => {
        this.captchaSrc = res.data.data
      })
    }
  }
}
