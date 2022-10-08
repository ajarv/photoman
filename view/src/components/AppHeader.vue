<template>
    <header id="header">
        <!-- <h1>{{ header }}</h1> -->
        <!-- <div v-html="text"></div> -->
        <!-- <ul class="icons">
            <li><a :href="twitter" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
            <li><a :href="instagram" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
            <li><a :href="github" class="icon fa-github"><span class="label">Github</span></a></li>
            <li><a :href="email" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
        </ul> -->
        <div  v-if="loggedin">
            <div>
                <button v-for="(year, index) in years" v-bind:class="{ 'active': year_ == year }" v-bind:key="index" v-on:click="gotoYear(year)" >{{year}}</button>
                <hr/>
            </div>
            <div>
                <button v-for="(month, index) in months" v-bind:class="{ 'active': month_ == month }" v-bind:key="index" v-on:click="gotoMonth(month)" >{{month}}</button>
                <hr/>
            </div>
            <div>
                <button v-for="(day, index) in days" v-bind:class="{ 'active': day_ == day }" v-bind:key="index" v-on:click="gotoDay(day)">{{day}}</button>
                <hr/>
            </div>
            <button v-on:click="logout">logout</button>
        </div>
        <div  v-else>
            <input type="password" v-model="password" @change="checklogin" >
        </div>
    </header>
</template>

<script>
import {EventBus} from '../event_bus';
import axios from 'axios';

const bu = "http://libra:7001";

function getImageObjects(flist){
    var rv = _.map(flist,(f)=>{
        return {
                "_id": "59833cb15ad4ceb321000925",
                "bucket": "59833ca15ad4ceb321000922",
                "slug": "beach",
                "title": ""+f,
                "content": "<p>"+f+"</p>",
                "metafield": {
                    "image": {
                        "imgix_url": bu+'/S2000'+f,
                        "imgix_url_orig": bu+'/ORIGN'+f,
                        "url": bu+'/S0300'+f
                    }
                }
            };
    });
    return rv;
}

export default {
    name: 'app-header',
    created() {
        EventBus.$on('global_loaded', (obj) => {
            this.header = obj.title;
            this.text = obj.metafield.tagline.value;
            this.twitter = obj.metafield.twitter.value;
            this.instagram = obj.metafield.instagram.value;
            this.github = obj.metafield.github.value;
            this.email = 'mailto:' + obj.metafield.email.value;

        });
       EventBus.$on('year', (year) => {
           this.year_ = year;
           var months =  _.uniq(_.map(_.filter(this.s2000.keys,(key) => {return key.startsWith('/'+year)}), (key) => { return key.split('/')[2]}));
            months.sort();
            months.reverse();
            this.months = months;
            this.gotoMonth(months[0]);

       })
       EventBus.$on('month', (month) => {
           this.month_ = month;
           
           var days =  _.uniq(_.map(_.filter(this.s2000.keys,(key) => {return key.startsWith('/'+this.year_+'/'+month)}), (key) => { return key.split('/')[3]}));
            days.sort();
            days.reverse();
            this.days = days;
            this.gotoDay(days[0]);
       })
        EventBus.$on('day', (day) => {
           this.day_ = day;
           var key = '/'+this.year_+'/'+this.month_+'/'+this.day_;
           var images = this.s2000.data[key]
            images.sort();
            images.reverse();
            var items = getImageObjects(images);
            EventBus.$emit('images', items);
       })
       

    },
    data () {
        return {
            text: null,
            twitter: '',
            instagram: '',
            github: '',
            email: '',
            header: '',
            years:[],
            year_:null,
            months:[],
            month_:null,
            days:[],
            day_:null,
            s2000:null,
            ix:0,
            loggedin:false,
            password:''
        }
    }, methods: {
        logout:  function(event){
            this.loggedin = false;
            EventBus.$emit('images', []);
        },
        checklogin: function (event){
            if (this.password == '11339'){
                this.loggedin = true;
                var self = this;
                axios
                    .get(bu + '/S2000__list.json')
                    // .then(response => (this.s2000 = response))
                    .then((response) => {
                        var data = response.data;
                        var s2000 = {data:_.groupBy(data.files, function(filename){ return filename.slice(0,11); }) };
                        s2000.keys = _.keys(s2000.data);
                        s2000.keys.sort();
                        s2000.keys.reverse();
                        self.s2000 = s2000;

                        var years =  _.uniq(_.map(s2000.keys, (key) => { return key.split('/')[1]}))
                        years.sort();
                        years.reverse();
                        self.years = years;
                        self.gotoYear(years[0]);
                    })
            }
        },
        gotoYear: (year) =>{
            EventBus.$emit('year', year);
        },
        gotoMonth: (month) =>{
            EventBus.$emit('month', month);
        },
        gotoDay: (day) =>{
            EventBus.$emit('day', day);
        }
        


    }
}
</script>