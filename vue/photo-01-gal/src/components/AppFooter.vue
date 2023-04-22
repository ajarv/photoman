<template>
    <footer id="footer">
        <div v-html="text"></div>
    </footer>
</template>

<script>

export default {
    name: 'app-footer',
    created() {
        this.emitter.on('global_loaded', (obj) => {
            this.text = obj.metafield.footer.value;
        });
    },
    data () {
        return {
            text: null
        }
    }
}
</script>