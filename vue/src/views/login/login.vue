<template>
    <div class="content">
        <div id="loginDiv">
            <el-space fill direction="vertical" id="login-space" :size="20">

                <h1 id="login-title">用户登录</h1>

                <el-input v-model="inputUsername" placeholder="请输入账号" :controls="false" :prefix-icon="User" size="large"
                    maxlength="11" />

                <el-input v-model="inputPassword" placeholder="请输入密码" @keyup.enter="clickLogin" type="password"
                    show-password :prefix-icon="Lock" size="large" />

                <el-button type="primary" @click="clickLogin" id="loginButton" size="large" :loading="isLoading">登
                    陆</el-button>


                <div id="login-bottom">
                    <el-link type="primary" @click="clickForget">忘记密码</el-link>
                    <el-link type="primary" @click="router.push('register')">用户注册</el-link>
                </div>
            </el-space>
        </div>
    </div>



</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';

import { login } from '@/request/api'

const router = useRouter()
const inputUsername = ref("")
const inputPassword = ref("")
const isLoading = ref(false)


function clickForget() {
    ElMessage.warning("我也不知道你密码多少，你自己再好好想想吧")
}

async function clickLogin() {

    if (inputUsername.value == "" || inputPassword.value == "") {
        ElMessage.error('账号或密码不能为空！')
    }
    else {
        isLoading.value = true
        await login(inputUsername.value, inputPassword.value)
            .then(res => {
                ElMessage.success("登录成功！")

                sessionStorage.setItem('username', inputUsername.value)
                sessionStorage.setItem('count', res.data.count)
                sessionStorage.setItem('name', res.data.name)
                isLoading.value = false

                router.push('item')
            })
            .catch(err => {
                ElMessage.error("登录失败，" + err)
                isLoading.value = false
            })
    }
}

</script>

<style scoped>
.content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}


#loginDiv {
    border-radius: 10px;
    width: 350px;
    padding: 30px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.1);
}

#login-space {
    width: 100%;
}

#login-title {
    margin: 0px auto 10px auto;
    text-align: center;
    color: #505458;
    letter-spacing: 3px;
}

#login-bottom {
    display: flex;
    justify-content: space-between;
}
</style>