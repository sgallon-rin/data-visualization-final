<template>
  <v-layout row wrap>

    <v-flex xs12 pa-1>
      <v-toolbar color="white" light>
        <v-toolbar-title>Final Project</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <div>
            <h3 class="title mb-0">China Pollution Data of All Places on a Certain Day</h3>
          </div>
        </v-card-title>

        <v-card-text>
          <v-label>Select Date (from 2013-01-01 to 2018-12-31)</v-label>
        </v-card-text>
        <v-card-actions>
          <date-picker v-model="input.all_pollution_date" type="date" :min="min_date" :max="max_date"/>
        </v-card-actions>

        <v-card-actions>
          <v-select
              :items="pollutionVariantList"
              label="Select Pollution Variant"
              v-model="input.all_pollution_variant"
          ></v-select>
        </v-card-actions>

        <v-card-text>
          <section v-if="errored_all_pollution">
            <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
          </section>
          <section v-else>
            <div v-if="loading_all_pollution">Loading...</div>
            <div v-else>Successfully loaded data (length: {{ all_pollution_data.length }})</div>
          </section>
        </v-card-text>

      </v-card>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <span class="title">China Pollution Data of {{ all_pollution_variant }} on {{ all_pollution_date }}</span>
        </v-card-title>

        <v-card-text>
          <v-text-field
              v-model="search1"
              append-icon="search"
              label="Search (Type something in this box to view data)"
              single-line
              hide-details
              outline
          ></v-text-field>
          <v-data-table
              :headers="headers"
              :items="all_pollution_data"
              :search="search1"
          >
            <template v-slot:items="props">
              <td class="text-xs-center">{{ props.item.date }}</td>
              <td class="text-xs-center">{{ props.item.long }}</td>
              <td class="text-xs-center">{{ props.item.lat }}</td>
              <td class="text-xs-center">{{ props.item.pm25 }}</td>
              <td class="text-xs-center">{{ props.item.pm10 }}</td>
              <td class="text-xs-center">{{ props.item.so2 }}</td>
              <td class="text-xs-center">{{ props.item.no2 }}</td>
              <td class="text-xs-center">{{ props.item.co }}</td>
              <td class="text-xs-center">{{ props.item.o3 }}</td>
              <td class="text-xs-center">{{ props.item.u }}</td>
              <td class="text-xs-center">{{ props.item.v }}</td>
              <td class="text-xs-center">{{ props.item.temp }}</td>
              <td class="text-xs-center">{{ props.item.rh }}</td>
              <td class="text-xs-center">{{ props.item.psfc }}</td>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <div>
            <h3 class="title mb-0">China Pollution Map of {{ all_pollution_variant }} on {{ all_pollution_date }}</h3>
          </div>
        </v-card-title>

        <v-card-text>
          <map-color-legend :display_key="all_pollution_display_key"
                            :pollution_data="all_pollution_data"
                            :title="all_pollution_variant_title"
          ></map-color-legend>
        </v-card-text>

        <v-card-text ref="chinaMapContainer">
          <china-map :height="container.height"
                     :width="container.width"
                     :display_key="all_pollution_display_key"
                     :pollution_data="all_pollution_data">
          </china-map>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <div>
            <h3 class="title mb-0">China Pollution Data at a Certain Place in a Certain Date Interval</h3>
          </div>
        </v-card-title>

        <v-card-text>
          <v-label>Select Date (from 2013-01-01 to 2018-12-31)</v-label>
        </v-card-text>
        <v-card-actions>
          <date-picker v-model="input.place_pollution_date_interval" type="date"
                       :range="range" :min="min_date" :max="max_date"/>
        </v-card-actions>

        <v-card-actions>
          <v-select
              :items="pollutionVariantList"
              label="Select Pollution Variant"
              v-model="input.place_pollution_variant"
          ></v-select>
        </v-card-actions>

        <v-layout row wrap>
          <v-flex xs12 sm5 md4 pa-1>
            <v-text-field
                label="Longitude"
                outline
                v-model="input.place_long"
                type="number"
                min="0"
                step="0.01"
                max="180"
            ></v-text-field>
          </v-flex>
          <v-flex xs12 sm5 md4 pa-1>
            <v-text-field
                label="Latitude"
                outline
                v-model="input.place_lat"
                type="number"
                min="0"
                step="0.01"
                max="90"
            ></v-text-field>
          </v-flex>
          <v-flex xs6 sm2 md3 pa-1>
            <v-btn @click="changePlace">
              Apply
            </v-btn>
          </v-flex>
        </v-layout>

        <v-card-text>
          <section v-if="errored_place_pollution">
            <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
          </section>
          <section v-else>
            <div v-if="loading_place_pollution">Loading... (If you keep seeing this, press APPLY to reload)</div>
            <div v-else-if="place_pollution_data_empty">Got no data, please check whether the coordinate is available!</div>
            <div v-else>Successfully loaded data (length: {{ place_pollution_data.length }})</div>
          </section>
        </v-card-text>

      </v-card>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <span class="title">
            Pollution Data of {{ place_pollution_variant }}
            during {{ place_pollution_date_interval }}
            at Longitude {{ place_long }}, Latitude {{ place_lat }}
          </span>
        </v-card-title>

        <v-card-text>
          <v-text-field
              v-model="search2"
              append-icon="search"
              label="Search (Type something in this box to view data)"
              single-line
              hide-details
              outline
          ></v-text-field>
          <v-data-table
              :headers="headers"
              :items="place_pollution_data"
              :search="search2"
          >
            <template v-slot:items="props">
              <td class="text-xs-center">{{ props.item.date }}</td>
              <td class="text-xs-center">{{ props.item.long }}</td>
              <td class="text-xs-center">{{ props.item.lat }}</td>
              <td class="text-xs-center">{{ props.item.pm25 }}</td>
              <td class="text-xs-center">{{ props.item.pm10 }}</td>
              <td class="text-xs-center">{{ props.item.so2 }}</td>
              <td class="text-xs-center">{{ props.item.no2 }}</td>
              <td class="text-xs-center">{{ props.item.co }}</td>
              <td class="text-xs-center">{{ props.item.o3 }}</td>
              <td class="text-xs-center">{{ props.item.u }}</td>
              <td class="text-xs-center">{{ props.item.v }}</td>
              <td class="text-xs-center">{{ props.item.temp }}</td>
              <td class="text-xs-center">{{ props.item.rh }}</td>
              <td class="text-xs-center">{{ props.item.psfc }}</td>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <div>
            <h3 class="title mb-0">
              Pollution Line Plot of {{ place_pollution_variant }}
              during {{ place_pollution_date_interval }}
              at Longitude {{ place_long }}, Latitude {{ place_lat }}
            </h3>
          </div>
        </v-card-title>

        <v-card-text ref="pollutionLinePlotContainer">
          <pollution-line-plot :height="container.height"
                     :width="container.width"
                     :display_key="place_pollution_display_key"
                     :pollution_data="place_pollution_data">
          </pollution-line-plot>
        </v-card-text>
      </v-card>
    </v-flex>

  </v-layout>
