<template>
<div class="modal-overlay">
    <div class="modal-content">
            <form @submit.prevent="submitFilters" class="filter-form">
                <div>
                    <label>Release Year: </label>
                    <input type="number" v-model="form.release_year" />
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
                        placeholder="Filter by director"
                    />
                </div>
                <div>
                    <label>Actor:</label>
                    <Multiselect
                        v-model="form.actor"
                        :options="persons"
                        :searchable="true"
                        :close-on-select="true"
                        :preserve-search="true"
                        label="name"
                        track-by="id"
                        placeholder="Filter by actor"
                    />
                </div>
                <div class='buttons-container'>
                    <button class="form-button" type="submit"> Send </button>
                    <button class="form-button cancel" type="button" @click="$emit('cancel')"> Cancel </button>
                </div>
            </form>
    </div>
</div>
</template>
<script>
    import Multiselect from 'vue-multiselect'
    import 'vue-multiselect/dist/vue-multiselect.min.css'
    import api from '@/services/api.js'
    export default {
        name: 'MovieFilterForm',
        components: {
            Multiselect,
        },
        props: {
            onSubmit: Function,
            currentFilters: {
                type: Object,
                default: () => ({})
            }
        },
        data() {
            return {
                persons: [],
                form: {
                    release_year: this.currentFilters.release_year || '',
                    director: this.currentFilters.director || null,
                    actor: this.currentFilters.actor || null,
                },
            }
        },
        async mounted() {
            await this.fetchPersons()
            if (this.form.actor) {
                this.form.actor = this.persons.find(p => p.id === this.form.actor)
            }
            if (this.form.director) {
                this.form.director = this.persons.find(p => p.id === this.form.director)
            }
        },
        methods: {
            async fetchPersons(){
                const response = await api.get('/movie-persons/')
                this.persons = response.data.results
            },
            submitFilters() {
                const clean = {}
                for (const key in this.form) {
                    if (this.form[key]) {
                        if (key == 'director' || key == 'actor') {
                            clean[key] = this.form[key].id
                        } else clean[key] = this.form[key] }
                }
                this.onSubmit(clean)
            },
        },
    }
</script>
<style scoped>
    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 8px;
    }
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .filter-form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
   .buttons-container {
        display: flex;
        align-content: center;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
   }
   .form-button {
        width: 80px;
   }
   .input {
        height: 25px;
        border: 1px solid #888;
   }
</style>