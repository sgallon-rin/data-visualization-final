<template>
  <div style="overflow: auto;"></div>
</template>

<script>
export default {
  name: "PollutionLinePlot",
  props: {
    pollution_data: {
      type: Array,
      required: true
    },
    display_key: {
      type: String,
      default: () => {
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
    },
    margin: {
      type: Object,
      default: () => {
        return {top: 20, right: 30, bottom: 30, left: 40}
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
      const margin = this.margin
      const container = this.$el
      const display_key = this.display_key
      const data = this.pollution_data

      /// remove previous dom objects in container
      while (container.firstChild) {
        container.removeChild(container.firstChild)
      }

      // const zoom = d3.zoom()
      //     .scaleExtent([1, 8])
      //     .on("zoom", zoomed);

      let svg = d3.select(container)
          .append("svg")
          .attr("viewBox", [0, 0, width, height])
      // .attr("transform", d3.zoomIdentity);

      let x = d3.scaleUtc()
          .domain(d3.extent(data, d => new Date(d.date)))
          .range([margin.left, width - margin.right])

      let y = d3.scaleLinear()
          .domain([0, d3.max(data, d => d[display_key])]).nice()
          .range([height - margin.bottom, margin.top])

      let line = d3.line()
          // .defined(d => !isNaN(d.value))
          .x(d => x(new Date(d.date)))
          .y(d => y(d[display_key]))

      let xAxis = g => g
          .attr("transform", `translate(0,${height - margin.bottom})`)
          .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))

      let yAxis = g => g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))
          .call(g => g.select(".domain").remove())
          .call(g => g.select(".tick:last-of-type text").clone()
                  .attr("x", 3)
                  .attr("text-anchor", "start")
                  .attr("font-weight", "bold")
              // .text(data.y)
          )

      svg.append("g")
          .call(xAxis);

      svg.append("g")
          .call(yAxis);

      svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 1.5)
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("d", line);

      // tooltip
      // remove previous tips
      d3.select(".d3-tip").remove();
      let tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
        return "date: " + d.date + " value: " + d[display_key]
      });
      svg.call(tip)

      svg.selectAll("circle")
          .data(data)
          .enter().append("g")
          .append("circle")
          .attr('cx', d => x(new Date(d.date)))
          .attr('cy', d => y(d[display_key]))
          .attr("r", 0.008 * width)
          .attr("fill", "red")
          .attr("opacity", 0.8)
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide);

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