</template>

<script>
import axios from "axios";
import DatePicker from '@hyjiacan/vue-datepicker';
import '@hyjiacan/vue-datepicker/dist/datepicker.css';
import ChinaMap from "../components/ChinaMap";
import MapColorLegend from "../components/MapColorLegend";
import PollutionLinePlot from "../components/PollutionLinePlot";

export default {
  name: "final",
  components: {PollutionLinePlot, MapColorLegend, ChinaMap, DatePicker},
  data: () => {
    return {
      pollutionVariantList: ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "U", "V", "TEMP", "RH", "PSFC"],
      variant2key: {
        "PM2.5": "pm25",
        "PM10": "pm10",
        "SO2": "so2",
        "NO2": "no2",
        "CO": "co",
        "O3": "o3",
        "U": "u",
        "V": "v",
        "TEMP": "temp",
        "RH": "rh",
        "PSFC": "psfc"
      },
      variant2title: {
        "PM2.5": "PM2.5(μg/m3)",
        "PM10": "PM10(μg/m3)",
        "SO2": "SO2(μg/m3)",
        "NO2": "NO2(μg/m3)",
        "CO": "CO(μg/m3)",
        "O3": "O3(μg/m3)",
        "U": "U(m/s)",
        "V": "V(m/s)",
        "TEMP": "TEMP(K)",
        "RH": "RH(%)",
        "PSFC": "PSFC(Pa)"
      },
      container: {
        width: 0,
        height: 0
      },
      // for resizing diagram only after resizing is finished
      resizeID: null,
      // load data
      // 1 - all, one day
      all_pollution_data: null,
      loading_all_pollution: true,
      errored_all_pollution: false,
      all_pollution_variant: "PM2.5",
      all_pollution_variant_title: "PM2.5(μg/m3)",
      all_pollution_display_key: "pm25",
      all_pollution_date: '2013-01-01',
      // 2 - one point, date interval
      place_pollution_data: null,
      place_pollution_data_empty: true,
      loading_place_pollution: true,
      errored_place_pollution: false,
      place_pollution_variant: "PM2.5",
      place_pollution_variant_title: "PM2.5(μg/m3)",
      place_pollution_display_key: "pm25",
      place_pollution_date_interval: ['2013-01-01', '2013-01-31'],
      place_long: 109.25,
      place_lat: 18.48,
      // for DatePicker
      min_date: '2013-01-01',
      max_date: '2018-12-31',
      range: true,
      // for table
      search1: "",
      search2: "",
      headers: [
        {text: "Date", value: "date", align: 'center'},
        {text: "Longitude(°E)", value: "long", align: 'center'},
        {text: "Latitude(°N)", value: "lat", align: 'center'},
        {text: "PM2.5(μg/m3)", value: "pm25", align: 'center'},
        {text: "PM10(μg/m3)", value: "pm10", align: 'center'},
        {text: "SO2(μg/m3)", value: "so2", align: 'center'},
        {text: "NO2(μg/m3)", value: "no2", align: 'center'},
        {text: "CO(μg/m3)", value: "co", align: 'center'},
        {text: "O3(μg/m3)", value: "o3", align: 'center'},
        {text: "U(m/s)", value: "u", align: 'center'},
        {text: "V(m/s)", value: "v", align: 'center'},
        {text: "TEMP(K)", value: "temp", align: 'center'},
        {text: "RH(%)", value: "rh", align: 'center'},
        {text: "PSFC(Pa)", value: "psfc", align: 'center'},
      ],
      // for input watch
      input: {
        all_pollution_date: '2013-01-01',
        all_pollution_variant: "PM2.5",
        place_pollution_date_interval: ['2013-01-01', '2013-01-31'],
        place_pollution_variant: "PM2.5",
        place_long: 109.25,
        place_lat: 18.48,
      }
    }
  },
  watch: {
    // 1
    'input.all_pollution_date': function (val) {
      // console.log(val)
      this.all_pollution_date = val
      this.read_all_pollution_data_daily(val)
    },
    'input.all_pollution_variant': function (val) {
      // console.log(val)
      this.all_pollution_variant = val
      this.all_pollution_display_key = this.variant2key[this.all_pollution_variant]
      this.all_pollution_variant_title = this.variant2title[this.all_pollution_variant]
    },
    // 2
    'input.place_pollution_date_interval': function (val) {
      // console.log(val)
      this.place_pollution_date_interval = val
      this.read_place_pollution_data_with_date_interval(val, this.place_long, this.place_lat)
    },
    'input.place_pollution_variant': function (val) {
      // console.log(val)
      this.place_pollution_variant = val
      this.place_pollution_display_key = this.variant2key[this.place_pollution_variant]
      this.place_pollution_variant_title = this.variant2title[this.place_pollution_variant]
    },
  },
  mounted() {
    window.addEventListener('resize', this.onResize)
    this.initContainerSize()
    this.read_all_pollution_data_daily(this.all_pollution_date)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize)
  },
  methods: {
    onResize(e) {
      clearTimeout(this.resizeID);
      this.resizeID = setTimeout(this.initContainerSize, 500)
    },
    initContainerSize() {
      this.container.width = this.$refs.chinaMapContainer.clientWidth
      this.container.height = parseInt(this.container.width * 0.8)
    },
    read_all_pollution_data_daily(date) {
      this.loading_all_pollution = true;
      this.errored_all_pollution = false;
      axios
          .get('http://127.0.0.1:8000/api/pollution_data/daily', {
            params: {
              date: date
            }
          })
          .then(response => {
            this.all_pollution_data = response.data.result
            // console.log(this.all_pollution_data)
          })
          .catch(error => {
            console.log(error)
            this.errored_all_pollution = true
          })
          .finally(() => this.loading_all_pollution = false)
    },
    read_place_pollution_data_with_date_interval(dateInterval, long, lat) {
      this.loading_place_pollution = true;
      this.errored_place_pollution = false;
      axios
          .get('http://127.0.0.1:8000/api/pollution_data/place', {
            params: {
              startdate: dateInterval[0],
              enddate: dateInterval[1],
              long: long,
              lat: lat
            }
          })
          .then(response => {
            this.place_pollution_data = response.data.result
            this.place_pollution_data_empty = this.place_pollution_data.length === 0
            // console.log(this.place_pollution_data)
          })
          .catch(error => {
            console.log(error)
            this.errored_place_pollution = true
          })
          .finally(() => this.loading_place_pollution = false)
    },
    changePlace() {
      this.place_long = this.input.place_long
      this.place_lat = this.input.place_lat
      this.read_place_pollution_data_with_date_interval(this.place_pollution_date_interval, this.place_long, this.place_lat)
    }
  }
}
</script>

<style scoped>

</style>