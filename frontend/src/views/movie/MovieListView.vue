<template>
    <div v-if="loading"><Loader /></div>
    <div v-else>
        <p>pass</p>
    </div>
</template>

<script>
  import api from '@/services/api.js'
  import Loader from '@/components/Loader.vue'
  export default {
    name: 'MovieList',
    components: {
        Loader,
    },
    data() {
        return {
            movies: [],
            next_page: null,
            previous_page: null,
            movies_count: null,
            loading: true,
        }
    },
    mounted() {
        this.fetchMovies()
    },
    methods: {
        async fetchMovies({ url=null, query={} } = {}) {
            var url = url ? url : '/movies/'
            try {
              const response = await api.get(url, {params: query})
              this.movies = response.data.results
              this.movies_count = response.data.count
              this.next_page = response.data.next
              this.previous_page = response.data.previous
              this.loading = false }
            catch (error) {
              console.error('error') }
            },
        },
    }

</script>