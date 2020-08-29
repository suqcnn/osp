<template>
    <div>
        <clusterbar :titleName="titleName" :nameFunc="nameSearch" />


        <div>
            <el-table ref="multipleTable" :data="nodes" class="table-fix" tooltip-effect="dark" style="width: 100%">
                <el-table-column type="selection" width="45">
                </el-table-column>
                <el-table-column prop="name" label="名称" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="taints" label="Taints" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="os" label="OS" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="os_image" label="OS Image" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="kernel_version" label="Kernel Version" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="version" label="Version" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="age" label="Age" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="status" label="状态" show-overflow-tooltip>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
    import { Clusterbar } from '@/views/components'
    import { listNodes } from '@/api/nodes'
    import { Message } from 'element-ui'

    export default {
        name: 'Pod',
        components: {
            Clusterbar
        },
        data() {
            return {
                titleName: ["Nodes"],
                search_name: "",
                nodeData: []
            }
        },
        methods: {
            handleListNodes() {
                const cluster = this.$store.state.cluster
                listNodes(cluster).then(response => {
                    this.nodeData = response.data
                    console.log(this.nodeData)
                })
            },
            nameSearch: function (val) {
                console.log(val)
                this.search_name = val
            },
        },
        computed: {
            nodes: function () {
                let nodeList = []
                for (let n of this.nodeData) {
                    if (this.search_name && !n.name.includes(this.search_name)) continue
                    nodeList.push(n)
                }
                return nodeList
            },
        },
        mounted() {
            this.handleListNodes()
        }
    }
</script>

<style lang="scss" scoped>
    .node-bar {
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
</style>