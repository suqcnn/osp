<template>
    <div>
        <div :id=id style="width: 400px; height: 300px;"></div>
    </div>
</template>

<script>
    import Highcharts from 'highcharts';
    import HighchartsMore from 'highcharts/highcharts-more';
    import SolidGauge from 'highcharts/modules/solid-gauge.js'
    HighchartsMore(Highcharts)
    SolidGauge(Highcharts);

    if (!Highcharts.theme) {
        Highcharts.setOptions({
            chart: {
                backgroundColor: 'white'
            },
            colors: ['#F62366', '#9DFF02', '#0CCDD6'],
            title: {
                style: {
                    color: 'silver'
                }
            },
            tooltip: {
                style: {
                    color: 'silver'
                }
            }
        });
    }

    export default {
        mounted() {
            this.init();
        },
        data() {
            return {

            }
        },
        props: {
            id: {
                type: String,
                default: "c"
            },
            data: {
                type: Object,
                default: function () {
                    return {
                        backgroundNum:0
                    }
                }
            }
        },
        methods: {
            setBackground() {
                let arr = []
                let obj = { // Track for Move
                    outerRadius: '',
                    innerRadius: '',
                    backgroundColor: '',
                    borderWidth: 0
                }
                let [outerRadius, outerRadius] = [112, 88]
                for (let i = 0; i++; i < this.data.backgroundNum) {
                    obj.outerRadius = outerRadius - 25 * i
                    obj.innerRadius = innerRadius - 25 * i
                    obj.backgroundColor = Highcharts.Color(Highcharts.getOptions().colors[i]).setOpacity(0.3).get()
                    arr.push(obj)
                }

                return arr
            },
            init() {
                this.draw();
            },
            draw() {
                new Highcharts.chart(this.id, {
                    chart: {
                        type: 'solidgauge',
                        marginTop: 50
                    },
                    credits: { enabled: false },
                    title: {
                        text: this.data.title,
                        style: {
                            fontSize: '24px'
                        }
                    },
                    tooltip: {
                        borderWidth: 0,
                        backgroundColor: 'none',
                        shadow: false,
                        style: {
                            fontSize: '15px'
                        },
                        pointFormat: '{series.name}<br><span style="font-size:1em; color: {point.color}; font-weight: bold">{point.y}%</span>',
                        positioner: function (labelWidth) {
                            return {
                                x: 200 - labelWidth / 2,
                                y: 140
                            };
                        }
                    },
                    pane: {
                        startAngle: 0,
                        endAngle: 360,
                        background: this.setBackground(),
                        // background: 
                    },
                    yAxis: {
                        min: 0,
                        max: 100,
                        lineWidth: 0,
                        tickPositions: []
                    },
                    plotOptions: {
                        solidgauge: {
                            borderWidth: '28px',   //覆盖层 宽度
                            dataLabels: {
                                enabled: false
                            },
                            linecap: 'round',
                            stickyTracking: false
                        }
                    },
                    series: this.data.series,
                    // series: 
                });
            }
        }
    }
</script>

<style lang="stylus">

</style>