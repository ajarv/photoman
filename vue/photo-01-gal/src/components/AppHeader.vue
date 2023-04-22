<template>
    <header id="header">
        <h1>{{ header }}</h1>
        <div v-html="text"></div>
    </header>
</template>

<script>

export default {
    name: 'app-header',
    created() {
        this.emitter.on('global_loaded', (obj) => {
            this.header = "Photo Tags";
            this.text = "all";
            this.twitter = "#x";
            this.instagram = "#x";
            this.github ="#x";
            this.email = 'mailto:' + "x";
        });
    },
    data () {
        return {
            text: null,
            twitter: '',
            instagram: '',
            github: '',
            email: '',
            header: ''
        }
    }
}
</script>