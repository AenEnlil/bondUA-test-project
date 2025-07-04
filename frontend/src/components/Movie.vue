<template>
  <div class="bg-white rounded-xl shadow p-4">
    <div class='movie-header'>
        <p>{{movie.id}}</p>
        <h2 class="text-xl font-bold">{{ movie.title }}</h2>
        <svg
            @click="showModal = true"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 32 32"
            class='button-icons'>
            <path d="M 23.90625 3.96875 C 22.859375 3.96875 21.8125 4.375 21 5.1875 L 5.1875 21 L 5.125 21.3125 L 4.03125 26.8125 L 3.71875 28.28125 L 5.1875 27.96875 L 10.6875 26.875 L 11 26.8125 L 26.8125 11 C 28.4375 9.375 28.4375 6.8125 26.8125 5.1875 C 26 4.375 24.953125 3.96875 23.90625 3.96875 Z M 23.90625 5.875 C 24.410156 5.875 24.917969 6.105469 25.40625 6.59375 C 26.378906 7.566406 26.378906 8.621094 25.40625 9.59375 L 24.6875 10.28125 L 21.71875 7.3125 L 22.40625 6.59375 C 22.894531 6.105469 23.402344 5.875 23.90625 5.875 Z M 20.3125 8.71875 L 23.28125 11.6875 L 11.1875 23.78125 C 10.53125 22.5 9.5 21.46875 8.21875 20.8125 Z M 6.9375 22.4375 C 8.136719 22.921875 9.078125 23.863281 9.5625 25.0625 L 6.28125 25.71875 Z"/>
        </svg>
        <svg
            @click="deleteMovie"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 48 48"
            class='button-icons'>
            <path d="M 24 4 C 20.704135 4 18 6.7041348 18 10 L 11.746094 10 A 1.50015 1.50015 0 0 0 11.476562 9.9785156 A 1.50015 1.50015 0 0 0 11.259766 10 L 7.5 10 A 1.50015 1.50015 0 1 0 7.5 13 L 10 13 L 10 38.5 C 10 41.519774 12.480226 44 15.5 44 L 32.5 44 C 35.519774 44 38 41.519774 38 38.5 L 38 13 L 40.5 13 A 1.50015 1.50015 0 1 0 40.5 10 L 36.746094 10 A 1.50015 1.50015 0 0 0 36.259766 10 L 30 10 C 30 6.7041348 27.295865 4 24 4 z M 24 7 C 25.674135 7 27 8.3258652 27 10 L 21 10 C 21 8.3258652 22.325865 7 24 7 z M 13 13 L 35 13 L 35 38.5 C 35 39.898226 33.898226 41 32.5 41 L 15.5 41 C 14.101774 41 13 39.898226 13 38.5 L 13 13 z M 20.476562 17.978516 A 1.50015 1.50015 0 0 0 19 19.5 L 19 34.5 A 1.50015 1.50015 0 1 0 22 34.5 L 22 19.5 A 1.50015 1.50015 0 0 0 20.476562 17.978516 z M 27.476562 17.978516 A 1.50015 1.50015 0 0 0 26 19.5 L 26 34.5 A 1.50015 1.50015 0 1 0 29 34.5 L 29 19.5 A 1.50015 1.50015 0 0 0 27.476562 17.978516 z"/>
        </svg>
    </div>
    <p class="text-sm text-gray-500">Release year: {{ movie.release_year }}</p>
    <p>Director: {{ director?.person_name || 'N/A' }}</p>

    <div v-if="actors.length !== 0" class="actors-dropdown">
        <details>
            <summary>Actors</summary>
            <ul class="actors-list">
                <li v-for="actor in actors" :key="actor.id">
                    {{actor.person_name}}
                </li>
            </ul>
        </details>
    </div>

    <div v-if="mode === 'detailed'" class="mt-2 text-gray-700">
      <p>detailed</p>
    </div>
  </div>
  <div v-if="showModal">
    <MovieFormModal :onSubmit="updateMovie" :movie="movie" @cancel="showModal = false"/>
  </div>
</template>

<script>
import api from '@/services/api.js'
import MovieFormModal from '@/components/MovieFormModal.vue'
export default {
  components: {
    MovieFormModal
  },
  emits: ['deleted', 'updated'],
  data() {
    return {
        showModal: false
    }
  },
  props: {
    movie: {
      type: Object,
      required: true,
    },
    mode: {
      type: String,
      default: 'list', // 'list' or 'details'
    },
  },
  computed: {
    director() {
        return this.movie.cast.find(person => person.role === 'director') || null
    },
    actors() {
        return this.movie.cast.filter(person => person.role === 'actor')
    },
  },
  methods: {
    async deleteMovie() {
      try {
        await api.delete(`/movies/${this.movie.id}/`)
        this.$emit('deleted', this.movie.id)
      } catch (err) {
        console.error('Error while deleting movie:', err)
      }
    },
    async updateMovie(payload) {
        try {
            const response = await api.patch(`/movies/${this.movie.id}/`, payload)
            this.showModal = false
            this.$emit('updated', response.data)
        } catch (err) {
            console.error('Error while deleting movie:', err)
        }
    },
  },
};
</script>
<style scoped>
    .button-icons {
        margin-top: 4px;
        height: 16px;
        cursor: pointer;
    }
    .actor-dropdown details {
        width: 100%;
        cursor: pointer;
        margin-bottom: 1rem;
    }
    .actors-list {
        display: flex;
        overflow-x: auto;
        gap: 1rem;
        padding: 0.5rem;
        white-space: nowrap;
        list-style: none;
    }
    .actors-list li {
        background: #f2f2f2;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        flex: 0 0 auto;
    }
</style>
