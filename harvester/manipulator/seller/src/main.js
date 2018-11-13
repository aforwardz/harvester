// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router/index'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
Vue.use(VueResource);
Vue.config.productionTip = false;
Vue.http.options.credentials = true;

// API
if (process.env.NODE_ENV === 'development'){
  Vue.prototype.API_BASE = 'http://127.0.0.1:8000/';
  Vue.prototype.ADMIN_BASE = 'http://127.0.0.1:8000/admin/'
}
else {
  Vue.prototype.API_BASE = 'http://aforwardz.com/';
  Vue.prototype.ADMIN_BASE = 'http://aforwardz.com/admin/'
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
