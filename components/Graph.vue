<script setup>

const props = defineProps({
  width: {
    type: Number,
    default: 500
  },
  height: {
    type: Number,
    default: 450
  },
  marginLeft: {
    type: Number,
    default: 50
  },
  marginTop: {
    type: Number,
    default: 10
  },
  marginRight: {
    type: Number,
    default: 20
  },
  marginBottom: {
    type: Number,
    default: 50
  },
  data: {
    type: Array,
    default: () => []
  }
});

useHead({
  script: [
    {
      src: 'https://cdn.jsdelivr.net/npm/d3@7/+esm',
      defer: true,
      async: true
    }
  ]
});

onMounted(async () => {
  const d3 = await import('https://cdn.jsdelivr.net/npm/d3@7/+esm');

  // Create simple d3 graph
  console.log("Creating graph");
  // Random data; array of objects with date and value properties
  const unparsedData = [
    {
      date: "01-01-2021",
      value: 100
    },
    {
      date: "01-02-2021",
      value: 200
    },
    {
      date: "01-03-2021",
      value: 300
    },
    {
      date: "01-04-2021",
      value: 400
    },
    {
      date: "01-05-2021",
      value: 500
    },
    {
      date: "01-06-2021",
      value: 600
    },
    {
      date: "01-07-2021",
      value: 700
    },
    {
      date: "01-08-2021",
      value: 800
    },
    {
      date: "01-09-2021",
      value: 900
    },
    {
      date: "01-10-2021",
      value: 1000
    },
    {
      date: "01-11-2021",
      value: 1100
    },
    {
      date: "01-12-2021",
      value: 1200
    },
    {
      date: "01-13-2021",
      value: 1300
    },
    {
      date: "01-14-2021",
      value: 1400
    },
    {
      date: "01-15-2021",
      value: 1500
    }
  ]
  const data = unparsedData.map((d) => {
    return {
      date: d3.timeParse("%m-%d-%Y")(d.date),
      value: d.value
    }
  })
  const chart = d3.select(".graph")
    .append("svg")
      .attr("width", props.width + props.marginLeft + props.marginRight)
      .attr("height", props.height + props.marginTop + props.marginBottom)
      .style("background", "#C9CFE5FF")
      .style("padding", 10)
    .append("g")
      .attr("transform", `translate(${props.marginLeft}, ${props.marginTop})`);
  const x = d3.scaleTime()
    .domain(d3.extent(data, (d) => d.date))
    .range([0, props.width]);
  chart.append("g")
    .attr("transform", `translate(0, ${props.height})`)
    .call(d3.axisBottom(x));
  const y = d3.scaleLinear()
    .domain([0, d3.max(data, (d) => d.value)])
    .range([props.height, 0]);
  chart.append("g")
    .call(d3.axisLeft(y));
  // Add lines
  chart.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(function(d) { return x(new Date(d.date)) })
      .y(function(d) { return y(d.value) })
    )
  // Add dots
  chart.append("g")
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function(d) { return x(new Date(d.date)) } )
      .attr("cy", function(d) { return y(d.value) } )
      .attr("r", 5)
      .attr("fill", "#69b3a2")
});
</script>

<template>
  <div class="graph"></div>
</template>

<style scoped>

</style>