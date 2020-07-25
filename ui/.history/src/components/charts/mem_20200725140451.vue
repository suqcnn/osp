<template>
    <div>
        <div id="mem" style="width: 400px; height: 300px;"></div>
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
        methods: {
            init() {
                this.draw();
            },
            draw() {
                new Highcharts.chart('mem', {
                    chart: {
                        type: 'solidgauge',
                        marginTop: 50
                    },
                    credits: { enabled: false },
                    title: {
                        text: 'MEM',
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
                        background: [{ // Track for Move
                            outerRadius: '112%',
                            innerRadius: '88%',
                            backgroundColor: 'red',
                            //Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0.3).get(),
                            borderWidth: 0
                        }, { // Track for Exercise
                            outerRadius: '87%',
                            innerRadius: '63%',
                            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0.3).get(),
                            borderWidth: 0
                        }, { // Track for Stand
                            outerRadius: '62%',
                            innerRadius: '38%',
                            backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[2]).setOpacity(0.3).get(),
                            borderWidth: 0
                        }]
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
                    series: [{
                        name: 'Move',
                        // borderColor: Highcharts.getOptions().colors[1],
                        borderColor: 'yellow',
                        data: [{
                            color: Highcharts.getOptions().colors[0],
                            // color:'yellow',
                            radius: '100%',
                            innerRadius: '100%',
                            y: 80
                        }]
                    }, {
                        name: 'Exercise',
                        borderColor: Highcharts.getOptions().colors[1],
                        data: [{
                            color: Highcharts.getOptions().colors[1],
                            radius: '75%',
                            innerRadius: '75%',
                            y: 65
                        }]
                    }, {
                        name: 'Stand',
                        borderColor: Highcharts.getOptions().colors[2],
                        data: [{
                            color: Highcharts.getOptions().colors[2],
                            radius: '50%',
                            innerRadius: '50%',
                            y: 50
                        }]
                    }]
                });
            }
        }
    }
</script>

<style lang="stylus">

</style>