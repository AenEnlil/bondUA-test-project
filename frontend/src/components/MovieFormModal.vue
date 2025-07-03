<template>
<div class="modal-overlay">
    <div class="modal-content">
        <MovieForm :onSubmit="onSubmit" @cancel="handleCancel"/>
    </div>
</div>
</template>
<script>
import MovieForm from '@/components/MovieForm.vue'
export default {
    name: 'MovieFormModal',
    components: {
        MovieForm
    },
    props: {
        onSubmit: Function,
    },
    methods: {
        handleCancel() {
            this.$emit('cancel')
        },
    }
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
</style>
