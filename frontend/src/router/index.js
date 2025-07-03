import { createRouter, createWebHistory } from 'vue-router'
import MovieListView from '@views/movie/MovieListView.vue';

const routes = [
    {path: '/', redirect: '/movies'},
    {path: '/movies', name: 'Movies', component: MovieListView},
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
