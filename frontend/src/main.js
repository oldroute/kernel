import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'

import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

let $backend = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

$backend.$getRoot = () => {
  return $backend.get(`book/root/`).then(response => response.data)
}

$backend.$getPage = (pk) => {
  return $backend.get(`book/page/${pk}/`)
  .then(response => response.data)
}

$backend.$getTask = (pk) => {
  return $backend.get(`book/task/${pk}/`)
  .then(response => response.data)
}

Vue.prototype.$backend = $backend;
Vue.config.productionTip = false;

Vue.use(BootstrapVue);
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
  el: '#app',
  render: h => h(App)
})
