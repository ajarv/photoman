<template>
    <div id="viewer">
        <div class="inner">            
            <div class="nav-next" v-on:click="selectNext()"></div>
            <div class="nav-previous" v-on:click="selectPrev()"></div>
        </div>
        <div class="slide active" v-if="img">
            <div class="caption">                
                <h3>{{ img.title }} - {{img.caption}}</h3>
                <p> 
                    <a class="btn btn-primary" target="_blank" :href="img.metafield.image.imgix_url" role="button">Open</a>
                    <a class="btn btn-primary" target="_blank" :href="img.metafield.image.imgix_url" role="button" download>Download Small</a>
                    <a class="btn btn-primary" target="_blank" :href="img.metafield.image.imgix_url_orig" role="button" download>Download Large</a>
                    <button @click="checkVoiceCommand">Check Voice Command</button>
                </p>
            </div>
            <div class="image" v-bind:style='{ backgroundImage: "url(" + img.metafield.image.imgix_url + ")", backgroundSize: "cover",  backgroundPosition: "center" }'>
            </div>
        </div> 
    </div>
</template>

<script>
import {EventBus} from '../event_bus';
import axios from 'axios';
import SpeechCommands from '../speech'

export default {
    name: 'viewer',
    created() {
        EventBus.$on('loaded', (obj) => {
            this.img = obj;
            this.fetchMetadata();
        });
        EventBus.$on('caption', (caption) => {
            this.addCaption(caption)
        });
        EventBus.$on('delete', () => {
            this.deletePhoto()
        });
        EventBus.$on('star', () => {
            this.favPhoto()
        });
        this.checkVoiceCommand =  SpeechCommands.initialize(EventBus);

    },
    data () {
        return {
            img: null,
            years:[]
        }
    },
    methods: {
        fetchMetadata() {
            if (this.img == null) return;
            const img = this.img;
            const imageId = img.imageId
            axios.get('/api/metadata/'+imageId)
            .then(function (response) {
                console.log(response.data.result);
                if (response.data.status == 'ok' && response.data.result.length > 0 ){
                    img.caption = response.data.result[0].caption;
                }
            })
            .catch(function (error) {
                console.log(error);
            });

        },
        updateMetadata(attributes){
            if (this.img == null) return;
            const imageId = this.img.imageId

            attributes.updatedOn = new Date().toISOString()
            attributes.id = imageId

            axios.post('/api/metadata/'+imageId, attributes)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        addCaption(caption){
            this.updateMetadata({caption:caption})
            if (this.img != null) this.img.caption = caption
        },
        deletePhoto(){
            this.updateMetadata({toBeDeleted:true})
        },
        favPhoto(){
            this.updateMetadata({favorite:true})
        },
        selectNext() {
            EventBus.$emit('move', 1);
        },
        selectPrev() {
            EventBus.$emit('move', -1);
        }
    }
}
</script>