<template>
  <v-layout row wrap>
    <v-flex xs12 pa-1>
      <v-card>
        <v-card-title>
          <span class="display-1">Introduction</span>
        </v-card-title>

        <v-card-text>
          <span class="title">Name: Jialun Shen</span>
          <br/>
          <span class="title">Stu id: 16307110030</span>
        </v-card-text>

        <v-card-text>
          <span class="title">Readme for Final</span>
          <span>
            <ol style="font-size: 16px">
              <li>This is the final project of <i>FDU: DATA130012 Data Visualization (数据可视化)</i>.</li>
              <li>The data I use is
                <a href="http://naq.cicidata.top:10443/chinavis/opendata">
                2013–2018年中国高分辨率大气污染再分析开放数据集</a>
                from <a href="http://chinavis.org/2021/challenge.html">ChinaVis 2021数据可视化竞赛</a>.
              </li>
<!--              <li>-->
<!--                I use the geography data from-->
<!--                <a href="https://blog.csdn.net/niu_dige/article/details/104856967">中国行政区边界shp下载（省，市，县）</a>-->
<!--                to draw a map of China.-->
<!--                I used <a href="https://mapshaper.org">this website</a> to transform map data format, which is helpful.-->
<!--              </li>-->
            </ol>
          </span>
        </v-card-text>

        <v-card-text>
          <span class="title">Used Libraries</span>
          <span>
            <ol style="font-size: 16px">
              <li>Vue.js (with CLI)</li>
              <li>Vuetify.js (for GUI)</li>
              <li>d3.js</li>
              <li>lodash.js</li>
            </ol>
          </span>
        </v-card-text>

        <!--        <v-card-text>-->
        <!--          <span class="title">Remarks</span>-->
        <!--          <span>-->
        <!--            <ol style="font-size: 16px">-->
        <!--              <span class="font-weight-bold"></span>-->
        <!--              <li>You can direct to this page if you click the icon on the toolbar</li>-->
        <!--              <li>Every page is fully  <span class="font-weight-bold">responsive</span> and-->
        <!--                <span class="font-weight-bold">dynamic</span>-->
        <!--              </li>-->
        <!--              <li>Each time a page is resized, diagrams in the page are resized as well</li>-->
        <!--              <li>There are data tables for the input data. You can search any element for the reference</li>-->
        <!--              <li><span class="font-weight-bold">For Level 2, </span> you can change the year range as you want</li>-->
        <!--              <li><span class="font-weight-bold">For Level 3, </span> you can change the department as you want</li>-->
        <!--              <li><span class="font-weight-bold">For Level 3, </span> I was not sure if the collaboration between professors from different departments should be excluded so the current version includes it</li>-->
        <!--              <li><span class="font-weight-bold">For Level 3, </span> you can zoom in/out in the node links diagram</li>-->
        <!--            </ol>-->
        <!--          </span>-->
        <!--        </v-card-text>-->

        <v-card-actions>
<!--          <v-btn color="red" dark @click="$router.push('/homework1')">GOTO Homework 1</v-btn>-->
<!--          <v-btn color="orange" dark @click="$router.push('/homework2')">GOTO Homework 2</v-btn>-->
          <v-btn color="green" dark @click="$router.push('/final')">GOTO Final</v-btn>
        </v-card-actions>


      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: "home"
}
</script>

<style scoped>

</style>