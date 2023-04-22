<template>
  <section id="thumbnails">
    <div class="controls">
      <h4>Available {{ count_available }}</h4>
      <div>
        <input
          class="slider"
          v-model="offset"
          type="range"
          @change="set_offset"
          min="0"
          :max="count_available"
          style="width: 100%"
        />
      </div>
      <button @click="doUrl(uprevious)">Previous</button>
      <input v-model="offset" @change="set_offset" class="index" />
      <button @click="doUrl(unext)">Next</button>
    </div>
    <br />
    <article
      v-for="(item, index) in items"
      :key="item.key"
      v-bind:class="{ active: activeIndex == index }"
    >
      <a class="thumbnail" v-on:click="selectImage(item, index)">
        <img v-bind:src="item.url_0300" alt="" />
      </a>
    </article>
  </section>
</template>
<style scoped>
.controls {
  display: inline-block;
}
.controls .index {
  width: 100px;
}
</style>
<script>
import axios from "axios";
const BASE_BUCKET_URL = "http://libra:7001"
export default {
  name: "thumbs",
  created() {
    this.emitter.on("toggle_tag", (tkey) => {
      let item = this.items[this.activeIndex];
      let durl = `http://libra:8000/api/obj/${item.id}/`;
      let needs_new = true;
      for (var i = 0; i < item.tags.length; i++) {
        let tag = item.tags[i];
        let tag_toks = tag.split(":");
        if (tag_toks.length > 1 && tag_toks[1] == tkey) {
          let tval = tag_toks.length > 2 && tag_toks[2] == "1" ? "0" : "1";
          item.tags[i] = `ns0:${tkey}:${tval}`;
          needs_new = false;
          break;
        }
      }
      if (needs_new) {
        item.tags.push(`ns0:${tkey}:1`);
      }
      axios
        .put(durl, item, {
          headers: {
            authorization: "Token efdc792bcdaadc420d2c0ea680173b73d682c6d4",
          },
        })
        .then((response) => {
          console.log(response);
          this.emitter.emit("loaded", item);
        });
    });
    this.emitter.on("move", (dir) => {
      this.activeIndex = this.activeIndex + dir;

      if (dir > 0 && this.activeIndex >= this.items.length) {
        this.doUrl(this.unext);
        this.activeIndex = 0;
      }
      if (dir < 0 && this.activeIndex < 0) {
        this.doUrl(this.uprevious);
        this.activeIndex = this.items.length - 1;
      }
      this.emitter.emit("loaded", this.items[this.activeIndex]);
    });
  },
  data() {
    return {
      items: [],
      uprevious: "",
      unext: "",
      offset: 10000,
      activeIndex: 0,
      count_available: 0,
    };
  },
  methods: {
    selectImage(item, index) {
      this.emitter.emit("loaded", item);
      this.activeIndex = index;
    },
    set_offset(e) {
      let durl = `http://libra:8000/api/obj/?offset=${e.target.value}`;
      this.doUrl(durl);
    },
    doUrl(durl) {
      const xurl = new URL(durl);
      let offset = xurl.searchParams.get("offset");
      console.log(offset);
      this.offset = offset;
      axios.get(durl).then((response) => {
        this.items = response.data.results;
        this.items.forEach(item => {
          item["url_0300"] = `${BASE_BUCKET_URL}/S0300/${item.key}`
          item["url_2000"] = `${BASE_BUCKET_URL}/S2000/${item.key}`
          item["url_ORIG"] = `${BASE_BUCKET_URL}/ORIGN/${item.key}`
          item["file_name"] = item.key.replace('/', '_')
        });
        this.uprevious = response.data.previous;
        this.unext = response.data.next;
        this.count_available = response.data.count;
      });
    },
    handlekey(e) {
      if (e.key === "ArrowLeft") {
        this.emitter.emit("move", -1);
      }
      if (e.key === "ArrowRight") {
        this.emitter.emit("move", 1);
      }
    },
  },
  mounted() {
    this.doUrl("http://libra:8000/api/obj/?offset=50200");
    window.addEventListener("keyup", this.handlekey);
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.handlekey);
  },
};
</script>