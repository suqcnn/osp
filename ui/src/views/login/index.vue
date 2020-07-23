<template>
    <div class="login">
        <div class="login-box">
            <el-row style="margin-bottom: 25px;">
                <el-col :span="16" :offset="4" align="center">
                    <span class='login-title'>OpenSpace</span>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="16" :offset="4">
                    <el-input 
                        placeholder="请输入用户名" clearable 
                        v-model="login_user" class="login-input">
                        <i slot="prefix" class="el-input__icon el-icon-user"></i>
                    </el-input>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="16" :offset="4">
                    <el-input type="password" autocomplete="new-password"
                        placeholder="请输入密码" clearable
                        v-model="login_password">
                        <i slot="prefix" class="el-input__icon el-icon-lock"></i>
                    </el-input>
                </el-col>
            </el-row>
            <el-row style="margin-top: 30px;">
                <el-col :span="16" :offset="4" align="center">
                    <el-button size="medium" plain style="width: 100%;">
                        <span style="margin-right: 20px;">登</span>
                        <span>录</span>
                    </el-button>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            login_user: '',
            login_password: ''
        }
    }
}
</script>

<style scoped>
.login {
    margin: auto;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    width: 450px;
}
.login-box {
    border-radius: 15px;
    padding: 40px 0px 25px;
    margin: 100px 0px;
    box-shadow: 0 2px 12px 0 rgba(191, 194, 201, 0.733);
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04) */
}
.el-row {
    margin-bottom: 20px;
}
.el-input__icon {
    font-size: 20px;
}
.login-title {
    font-size: 32px;
    font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
}
</style>