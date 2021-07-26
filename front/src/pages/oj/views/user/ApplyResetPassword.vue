<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">{{$t('m.Reset_Password')}}</div>
    <p class="center">비밀번호를 재설정 할 이메일을 입력하세요.</p>
    <p class="center">자세한 안내가 담긴 메일을 보내드리겠습니다.</p>
    <template v-if="!successApply">
      <Form :rules="ruleResetPassword" :model=formResetPassword ref="formResetPassword">
        <Form-item prop="email">
          <Input class="input" v-model="formResetPassword.email" :placeholder="$t('m.ApplyEmail')" size="large">
          </Input>
        </Form-item>
        <!-- <Form-item prop="captcha" style="margin-bottom:10px">
          <div class="oj-captcha">
            <div class="oj-captcha-code">
              <Input v-model="formResetPassword.captcha" :placeholder="$t('m.RCaptcha')" size="large">
              <Icon type="ios-lightbulb-outline" slot="prepend"></Icon>
              </Input>
            </div>
            <div class="oj-captcha-img">
              <Tooltip content="Click to refresh" placement="top">
                <img :src="captchaSrc" @click="getCaptchaSrc"/>
              </Tooltip>
            </div>
          </div>
        </Form-item> -->
      </Form>
      <Button type="primary"
              @click="sendEmail"
              class="btn" long
              :loading="btnLoading">{{$t('m.Send_Password_Reset_Email')}}
      </Button>
    </template>
    <template v-else>
      <Alert type="success" show-icon>
        {{$t('Success')}}
        <span slot="desc"> {{$t('Password_reset_mail_sent')}}</span>
      </Alert>
    </template>
  </Panel>
</template>
<script>
  import api from '@oj/api'
  import {FormMixin} from '@oj/components/mixins'

  export default {
    mixins: [FormMixin],
    data () {
      const CheckEmailExist = (rule, value, callback) => {
        if (value !== '') {
          api.checkUsernameOrEmail(undefined, value).then(res => {
            if (res.data.data.email === false) {
              callback(new Error(this.$i18n.t('m.The_email_doesnt_exist')))
            } else {
              callback()
            }
          }, _ => callback())
        } else {
          callback()
        }
      }
      return {
        captchaSrc: '',
        successApply: false,
        btnLoading: false,
        formResetPassword: {
          email: '',
          captcha: ''
        },
        ruleResetPassword: {
          email: [
            {required: true, type: 'email', trigger: 'blur'},
            {validator: CheckEmailExist, trigger: 'blur'}
          ],
          captcha: [
            {required: true, trigger: 'blur', min: 1, max: 10}
          ]
        }
      }
    },
    mounted () {
      this.getCaptchaSrc()
    },
    methods: {
      sendEmail () {
        this.validateForm('formResetPassword').then(() => {
          this.btnLoading = true
          api.applyResetPassword(this.formResetPassword).then(res => {
            setTimeout(() => {
              this.btnLoading = false
              this.successApply = true
            }, 2000)
          }, _ => {
            this.btnLoading = false
            this.formResetPassword.captcha = ''
            this.getCaptchaSrc()
          })
        })
      }
    }
  }
</script>

<style scoped lang="less">
  .container {
    border-radius: 1rem;
    width: 450px;
    margin: auto;
    .center {
      text-align: center;
      margin-bottom: 2%;
    }
    .btn {
      text-align: center;
    }
    .input {
      margin-top: 5%;
    }
  }
</style>
