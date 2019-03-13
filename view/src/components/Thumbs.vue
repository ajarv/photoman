<template>
    <section id="thumbnails">
        <article v-for="(item, index) in items" v-bind:class="{ 'active': activeIndex == index }" v-bind:key="index">
            <a class="thumbnail" v-on:click="selectImage(item, index)">
                <img v-bind:src="item.metafield.image.imgix_url" alt="" />
            </a>
            <h2>{{ item.title }}</h2>
            <div v-html="item.content"></div>
        </article>
    </section>
</template>

<script>
import Cosmic from 'cosmicjs';
import * as Config from '../config';
import {EventBus} from '../event_bus';
import {_} from 'vue-underscore';
import axios from 'axios';

const bucket = { slug: Config.bucket };
const bu = "http://192.168.0.11:8084/";
const map = {}

function gx(flist){
    var rv = _.map(flist,(f)=>{
        return {
                "_id": "59833cb15ad4ceb321000925",
                "bucket": "59833ca15ad4ceb321000922",
                "slug": "beach",
                "title": ""+f,
                "content": "<p>"+f+"</p>",
                "metafield": {
                    "image": {
                        "imgix_url": bu+'S2000'+f,
                        "url": bu+'S0300'+f
                    }
                }
            };
    });
    return rv;
    // return [];
}

export default {
    name: 'thumbs',
    created() {
        var self = this;
        axios
            .get('http://192.168.0.11:8084/S2000__list.json')
            // .then(response => (this.s2000 = response))
            .then((response) => {
                var data = response.data;
                var s2000 = {data:_.groupBy(data.files, function(filename){ return filename.slice(0,11); }) };
                s2000.keys = _.keys(s2000.data);
                s2000.keys.sort();
                s2000.keys.reverse();
                self.s2000 = s2000;

            })
        
        Cosmic.getObjectType({ bucket }, { type_slug: 'photos' }, (err, res) => {
            this.cosmic_items = this.items = res.objects.all;
            EventBus.$emit('loaded', this.items[0]);
        });
        EventBus.$on('deploy', (n) => {
            n = n % this.s2000.keys.length; 
            console.log(n);
            this.n = n;
            this.items = gx(this.s2000.data[this.s2000.keys[n]]);
            EventBus.$emit('loaded', this.items[0]);
        });
        EventBus.$on('move', (dir) => {
            this.activeIndex = this.activeIndex + dir;
            if (dir > 0 && this.activeIndex >= this.items.length) {
                this.activeIndex = 0;
            }
            if (dir < 0 && this.activeIndex < 0) {
                this.activeIndex = this.items.length - 1;
            }
            EventBus.$emit('loaded', this.items[this.activeIndex]);
        });

    },
    data () {
        return {
            items: [],
            activeIndex: 0,
            cosmic_items : null,
            s2000: null
        }
    },
    methods: {
        selectImage (itm, index) {
            EventBus.$emit('loaded', itm);
            this.activeIndex = index;
        }
    }
}
</script>