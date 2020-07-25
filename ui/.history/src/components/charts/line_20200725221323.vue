<template>
    <div>
        <div :id=id style="width: 100%; height: 300px;"></div>
    </div>
</template>

<script>
    import Highcharts from 'highcharts';
    export default {
        mounted() {
            this.init();
        },
        data() {
            return {}
        },
        props: {
            id: {
                type: String,
                default: "charts"
            }
        },
        methods: {
            init() {
                this.draw();
            },
            draw() {
                new Highcharts.chart(this.id, {
                    title: {
                        text: ''
                    },
                    yAxis: {
                        title: {
                            text: '单位:Gi/核'
                        }
                    },
                    xAxis: {
                        type: 'string',
                        title: {
                            text: null
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'bottom'
                    },
                    credits: { enabled: false },
                    plotOptions: {
                        series: {
                            label: {
                                connectorAllowed: false
                            },
                            pointStart: 0
                        }
                    },
                    series: [{
                        name: 'Memory',
                        data: [
                            ["2020,07,24,12,01,01", 2.2], 
                            ["2020-07-24 12:02:01", 2.5],
                            ["2020-07-24 12:03:01", 2.1], 
                            ["2020-07-24 12:06:01", 2.9], 
                            ["2020-07-24 12:09:01", 2.6]
                        ]
                    }, {
                        name: 'CPU',
                        data: [
                            ["2020-07-24 12:01:01", 2],
                            ["2020-07-24 12:02:01", 5],
                            ["2020-07-24 12:05:01", 4],
                            ["2020-07-24 12:07:01", 2],
                            ["2020-07-24 12:09:01", 3]
                        ]
                    }],
                    responsive: {
                        rules: [{
                            condition: {
                                maxWidth: 500
                            },
                            chartOptions: {
                                legend: {
                                    layout: 'horizontal',
                                    align: 'right',
                                    verticalAlign: 'bottom'
                                }
                            }
                        }]
                    }
                });
            }
        }
    }
</script>