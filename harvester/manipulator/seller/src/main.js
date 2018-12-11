// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router/index'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css';

import VueSessionStorage from 'vue-sessionstorage'
import VueCookies from 'vue-cookies'
import VueRouter from 'vue-router'
import store from './store'

Vue.use(ElementUI);
Vue.use(VueResource);
Vue.use(VueSessionStorage);
Vue.use(VueCookies);
Vue.use(VueRouter);

Vue.config.productionTip = false;
Vue.http.options.credentials = true;
// Vue.http.headers.common['X-CSRFToken'] = Vue.cookies.get('csrftoken')

// 可以用拦截器实现
Vue.http.interceptors.push((request, next) => {
    request.headers.set('X-CSRFToken', Vue.cookies.get('csrftoken'))
    next();
})

// API
if (process.env.NODE_ENV === 'development'){
  Vue.prototype.API_BASE = 'http://127.0.0.1:8000/api/';
  Vue.prototype.NLP_BASE = 'http://127.0.0.1:8000/nlp/';
  Vue.prototype.ADMIN_BASE = 'http://127.0.0.1:8000/admin/'
}
else {
  Vue.prototype.API_BASE = 'https://little-old-brother.cn/api/';
  Vue.prototype.NLP_BASE = 'https://little-old-brother.cn/nlp/';
  Vue.prototype.ADMIN_BASE = 'https://little-old-brother.cn/admin/'
}

Vue.prototype.LOGIN = Vue.prototype.API_BASE + 'account/login/';
Vue.prototype.LOGOUT = Vue.prototype.API_BASE + 'account/logout/';
Vue.prototype.UPLOAD = Vue.prototype.API_BASE + 'kbase/imgFile/';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})
