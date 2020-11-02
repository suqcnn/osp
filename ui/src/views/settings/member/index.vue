<template>
    <div>
        <div class="member-bar">
            <el-breadcrumb class="app-breadcrumb" separator="/">
                <transition-group name="breadcrumb">
                    <el-breadcrumb-item key="pods">
                        <span class="no-redirect">用户管理</span>
                    </el-breadcrumb-item>
                </transition-group>
            </el-breadcrumb>
            <div class="right">
                <el-button size="mini" @click="createUserFormVisible = true">创建用户</el-button>
                <el-button size="mini">禁用</el-button>
                <el-button size="mini" type="danger">删除</el-button>
                <el-input size="small" placeholder="搜索" suffix-icon="el-icon-search">
                </el-input>
            </div>
        </div>
        <div>
            <el-table ref="multipleTable" :data="userData" class="table-fix" tooltip-effect="dark" style="width: 100%">
                <el-table-column type="selection" width="45">
                </el-table-column>
                <el-table-column prop="name" label="用户名" show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="email" label="邮箱" show-overflow-tooltip>
                    <template slot-scope="scope">{{ scope.row.email ? scope.row.email : "—" }}</template>
                </el-table-column>
                <el-table-column prop="status" label="状态" show-overflow-tooltip>
                    <template slot-scope="scope">
                        {{ scope.row.status | filterStatus }}
                    </template>
                </el-table-column>

                <el-table-column prop="last_login" label="上次登录时间" show-overflow-tooltip>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">权限管理</el-button>
                        <el-button size="mini" @click="handleEnableUser(scope.row.name, scope.row.status)">
                                {{ scope.row.status | filterEnable }}
                        </el-button>
                        <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div>
            <el-dialog title="创建用户" :visible.sync="createUserFormVisible">
                <el-form :model="form">
                    <el-form-item label="用户名">
                        <el-input v-model="form.name" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input v-model="form.password" autocomplete="off" placeholder="请输入密码" show-password>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="邮箱">
                        <el-input v-model="form.email" autocomplete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="handleCreateUser()">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
    import { createUser, getUser, updateUser } from '@/api/user'
    import { Message } from 'element-ui'

    export default {
        name: 'member',
        mounted: function () {
            this.handleGetUser()
        },
        data() {
            return {
                createUserFormVisible: false,
                form: {
                    name: '',
                    email: '',
                    password: ''
                },
                formLabelWidth: '120px',
                userData: []
            }
        },
        filters: {
            filterStatus(val) {
                switch (val) {
                    case "normal":
                        val = "正常"
                        break
                    case "disable":
                        val = "禁用"
                        break
                }
                return val
            },
            filterEnable(val) {
                switch (val) {
                    case "normal":
                        val = "禁用"
                        break
                    case "disable":
                        val = "启用"
                        break
                }
                return val
            }
        },
        methods: {
            handleEdit(index, row) {
                console.log(index, row);
            },
            handleDelete(index, row) {
                console.log(index, row);
            },
            handleCreateUser() {
                console.log(this.form.name, this.form.email, this.form.password)
                if (!this.form.name) {
                    Message.error("用户名称不能为空！")
                }
                if (!this.form.password) {
                    Message.error("密码不能为空！")
                }
                if (!this.form.email) {
                    Message.error("邮箱不能为空！")
                }
                createUser(this.form).then(() => {
                    this.loading = false
                }).catch(() => {
                    this.loading = false
                })
                this.createUserFormVisible = false
            },
            handleGetUser(name) {
                getUser(name).then(response => {
                    this.userData = response.data
                    console.log(this.userData)
                })
            },
            handleEnableUser(name, currentStatus) {
                console.log(name, status)
                
                this.$confirm('此操作将禁用该用户, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    updateUser(name, {status: currentStatus == "normal" ?"disable":"normal"}).then(response => {
                        console.log(response)
                        this.$message({
                            type: 'success',
                            message: '修改成功!'
                        });
                        this.handleGetUser()
                    })

                });
                // updateUser(name, status).then(response => {
                //     this.loading = true
                // })
            },
            open() {

            }
        }
    }
</script>


<style lang="scss" scoped>
    @import "~@/styles/variables.scss";

    .table-fix {
        height: calc(100% - 100px);
    }

    .member-bar {
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