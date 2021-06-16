<template>
  <div style="overflow: auto;"></div>
</template>

<script>
export default {
  name: "ChinaMap",
  props: {
    pollution_data: {
      type: Array,
      required: true
    },
    display_key: {
      type: String,
      default: () =>{
        return "pm25"
      }
    },
    width: {
      type: Number,
      default: () => {
        return 500
      }
    },
    height: {
      type: Number,
      default: () => {
        return 500
      }
    }
  },
  watch: {
    width() {
      this.draw()
    },
    height() {
      this.draw()
    },
    display_key() {
      this.draw()
    },
    pollution_data() {
      this.draw()
    }
  },
  mounted() {
    this.draw()
  },
  methods: {
    draw() {
      const d3 = this.d3
      const lodash = this.lodash
      const width = this.width
      const height = this.height
      const container = this.$el
      const display_key = this.display_key
      const pollution_data = this.pollution_data

      /// remove previous dom objects in container
      while (container.firstChild) {
        container.removeChild(container.firstChild)
      }

      // const zoom = d3.zoom()
      //     .scaleExtent([1, 8])
      //     .on("zoom", zoomed);

      let svg = d3.select(container)
          .append("svg")
          // .attr("width", width)
          // .attr("height", height)
          .attr("viewBox", [0, 0, width, height])
          // .attr("transform", d3.zoomIdentity);

      // let color = d3.scaleOrdinal(d3.schemeCategory10);

      // D3 - 绘制中国地图 (D3.v5)
      // https://blog.csdn.net/moon_sky1999/article/details/106495778
      let projection = d3.geoMercator()
          .center([107, 31])
          .scale(height * 0.9)
          .translate([width / 2, height / 2]);

      let path = d3.geoPath()
          .projection(projection);

      d3.json("data/ChinaMap.json").then(function (geo) {
        // console.log(geo);
        let Province = svg.append("g")
            .attr("cursor", "pointer")
            .attr("stroke", "#AAA")//设置边线颜色
            .attr("stroke-width", 0.0005*width)//设置边线宽度
            .attr("stroke-linejoin", "round")
            .selectAll("path")
            .data(geo.features)
            .enter()
            .append("path")
            .attr("class", "province")
            .attr("fill", "#FFF")
            .attr("class", "province")
            // .style("fill", function (d, i) {
            //   return 'rgba(0,' + parseFloat(255 - Math.random() * 50) + ',' + parseFloat(255 - Math.random() * 100) + ')';
            // })
            .attr("d", path);

        // tooltip
        // remove previous tips
        d3.select(".d3-tip").remove();
        let tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
          return "long: " + d.long + " lat: " + d.lat + " value: " + d[display_key]
        });
        svg.call(tip)

        // color
        let color = d3.scaleSequential(d3.extent(pollution_data, d => d[display_key]), d3.interpolateYlOrRd)

        svg.selectAll("circle")
            .data(pollution_data)
            .enter().append("g")
            .attr("transform", function (d) {
              //计算标注点的位置
              var coor = projection([d.long, d.lat]); //经纬度的投影
              return "translate(" + coor[0] + "," + coor[1] + ")";
            })
            .append("circle")
            .attr("r", 0.00125*width)
            .attr("fill", d => color(d[display_key]))
            .attr("opacity", 0.8)
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

      });

      // test pollution data
      // let pollution_file = "data/pollution_20130101.json"
      // d3.json(pollution_file).then(function (data) {
      //   // console.log(data);
      //   let color = d3.scaleSequential(d3.extent(data, d => d[display_key]), d3.interpolateYlOrRd)
      //   svg.selectAll("circle")
      //       .data(data)
      //       .enter().append("g")
      //       .attr("transform", function (d) {
      //         //计算标注点的位置
      //         var coor = projection([d.long, d.lat]); //经纬度的投影
      //         return "translate(" + coor[0] + "," + coor[1] + ")";
      //       })
      //       .append("circle")
      //       .attr("r", 0.0012*width)
      //       .attr("fill", d => color(d[display_key]))
      //       .attr("opacity", 0.8);
      // });

      // svg.call(zoom);
      //
      // function zoomed() {
      //   svg.attr("transform", d3.event.transform);
      // }

    }
  }
}
</script>


<style scoped>

</style>