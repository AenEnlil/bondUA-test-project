<template>
    <div v-if="loading"><Loader /></div>
    <div v-else>
        <div v-if="movies_count === 0" class='no-movies'>
            <p class="no-movies-text">there is no movies yet, but you can...</p>
            <div class="create-movie-button">
                <button @click="showModalWithForm">Add movie</button>
            </div>
        </div>
        <div v-else>
            <div class="movies-list">
                <Movie
                    v-for='movie in movies'
                    :key='movie.id'
                    :movie='movie'
                    mode='list'
                    @deleted='removeMovie'
                />
            </div>
            <div class="buttons">
                <div class="pagination">
                    <button :disabled="!previous_page" @click="goToPreviousPage"> Back </button>
                    <button :disabled="!next_page" @click="goToNextPage"> Next</button>
                </div>
                <div class="create-movie-button">
                    <button @click="showModalWithForm">Add movie</button>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showModal">
        <MovieFormModal :onSubmit="createMovie" @cancel="showModal = false"/>
    </div>
</template>

<script>
  import api from '@/services/api.js'
  import Loader from '@/components/Loader.vue'
  import Movie from '@/components/Movie.vue'
  import MovieFormModal from '@/components/MovieFormModal.vue'
  export default {
    name: 'MovieList',
    components: {
        Loader,
        Movie,
        MovieFormModal,
    },
    data() {
        return {
            movies: [],
            next_page: null,
            previous_page: null,
            movies_count: null,
            loading: true,
            showModal: false,
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

        showModalWithForm() {
          this.showModal = true
        },
        removeMovie(id) {
          this.movies = this.movies.filter(m => m.id !== id)
        },
        goToNextPage() {
         if (this.next_page) {
          this.fetchMovies({url: this.next_page})
         }
        },
        goToPreviousPage() {
         if (this.previous_page) {
          this.fetchMovies({url: this.previous_page})
         }
        },
        async createMovie(formData) {
            try {
                await api.post('/movies/', formData)
                this.showModal = false
            } catch (error) {
                if (error.response && error.response.data) {
                    return Promise.reject(error.response.data)
                }
                console.log("Error while creating comment", error)
            }
        },
    },
    }

</script>
<style scoped>
    .no-movies {
        display: flex;
        flex-direction: column;
        gap: 7px;
        align-items: center;
        justify-content: center;
        margin-top: 50px;
    }
    .no-movies-text{
        margin-bottom: 10px;
    }
    .create-movie-button {
        margin-right: 10px;
    }
    .movies-list {
        grid: auto-flow;
        grid-cols: 2px;
        gap: 4px;
        p: 4px;
    }
</style>
