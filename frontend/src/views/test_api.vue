<template>
  <div id="test-api">
<!--    <h1>Bitcoin Price Index</h1>-->

<!--    <section v-if="errored">-->
<!--      <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>-->
<!--    </section>-->

<!--    <section v-else>-->
<!--      <div v-if="loading">Loading...</div>-->

<!--      <div-->
<!--          v-else-->
<!--          v-for="currency in info"-->
<!--          class="currency"-->
<!--      >-->
<!--        {{ currency.description }}:-->
<!--        <span class="lighten">-->
<!--        <span v-html="currency.symbol"></span>{{ currency.rate_float | currencydecimal }}-->
<!--      </span>-->
<!--      </div>-->

<!--    </section>-->

    <h2>===== Test pollution =====</h2>
    <section v-if="errored_pollution">
      <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
    </section>

    <section v-else>
      <div v-if="loading_pollution">Loading...</div>
      <div v-else>
<!--        (lat, long): SO2-->
<!--        <div-->
<!--            v-for="record in pollution_records"-->
<!--            class="record"-->
<!--        >-->
<!--          ({{ record.lat }}, {{ record.long }}):-->
<!--          {{ record.so2 }}-->
<!--        </div>-->
        <v-data-table
            :headers="headers"
            :items="pollution_records"
            :search="search"
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
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "test_api",
  data() {
    return {
      info: null,
      loading: true,
      errored: false,
      pollution_records: null,
      loading_pollution: true,
      errored_pollution: false,
      search: "",
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
      ]
    }
  },
  filters: {
    currencydecimal(value) {
      return value.toFixed(2)
    }
  },
  mounted() {
    axios
        .get('http://127.0.0.1:8000/test_api')
        .then(response => {
          this.info = response.data.bpi
        })
        .catch(error => {
          console.log(error)
          this.errored = true
        })
        .finally(() => this.loading = false)

    axios
        .get('http://127.0.0.1:8000/api/pollution_data/daily', {
          params: {
            date: "2013-01-02",
            // lat: 18.34,
            // long: 109.38
          }
        })
        .then(response => {
          this.pollution_records = response.data.result
          console.log(this.pollution_records)
        })
        .catch(error => {
          console.log(error)
          this.errored_pollution = true
        })
        .finally(() => this.loading_pollution = false)
  }
}

</script>

<style scoped>

</style>