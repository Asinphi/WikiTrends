<template>
  <div class="graph-container">
    <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`" @click="$emit('graphClicked')">
      <g :transform="`translate(${marginLeft},${marginTop})`">
        <path :d="linePath" fill="none" stroke="steelblue" stroke-width="1.5" />
        <g :transform="`translate(0,${innerHeight})`">
          <line :x2="innerWidth" stroke="black" stroke-width="0.5" />
          <text :x="innerWidth / 2" :y="15" text-anchor="middle" font-size="10">Date</text>
          <text :x="innerWidth / 2" :y="15" text-anchor="middle" font-size="10">Date (Months)</text>
        </g>
        <g v-for="(tickValue, index) in xAxisTickFormat" :key="index"
        :transform="`translate(0,${innerHeight - xScale(tickValue)})`">
        <line :x2="innerWidth" stroke="black" stroke-width="0.5" />
        <text :x="innerWidth / 2" :y="15" text-anchor="end" dominant-baseline="middle" font-size="10">{{ tickValue }}</text>
        </g>
        <g v-for="(tickValue, index) in yTicks" :key="index"
          :transform="`translate(0,${innerHeight - yScale(tickValue)})`">
          <line :x2="innerWidth" stroke="black" stroke-width="0.5" />
          <text :x="-15" :y="3" text-anchor="end" dominant-baseline="middle" font-size="10">{{ tickValue }}</text>
          <text :x="-20" :y="3" text-anchor="end" dominant-baseline="middle" font-size="10">{{ tickValue }}</text>
        </g>
        <text :transform="`translate(-10,${innerHeight / 2})rotate(-90)`" text-anchor="middle" font-size="10">View
          Count</text>
        <text :transform="`translate(-10,${innerHeight / 2})rotate(-90)`" text-anchor="middle" font-size="10">
          View Count (Views)</text>
      </g>
    </svg>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as d3 from 'd3';

export default {
  props: {
    width: {
      type: Number,
      required: true,
    },
    marginLeft: {
      type: Number,
      default: 20,
    },
    article: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const height = 150;
    const marginTop = 10;
    const marginRight = 10;
    const marginBottom = 20;
    const innerWidth = props.width - props.marginLeft - marginRight;
    const innerHeight = height - marginTop - marginBottom;

    const pageViews = ref([]);
    const linePath = ref('');
    const xScale = d3.scaleTime().range([0, innerWidth]);
    const yScale = d3.scaleLinear().range([innerHeight, 0]);
    const yTicks = ref([]);
    const xAxisTickFormat = d3.timeFormat('%b %d'); // Custom tick format for x-axis

    const updateGraph = () => {
      pageViews.value = props.article.page_views.map(pageView => ({
        date: new Date(pageView.view_date),
        viewCount: pageView.view_count,
      }));

      xScale.domain(d3.extent(pageViews.value, d => d.date));
      yScale.domain([0, d3.max(pageViews.value, d => d.viewCount)]);

      const line = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.viewCount));

      linePath.value = line(pageViews.value);

      yTicks.value = yScale.ticks(4);
    };
    
    onMounted(updateGraph);

    watch(() => props.article, updateGraph);

    return {
      height,
      marginTop,
      marginRight,
      marginBottom,
      innerWidth,
      innerHeight,
      linePath,
      yScale,
      yTicks,
      xAxisTickFormat,
    };
  },
};
</script>

<style scoped>
.graph-container {
  margin-top: 10px;
}
</style>