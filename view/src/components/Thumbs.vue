<template>
    <section id="thumbnails">
        <article v-for="(item, index) in items" v-bind:class="{ 'active': activeIndex == index }" v-bind:key="index">
            <a class="thumbnail" v-on:click="selectImage(item, index)">
                <img v-bind:src="item.metafield.image.url" alt="" />
                <!-- <img v-bind:id="'imix-'+index" alt="" /> -->
            </a>
            <h2>{{ item.title }}</h2>
            <div v-html="item.content"></div>
        </article>
    </section>
</template>

<script>
import {EventBus} from '../event_bus';

export default {
    name: 'thumbs',
    created() {
        EventBus.$on('images', (items) => {
            this.items = items;
            this.activeIndex= 0;
            EventBus.$emit('loaded', this.items[this.activeIndex]);
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
            activeIndex: 0
        }
    },
    methods: {
        loadTn(ix){
            let ele = document.getElementById('imix-'+ix)
            if(ele) ele.src = item.metafield.image.url
        },
        selectImage (itm, index) {
            EventBus.$emit('loaded', itm);
            this.activeIndex = index;
        }
    }
}
</script>