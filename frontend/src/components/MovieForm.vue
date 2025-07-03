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
        <button class="form-button" type="submit"> Send </button>
        <button class="form-button cancel" type="button" @click="$emit('cancel')"> Cancel </button>
    </form>
</template>
<script>
    import api from '@/services/api.js'
    export default {
        name: 'MovieForm',
        props: {
            onSubmit: Function,
        },
        data() {
            return {
                persons: [],
                form: {
                    title: '',
                    release_year: '',
                    cast: [],
                },
                errors: {},
            }
        },
        mounted() {
            this.fetchPersons()
        },
        methods: {
            async fetchPersons(){
                const response = await api.get('/movie-persons/')
                this.persons = response.data.results
            },
            async handleSubmit() {
                this.errors = {}
                try {
                    if (this.onSubmit) {
                            let payload
                            payload = {...this.form}
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
              }
            },
        },
    }
</script>
<style scoped>
</style>