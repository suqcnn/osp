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
            <el-card class="box-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>Master</span>
                </div>
                <el-row :gutter=10>
                    <el-col :span=4 v-for="(item,index) in masterOptions" :key="index">
                        <SolidGauge :id="item.id" :data="item">
                        </SolidGauge>
                    </el-col>
                    <el-col :span=12>
                        <Ployline id="masterLine"></Ployline>
                    </el-col>
                </el-row>
                <!-- <div class="charts">
                    <SolidGauge v-for="(item,index) in masterOptions" :key="index" :id="item.id" :data="item">
                    </SolidGauge>
                </div> -->

            </el-card>
            <el-card class="box-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>Worker</span>
                </div>
                <el-row :gutter=10>
                    <el-col :span=4 v-for="(item,index) in workerOptions" :key="index">
                        <SolidGauge :id="item.id" :data="item">
                        </SolidGauge>
                    </el-col>
                    <el-col :span=12>
                        <Ployline id="workerLine"></Ployline>
                    </el-col>
                </el-row>
                <!-- <div class="charts">
                    <SolidGauge v-for="(item,index) in workerOptions" :key="index" :id="item.id" :data="item">
                    </SolidGauge>
                </div> -->
            </el-card>
        </div>
    </div>
</template>

<script>
    import { SolidGauge, Ployline } from '@/components/charts'

    export default {
        name: 'aaa',
        components: {
            SolidGauge,
            Ployline
        },
        data() {
            return {
                workerOptions: [
                    {
                        id: 'wokerCpu',
                        title: "CPU",
                        backgroundNum: 3,
                        series: [{
                            name: 'Usage',
                            value: 80
                        }, {
                            name: 'Limits',
                            value: 65
                        }, {
                            name: 'Capacity',
                            value: 50
                        }]
                    },
                    {
                        id: 'wokerMem',
                        title: "Memory",
                        backgroundNum: 3,
                        series: [{
                            name: 'Usage',
                            value: 80
                        }, {
                            name: 'Limits',
                            value: 65
                        }, {
                            name: 'Capacity',
                            value: 50
                        }]
                    },
                    {
                        id: 'workerPod',
                        title: "Pod",
                        backgroundNum: 1,
                        series: [{
                            name: 'Usage',
                            value: 11
                        }]
                    }
                ],
                masterOptions: [
                    {
                        id: 'masterCpu',
                        title: "CPU",
                        backgroundNum: 3,
                        series: [{
                            name: 'Usage',
                            value: 80
                        }, {
                            name: 'Limits',
                            value: 65
                        }, {
                            name: 'Capacity',
                            value: 50
                        }]
                    },
                    {
                        id: 'masterMem',
                        title: "Memory",
                        backgroundNum: 3,
                        series: [{
                            name: 'Usage',
                            value: 80
                        }, {
                            name: 'Limits',
                            value: 65
                        }, {
                            name: 'Capacity',
                            value: 50
                        }]
                    },
                    {
                        id: 'masterPod',
                        title: "Pod",
                        backgroundNum: 1,
                        series: [{
                            name: 'Usage',
                            value: 11
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
        margin-top: 5px;
        /* bottom: 0; */
    }

    .charts {
        display: flex;
        flex-direction: row;
    }
</style>