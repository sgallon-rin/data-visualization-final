import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            component: () => import('../views/layout/default.vue'),
            children: [
                {
                    path: '',
                    name: 'home',
                    component: () => import('../views/home.vue')
                },
                {
                    path: 'test_api',
                    name: 'test_api',
                    component: () => import('../views/test_api.vue'),
                },
                {
                    path: 'final',
                    name: 'final',
                    component: () => import('../views/final.vue'),
                }
            ]
        },
    ]
})
