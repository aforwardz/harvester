<template>
  <Manipulator name="Manipulator">
    <transition name="modal">
      <div class="login-mask">
        <div class="login-wrapper">
          <div class="login-container">
            <div class="close-btn">
              <span class="close" @click="close_back"></span>
            </div>
            <div class="login-header">
                <h2>Little Old Brother</h2>
                <p>你怎么回事小老弟？</p>
            </div>
            <div class="login-body" v-if="!isLogined">
              <el-form :model="loginForm" ref="loginForm">
                <el-form-item prop="userName">
                  <el-input type="text" v-model="loginForm.userName" placeholder="账号"></el-input>
                </el-form-item>
                <el-form-item prop="pwd">
                  <el-input v-model="loginForm.pwd" placeholder="密码" type="password" @keyup.enter.native="submitForm"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="loading" @click="submitForm" class="submitBtn">登录</el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Manipulator>
</template>

<script>
// import { doLogin } from '../../node_modules/vue-helper'
import Manipulator from './menu';
export default {
  name: 'Login',
  props: ['isLogined'],
  components: {
    Manipulator
  },
  data () {
    return {
      loginForm: {
        userName: '',
        pwd: ''
      },
      loading: false
    }
  },
  methods: {
    close_back: function () {
      this.$emit('close');
      this.$router.push({path: '/'})
    },
    submitForm() {
      this.loading = true;
      var data = {
        'username': this.loginForm.userName,
        'password': this.loginForm.pwd
      }
      this.$http.post(this.LOGIN, data).then(
        (response) => {
          this.close_back();
          this.$message({message: response.body.detail, type: 'success'});
          this.loading = false
          this.$store.state.LoginState = true;
          this.$session.set('userName', data.username);
          this.$session.set('identity', response.body.identity);
          var curTime = new Date().getTime();
          this.$session.set('lastLogined', curTime);
          console.log(response)
          console.log(document.cookie)
          // this.$emit('afterLogin')
          },
        (response) => {
          // this.close_back();
          this.$message({message: response.body.detail, type: 'error'});
          this.loading = false;
          this.$session.delete('userName')
        })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.login-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.login-container {
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: rgb(84, 92, 100);
  opacity: 0.95;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.login-container .close-btn .close {
    /* still bad on picking color */
    background-color: #fff;
    color: gray;
    /* make a round button */
    border-radius: 16px;
    /* center text */
    line-height: 20px;
    text-align: center;
    height: 20px;
    width: 20px;
    font-size: 20px;
    padding: 1px;
}
/* use cross as close button */
.login-container .close-btn .close::before {
    content: "\2716";
}
/* place the button on top-right */
.login-container .close-btn .close {
    top: -20px;
    right: -30px;
    float: right;
    position: relative;
}

.login-header {
  width: 300px;
  text-align: center;
}

.login-header h2 {
  font-weight: 400;
  color: #20A0FF;
}

.login-header p {
  font-size: 15px;
  color: #1f2f3d;
}

.login-body {
  width: 300px;
  margin: 20px 0;
  text-align: center;
  display: flex;
}

.login-body form {
  margin-left: auto;
  margin-right: auto;
}

.login-body .submitBtn {
  width: 60%;
}

.login-footer {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  width: 300px;
  font-size: 14px;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .login-container,
.modal-leave-active .login-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
