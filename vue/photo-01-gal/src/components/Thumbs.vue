<template>
  <section id="thumbnails">
    <div class="controls">
      <h4>Available {{ count_available }}</h4>
      <v-slider
        v-model="year_index"
        :min="0"
        :max="year_tag_list.length - 1"
        :step="1"
        :label="'Year ' + year_selected"
        track-color="orange"
      >
      </v-slider>
      <v-slider
        v-model="month_index"
        :min="0"
        :max="month_tag_list.length - 1"
        :step="1"
        :label="'Month ' + month_selected"
        track-color="green"
      >
      </v-slider>
      <v-slider
        v-model="offset"
        :min="0"
        :max="count_available"
        :step="1"
        :label="'Index ' + offset + '/'+count_available"
        track-color="blue"
      >
      </v-slider>
      <button @click="load_photos(uprevious)">Previous</button>
      <input v-model="offset" class="index" />
      <button @click="load_photos(unext)">Next</button>
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
const BASE_BUCKET_URL = "http://libra:7001";
const API_BASE_URL = "http://libra:8000/api";
export default {
  name: "thumbs",
  created() {
    this.emitter.on("toggle_tag", (tkey) => {
      let item = this.items[this.activeIndex];
      let durl = `${API_BASE_URL}/api/obj/${item.id}/`;
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
          this.emitter.emit("loaded", item);
        });
    });
    this.emitter.on("move", (dir) => {
      this.activeIndex = this.activeIndex + dir;

      if (dir > 0 && this.activeIndex >= this.items.length) {
        this.load_photos(this.unext);
        this.activeIndex = 0;
      }
      if (dir < 0 && this.activeIndex < 0) {
        this.load_photos(this.uprevious);
        this.activeIndex = this.items.length - 1;
      }
      this.emitter.emit("loaded", this.items[this.activeIndex]);
    });
  },
  data() {
    return {
      items: [],
      year_index: 0,
      year_tag_list: [],
      year_selected: "",
      month_index: 0,
      month_tag_list: [],
      month_selected: "",
      uprevious: "",
      unext: "",
      offset: 0,
      activeIndex: 0,
      count_available: 0,
    };
  },
  watch: {
    // whenever question changes, this function will run
    year_index(old_index, new_index) {
      this.refresh_thumbs();
    },
    month_index(old_index, new_index) {
      this.refresh_thumbs();
    },
    offset(old_index, new_index) {
      this.refresh_thumbs();
      return true;
    },
  },
  methods: {
    selectImage(item, index) {
      this.emitter.emit("loaded", item);
      this.activeIndex = index;
    },
    load_photos(durl) {
      const xurl = new URL(durl);
      let offset = xurl.searchParams.get("offset");
      this.offset = offset != null ? offset : 0;
      axios.get(durl).then((response) => {
        this.items = response.data.results;
        if (this.items.length == 0) return;
        console.log(response.data);
        this.items.forEach((item) => {
          item["url_0300"] = `${BASE_BUCKET_URL}/S0300/${item.key}`;
          item["url_2000"] = `${BASE_BUCKET_URL}/S2000/${item.key}`;
          item["url_ORIG"] = `${BASE_BUCKET_URL}/ORIGN/${item.key}`;
          item["file_name"] = item.key.replace("/", "_");
        });
        this.uprevious = response.data.previous;
        this.unext = response.data.next;
        this.count_available = response.data.count;
        // this.offset = Math.min(this.count_available - 1, this.offset);
      });
    },
    load_year_tags() {
      const xurl = new URL(`${API_BASE_URL}/tag-list/?tag_query=c_year`);
      axios.get(xurl).then((response) => {
        this.year_tag_list = response.data.results;
        this.year_index = this.year_tag_list.length - 1;
        this.load_month_tags();
      });
    },
    load_month_tags() {
      const xurl = new URL(`${API_BASE_URL}/tag-list/?tag_query=c_month`);
      axios.get(xurl).then((response) => {
        this.month_tag_list = response.data.results;
        this.month_index = this.month_tag_list.length - 1;
        this.refresh_thumbs();
      });
    },
    refresh_thumbs() {
      let qparams = [];
      if (this.year_tag_list.length > 0) {
        let year_tag = this.year_tag_list[this.year_index];
        this.year_selected = year_tag.split(":")[2];
        qparams.push(`tag_query=${year_tag}`);
      }
      if (this.month_tag_list.length > 0) {
        let month_tag = this.month_tag_list[this.month_index];
        this.month_selected = month_tag.split(":")[2];
        qparams.push(`tag_query=${month_tag}`);
      }
      let purl = `${API_BASE_URL}/obj/`;
      if (qparams.length > 0) {
        purl += "?" + qparams.join("&");
      }
      // console.log(purl)
      this.load_photos(purl);
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
    // this.load_photos(API_BASE_URL+"/obj/?offset=0");
    this.load_year_tags();
    window.addEventListener("keyup", this.handlekey);
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.handlekey);
  },
};
</script>