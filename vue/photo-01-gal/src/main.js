import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import mitt from 'mitt';

// Vuetify
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
})
const emitter = mitt();

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.config.globalProperties.emitter = emitter;
app.mount('#app')
