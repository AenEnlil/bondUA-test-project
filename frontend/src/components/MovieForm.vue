<template>
    <form @submit.prevent="handleSubmit" class="comment-form">
        <div>
            <label>Title: </label>
            <input type="text" v-model="form.title" required />
            <div v-if="errors.title">
                <ul>
                    <li v-for="(error, index) in errors.title" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Release Year: </label>
            <input type="number" v-model="form.release_year" required />
            <div v-if="errors.release_year">
                <ul>
                    <li v-for="(error, index) in errors.release_year" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Director: </label>
            <Multiselect
                v-model="form.director"
                :options="persons"
                :searchable="true"
                :close-on-select="true"
                :show-labels="false"
                label="name"
                track-by="id"
                placeholder="Select a director"
            />
            <div v-if="errors.director">
                <ul>
                    <li v-for="(error, index) in errors.director" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Actors:</label>
            <Multiselect
                v-model="form.actors"
                :options="persons"
                :multiple="true"
                :searchable="true"
                :close-on-select="false"
                :clear-on-select="false"
                :preserve-search="true"
                label="name"
                track-by="id"
                placeholder="Select actors"
            />
            <div v-if="errors.actors">
                <ul>
                    <li v-for="(error, index) in errors.actors" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <button class="form-button" type="submit"> Send </button>
        <button class="form-button cancel" type="button" @click="$emit('cancel')"> Cancel </button>
    </form>
</template>
<script>
    import Multiselect from 'vue-multiselect'
    import 'vue-multiselect/dist/vue-multiselect.min.css'
    import api from '@/services/api.js'
    export default {
        name: 'MovieForm',
        components: {
            Multiselect,
        },
        props: {
            onSubmit: Function,
            movie: {
                type: Object,
                default: null,
            }
        },
        data() {
            return {
                persons: [],
                form: {
                    title: '',
                    release_year: '',
                    director: null,
                    actors: [],
                },
                errors: {},
            }
        },
        mounted() {
            this.fetchPersons()
            if (this.movie) {
                this.setFormFromMovie(this.movie)
            }
        },
        methods: {
            async fetchPersons(){
                const response = await api.get('/movie-persons/')
                this.persons = response.data.results
            },
            setFormFromMovie(movie) {
                this.form.title = movie.title || ''
                this.form.release_year = movie.release_year || ''

                if (movie.cast) {
                    this.form.director = movie.cast
                        .filter(p => p.role === 'director')
                        .map(p => ({'id': p.person_id, 'name': p.person_name}))[0] || null
                    this.form.actors = movie.cast
                        .filter(p => p.role === 'actor')
                        .map(p => ({'id': p.person_id, 'name': p.person_name}))
                }
            },
            prepareCast() {
                const temp = []
                if (this.form.director) {
                    temp.push({'person_id': this.form.director.id, 'role': 'director'})
                }
                if (this.form.actors) {
                    for (const actor of this.form.actors) {
                        temp.push({'person_id': actor.id, 'role': 'actor'})
                    }
                }
                return temp
            },
            async handleSubmit() {
                this.errors = {}
                if (!this.form.director) {
                    this.errors.director = ['Please select a director'] }
                if (!this.form.actors || this.form.actors.length === 0) {
                    this.errors.actors = ['Please select at least one actor'] }
                if (Object.keys(this.errors).length > 0) {
                    return }
                try {
                    if (this.onSubmit) {
                            const cast = this.prepareCast()
                            const payload = {
                                title: this.form.title,
                                release_year: this.form.release_year,
                                cast: cast
                            }
                            await this.onSubmit(payload)
                        }
                    this.clearForm()
                } catch (serverErrors) {
                    this.errors = serverErrors
                }
            },
            clearForm() {
              this.form = {
                title: '',
                release_year: '',
                director: null,
                actors: [],
              }
            },
        },
    }
</script>
<style scoped>
</style>