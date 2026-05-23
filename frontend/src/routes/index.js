import {createRouter, createWebHashHistory} from "vue-router";

import MapView from "@/views/MapView.vue";
// import LoginView from "@/views/LoginView.vue";
//import RegisterView from "@/views/RegisterView.vue";

const routes = [
/*
    {
        path: '/login',
        name: 'Login',
        component: RegisterView
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView
    },*/
    {
        path: '/:pathMatch(.*)*',
        name: 'Map',
        component: MapView,
        meta: {
            requiresAuth: true
        }
    },
]

const router = createRouter({
    history: createWebHashHistory(process.env.BASE_URL),
    routes
})

export default router