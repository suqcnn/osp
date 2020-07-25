<template>
    <div>
        <div :id=id style="width: 400px; height: 300px;"></div>
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
                            // text: '就业人数'
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle'
                    },
                    plotOptions: {
                        series: {
                            label: {
                                connectorAllowed: false
                            },
                            pointStart: 2010
                        }
                    },
                    series: [{
                        name: '安装，实施人员',
                        data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175,154175,154175,154175,154175,154175]
                    }],
                    responsive: {
                        rules: [{
                            condition: {
                                // maxWidth: 100%
                            },
                            chartOptions: {
                                legend: {
                                    layout: 'horizontal',
                                    align: 'center',
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