<template>
  <v-app>
    <div id="viewer">
      <div class="inner">
        <div class="nav-next" v-on:click="selectNext()"></div>
        <div class="nav-previous" v-on:click="selectPrev()"></div>
      </div>
      <div class="slide active" v-if="img">
        <div class="caption">
          <h2>{{ title }}</h2>
          <v-row justify="space-around" align="center">
            <v-chip class="ma-2" v-for="tag in img.tags">
              {{ tag }}
            </v-chip>
            <v-text-field v-model="new_tag" label="New Tag"></v-text-field>
            <v-btn size="x-small" @click="add_tag">Add</v-btn>
          </v-row>
          <v-btn class="my-1" @click="toggle_tag('blurred')" :style="{
              backgroundColor: blurred ? 'black !important' : '',
              color: blurred ? 'white !important' : 'black',
            }">
            Blurred
          </v-btn>
          <v-btn class="my-1" @click="toggle_tag('favorite')" :style="{
              backgroundColor: favorite ? 'orange !important' : '',
              color: favorite ? 'yellow !important' : 'black',
            }">
            Favorite
          </v-btn>
          <v-btn class="my-1" @click="toggle_tag('ugly')" :style="{
              backgroundColor: ugly ? '#b7702d !important' : '',
              color: ugly ? 'cyan !important' : 'black',
            }">
            Ugly
          </v-btn>
          <v-btn class="my-1" @click="toggle_tag('repeat')" :style="{
              backgroundColor: repeat ? '#b7702d !important' : '',
              color: repeat ? 'cyan !important' : 'black',
            }">
            Repeat
          </v-btn>
          <button @click="toggle_tag('rot-right')">Rotate Right</button>
          <button @click="toggle_tag('rot-left')">Rotate Left</button>
          <br />
          <a :href="img.url_2000" target="_blank" role="button">
            <v-btn class="my-1"> Open </v-btn>
          </a>
          <a :href="img.url_2000" target="_blank" role="button" :download="img.file_name">
            <v-btn class="my-1"> Download Small </v-btn>
          </a>
          <a :href="img.url_ORIG" target="_blank" role="button" :download="'O' + img.file_name">
            <v-btn class="my-1"> Download Large </v-btn>
          </a>
        </div>
        <div>
          <a class="btn btn-primary" target="_blank" :href="img.url_2000" role="button">Open</a>
          <a class="btn btn-primary" target="_blank" :href="img.url_2000" role="button" download>Download Small</a>
          <a class="btn btn-primary" target="_blank" :href="img.url_ORIG" role="button" download>Download Large</a>
        </div>
        <div class="image" v-bind:style="{
            backgroundImage: 'url(http://libra:7001/S2000/' + img.key + ')',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }"></div>
      </div>
    </div>
  </v-app>
</template>

<script>
export default {
  name: "viewer",
  created() {
    this.emitter.on("loaded", (item) => {
      if (item === undefined) return
      this.img = item;
      this.title = item.file_name;
      this.blurred =
        item.tags.filter((tag) => tag == "ns0:blurred:1").length == 1;
      this.ugly = item.tags.filter((tag) => tag == "ns0:ugly:1").length == 1;
      this.repeat = item.tags.filter((tag) => tag == "ns0:repeat:1").length == 1;
      this.favorite =
        item.tags.filter((tag) => tag == "ns0:favorite:1").length == 1;
    });
  },
  data() {
    return {
      new_tag: "",
      img: null,
      title: "",
      blurred: 0,
    };
  },
  methods: {
    add_tag(){
      if (this.new_tag != ""){
        this.emitter.emit("add_tag",this.new_tag)
        this.new_tag=""
      }
    },
    selectNext() {
      this.emitter.emit("move", 1);
    },
    selectPrev() {
      this.emitter.emit("move", -1);
    },
    toggle_tag(tag) {
      this.emitter.emit("toggle_tag", tag);
    },
  },
};
</script>