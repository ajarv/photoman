<template>
  <div>
    <v-app>
    <div id="main">
      <app-header></app-header>
      <thumbs></thumbs>
      <app-footer></app-footer>
    </div>
    <viewer></viewer>
    </v-app>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import Thumbs from './components/Thumbs.vue'
import Viewer from './components/Viewer.vue'

export default {
  name: 'app',
  components: {
    AppFooter,
    AppHeader,
    Thumbs,
    Viewer
  },
  created() {
          this.emitter.emit('global_loaded', {});
  },
}
</script>
