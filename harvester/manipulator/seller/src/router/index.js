import Vue from 'vue'
import Router from 'vue-router'
import Cut from '@/components/cut'
import Label from '@/components/label'
import Keyword from '@/components/keyword'
import Classify from '@/components/classify'
import Ner from '@/components/ner'
import Graph from '@/components/graph'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Cut',
      component: Cut
    },
    {
      path: '/label',
      name: 'Label',
      component: Label
    },
    {
      path: '/keyword',
      name: 'Keyword',
      component: Keyword
    },
    {
      path: '/classify',
      name: 'Classify',
      component: Classify
    },
    {
      path: '/ner',
      name: 'Ner',
      component: Ner
    },
    {
      path: '/graph',
      name: 'Graph',
      component: Graph
    }
  ]
})
