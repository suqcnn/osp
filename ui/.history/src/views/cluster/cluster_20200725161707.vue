<template>
    <div>
        <div class="cluster-bar">
            <el-breadcrumb class="app-breadcrumb" separator="/">
                <transition-group name="breadcrumb">
                    <el-breadcrumb-item key="pods">
                        <span class="no-redirect">Cluster</span>
                    </el-breadcrumb-item>
                </transition-group>
            </el-breadcrumb>
        </div>

        <div style="margin: 20px;">
            <el-card class="box-card">
                <div slot="header" class="clearfix">
                    <span>Master</span>
                </div>
                <div class="charts">
                    <CPU></CPU>
                    <!-- <MEM id="masterMem"></MEM> -->
                    <POD></POD>
                </div>

            </el-card>
            <el-card class="box-card">
                <div slot="header" class="clearfix">
                    <span>Worker</span>
                </div>
                <div class="charts">
                    <MEM v-for="(item,index) in options" :key="index" 
                    :id="item.id" :data="item"></MEM>
                    <MEM v-for="(item,index) in options" :key="index" 
                    :id="item.id" :data="item"></MEM>
                </div>
            </el-card>
        </div>
    </div>

</template>

<script>
    import { CPU, MEM, POD } from '@/components/charts'

    export default {
        name: 'aaa',
        components: {
            CPU, MEM, POD
        },
        data() {
            return {
                options: [
                    {
                        id:'mem',
                        title: "Memory",
                        backgroundNum: 3,
                        series: [{
                            name: 'Move',
                            value: 80
                        }, {
                            name: 'Exercise',
                            value: 65
                        }, {
                            name: 'Stand',
                            value: 50
                        }]
                    },
                    {
                        id:'pod',
                        title: "Pod",
                        backgroundNum: 3,
                        series: [{
                            name: '1',
                            value: 11
                        }, {
                            name: '2',
                            value: 65
                        }, {
                            name: '3',
                            value: 50
                        }]
                    },
                    {
                        id:'pod12312',
                        title: "Pod",
                        backgroundNum: 3,
                        series: [{
                            name: '1',
                            value: 11
                        }, {
                            name: '2',
                            value: 65
                        }, {
                            name: '3',
                            value: 50
                        }]
                    }
                ],

            }
        }
    }
</script>


<style lang="scss" scoped>
    @import "~@/styles/variables.scss";

    .cluster-bar {
        transition: width 0.28s;
        height: 55px;
        overflow: hidden;
        box-shadow: inset 0 0 4px rgba(0, 21, 41, 0.1);
        margin: 20px 20px 0px;

        .app-breadcrumb.el-breadcrumb {
            display: inline-block;
            font-size: 20px;
            line-height: 55px;
            margin-left: 8px;

            .no-redirect {
                // color: #97a8be;
                cursor: text;
                margin-left: 15px;
                font-size: 23px;
                font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
            }
        }

        .icon-create {
            display: inline-block;
            line-height: 55px;
            margin-left: 20px;
            width: 1.8em;
            height: 1.8em;
            vertical-align: 0.8em;
            color: #bfbfbf;
        }

        .right {
            float: right;
            height: 100%;
            line-height: 55px;
            margin-right: 25px;

            .el-input {
                width: 195px;
                margin-left: 15px;
            }

            .el-select {
                .el-select__tags {
                    white-space: nowrap;
                    overflow: hidden;
                }
            }

        }
    }

    .text {
        font-size: 14px;
    }

    .item {
        margin-bottom: 18px;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }

    .clearfix:after {
        clear: both
    }

    .box-card {
        width: 100%;
        /* bottom: 0; */
    }

    .charts {
        display: flex;
        flex-direction: row;
    }
</style>