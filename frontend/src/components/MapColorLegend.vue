<template>
  <div style="overflow: auto;"></div>
</template>

<script>
export default {
  name: "MapColorLegend",
  props: {
    width: {
      type: Number,
      default: () => {
        return 300
      }
    },
    height: {
      type: Number,
      default: () => {
        return 50
      }
    },
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
    title: {
      type: String,
      default: () =>{
        return "Value range"
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
    validProps() {
      return true
    },
    draw() {
      if (!this.validProps()) {
        return
      }
      const d3 = this.d3
      const lodash = this.lodash
      const width = this.width
      const height = this.height
      const container = this.$el
      // const domain = 30
      const display_key = this.display_key
      const pollution_data = this.pollution_data
      const tickSize = 6
      const marginTop = 18
      const marginRight = 0
      const marginBottom = 16 + tickSize
      const marginLeft = 0
      const ticks = width / 64
      const title = this.title
      let tickFormat = undefined
      let tickValues = undefined

      // remove previous dom objects in container
      while (container.firstChild) {
        container.removeChild(container.firstChild)
      }

      const svg = d3.select(container)
          .append("svg")
          .attr("width", width)
          .attr("height", height)
          .attr("viewBox", [0, 0, width, height])
          .style("overflow", "visible")
          .style("display", "block");

      let tickAdjust = g => g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);

      let color = d3.scaleSequential(d3.extent(pollution_data, d => d[display_key]), d3.interpolateYlOrRd);

      let x = Object.assign(color.copy()
          .interpolator(d3.interpolateRound(marginLeft, width - marginRight)), {
        range() {
          return [marginLeft, width - marginRight];
        }
      });

      svg.append("image")
          .attr("x", marginLeft)
          .attr("y", marginTop)
          .attr("width", width - marginLeft - marginRight)
          .attr("height", height - marginTop - marginBottom)
          .attr("preserveAspectRatio", "none")
          .attr("xlink:href", ramp(color.interpolator()).toDataURL());

      // scaleSequentialQuantile doesn’t implement ticks or tickFormat.
      if (!x.ticks) {
        if (tickValues === undefined) {
          const n = Math.round(ticks + 1);
          tickValues = d3.range(n).map(i => d3.quantile(color.domain(), i / (n - 1)));
        }
        if (typeof tickFormat !== "function") {
          tickFormat = d3.format(tickFormat === undefined ? ",f" : tickFormat);
        }
      }

      svg.append("g")
          .attr("transform", `translate(0,${height - marginBottom})`)
          .call(d3.axisBottom(x)
              .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
              .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
              .tickSize(tickSize)
              .tickValues(tickValues))
          .call(tickAdjust)
          .call(g => g.select(".domain").remove())
          .call(g => g.append("text")
              .attr("x", marginLeft)
              .attr("y", marginTop + marginBottom - height - 6)
              .attr("fill", "currentColor")
              .attr("text-anchor", "start")
              .attr("font-weight", "bold")
              .text(title));

      function ramp(color, n = 256) {
        var canvas = document.createElement('canvas');
        canvas.width = n;
        canvas.height = 1;
        const context = canvas.getContext("2d");
        for (let i = 0; i < n; ++i) {
          context.fillStyle = color(i / (n - 1));
          context.fillRect(i, 0, 1, 1);
        }
        return canvas;
      }

    }
  }
}
</script>

<style scoped>

</style>