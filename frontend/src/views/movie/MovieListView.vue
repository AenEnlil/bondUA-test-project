<template>
    <div v-if="loading"><Loader /></div>
    <div v-else>
        <div class='menu-buttons'>
            <svg
                class='create-button'
                @click="showModalWithForm"
                width="50px" height="50px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.75 9C12.75 8.58579 12.4142 8.25 12 8.25C11.5858 8.25 11.25 8.58579 11.25 9L11.25 11.25H9C8.58579 11.25 8.25 11.5858 8.25 12C8.25 12.4142 8.58579 12.75 9 12.75H11.25V15C11.25 15.4142 11.5858 15.75 12 15.75C12.4142 15.75 12.75 15.4142 12.75 15L12.75 12.75H15C15.4142 12.75 15.75 12.4142 15.75 12C15.75 11.5858 15.4142 11.25 15 11.25H12.75V9Z"/>
                <path d="M12 1.25C6.06294 1.25 1.25 6.06294 1.25 12C1.25 17.9371 6.06294 22.75 12 22.75C17.9371 22.75 22.75 17.9371 22.75 12C22.75 6.06294 17.9371 1.25 12 1.25ZM2.75 12C2.75 6.89137 6.89137 2.75 12 2.75C17.1086 2.75 21.25 6.89137 21.25 12C21.25 17.1086 17.1086 21.25 12 21.25C6.89137 21.25 2.75 17.1086 2.75 12Z"/>
            </svg>
            <svg
                class='filter-button'
                width="50px" height="50px" viewBox="0 0 24 24"
                @click = 'showFilters = true'
                xmlns="http://www.w3.org/2000/svg">
                <path d="M4 5L10 5M10 5C10 6.10457 10.8954 7 12 7C13.1046 7 14 6.10457 14 5M10 5C10 3.89543 10.8954 3 12 3C13.1046 3 14 3.89543 14 5M14 5L20 5M4 12H16M16 12C16 13.1046 16.8954 14 18 14C19.1046 14 20 13.1046 20 12C20 10.8954 19.1046 10 18 10C16.8954 10 16 10.8954 16 12ZM8 19H20M8 19C8 17.8954 7.10457 17 6 17C4.89543 17 4 17.8954 4 19C4 20.1046 4.89543 21 6 21C7.10457 21 8 20.1046 8 19Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div v-if="movies_count === 0" class='no-movies'>
            <p class="no-movies-text">Movies not found</p>
        </div>
        <div v-else>
            <div class="movies-list">
                <Movie
                    v-for='movie in movies'
                    :key='movie.id'
                    :movie='movie'
                    mode='list'
                    @deleted='removeMovie'
                    @updated='handleUpdate'
                />
            </div>
            <div class="buttons">
                <div class="pagination">
                    <button :disabled="!previous_page" @click="goToPreviousPage"> Back </button>
                    <button :disabled="!next_page" @click="goToNextPage"> Next</button>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showModal">
        <MovieFormModal :onSubmit="createMovie" @cancel="showModal = false"/>
    </div>
    <div v-if="showFilters">
        <MovieFilterForm :onSubmit='applyFilters' :currentFilters='currentFilters' @cancel="showFilters = false"/>
    </div>
</template>

<script>
  import api from '@/services/api.js'
  import Loader from '@/components/Loader.vue'
  import Movie from '@/components/Movie.vue'
  import MovieFormModal from '@/components/MovieFormModal.vue'
  import MovieFilterForm from '@/components/MovieFilterForm.vue'
  export default {
    name: 'MovieList',
    components: {
        Loader,
        Movie,
        MovieFormModal,
        MovieFilterForm,
    },
    data() {
        return {
            movies: [],
            next_page: null,
            previous_page: null,
            movies_count: null,
            loading: true,
            showModal: false,
            showFilters: false,
            currentQuery: {},
            currentFilters: {},
        }
    },
    mounted() {
        this.fetchMovies()
    },
    methods: {
        async fetchMovies({ url=null, query=null } = {}) {
            var url = url ? url : '/movies/'
            const finalQuery = query !== null ? query : this.currentQuery
            if (query !== null) {
                this.currentQuery = query
            }
            try {
              const response = await api.get(url, {params: finalQuery})
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
        handleUpdate(updatedMovie) {
          const index = this.movies.findIndex(m => m.id === updatedMovie.id)
          if (index !== -1) {
            this.movies.splice(index, 1, updatedMovie)
          }
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
                const response = await api.post('/movies/', formData)
                this.showModal = false
                this.movies.push(response.data)
                if (this.movies_count === 0) {this.movies_count = 1}
            } catch (error) {
                if (error.response && error.response.data) {
                    return Promise.reject(error.response.data)
                }
                console.log("Error while creating comment", error)
            }
        },
        applyFilters(filters) {
            this.currentFilters = filters
            this.fetchMovies({query: filters})
            this.showFilters = false
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
        font-size: 24px;
    }`
    .movies-list {
        grid: auto-flow;
        grid-cols: 2px;
        gap: 4px;
        p: 4px;
    }
    .pagination {
        padding-top: 50px;
        padding-bottom: 50px;
        text-align: center;
    }
    .pagination button {
        width: 100px;
        font-size: 16px;
    }
    .menu-buttons {
        display: flex;
        gap: 10px;
        padding-top: 20px;
        justify-content: end;
        padding-right: 80px;
    }
    .create-button:hover {
        fill: #c7ecee;
        cursor: pointer;
    }
    .filter-button:hover {
        fill: #c7ecee;
        cursor: pointer;
    }

</style>
