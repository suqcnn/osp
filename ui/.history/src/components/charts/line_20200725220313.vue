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
                            text: '单位:Gi/核'
                        }
                    },
                    // legend: {
                    //     layout: 'vertical',
                    //     align: 'right',
                    //     verticalAlign: 'middle'
                    // },
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
                        data: [2.2, 2.23, 2.23, 2.45, 2.67, 2.89]
                    },{
                        name: 'CPU',
                        data: [1, 2, 5, 8, 4, 5]
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