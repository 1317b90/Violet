<template>
    <div class="content">
        <div id="loginDiv">
            <el-space fill direction="vertical" id="login-space" :size="20">

                <h1 id="login-title">用户注册</h1>

                <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto">
                    <!-- 账号 -->
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="Form.username" />
                    </el-form-item>
                    <!-- 密码 -->
                    <el-form-item label="密码" prop="password">
                        <el-input v-model="Form.password" type="password" show-password />
                    </el-form-item>
                    <!-- 确认密码 -->
                    <el-form-item label="确认密码" prop="password2">
                        <el-input v-model="Form.password2" type="password" show-password />
                    </el-form-item>
                    <!-- 邮箱 -->
                    <!-- placeholder="" -->
                    <el-form-item label="邮箱" prop="email">
                        <el-input v-model="Form.email" />
                    </el-form-item>

                    <!-- 底部按钮 -->
                    <el-form-item>
                        <div id="login-bottom">
                            <el-button @click="resetForm(FormRef)" class="formButton" id="registerButton">重置</el-button>
                            <el-button type="primary" @click="submitForm(FormRef)" class="formButton"
                                :loading="isLoading">
                                注册
                            </el-button>
                        </div>
                    </el-form-item>
                </el-form>


                <div id="login-bottom">
                    <!-- <el-link type="primary" @click="clickForget">忘记密码</el-link> -->
                    <el-link type="primary" @click="router.push('login')">用户登录</el-link>
                </div>
            </el-space>
        </div>
    </div>



</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';
const router = useRouter()

import type { FormInstance, FormRules } from 'element-plus'
const FormRef = ref<FormInstance>()

const inputUsername = ref("10086")
const inputPassword = ref("password")
const isLoading = ref(false)



// username验证
const usernameV = (rule: any, value: any, callback: any) => {
    const pattern = /^[a-zA-Z0-9]{3,15}$/
    if (value === '') {
        callback(new Error('用户名不能为空！'))
    }
    else if (!pattern.test(value)) {
        callback(new Error('要求3到15个字符，只能包含字母和数字'))
    } else {
        // 验证用户名的地方
        // getUser(value).then(res => {
        //     if (res.data) {
        //         callback(new Error('用户名已存在！'))
        //     } else {
        //         callback()
        //     }
        // }).catch(err => {
        //     console.log(err)
        // })

    }
}

// password验证
const passwordV = (rule: any, value: any, callback: any) => {
    const pattern = /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
    if (value === '') {
        callback(new Error('密码不能为空！'))
    } else if (!pattern.test(value)) {
        callback(new Error('要求至少8个字符，同时包含字母和数字'))
    } else {
        callback()
    }

}

// password二次验证
const password2V = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('确认密码不能为空！'))
    } else if (value !== Form.password) {
        callback(new Error("两次输入的密码不一致！"))
    } else {
        callback()
    }
}

// 邮箱验证
const emailV = (rule: any, value: any, callback: any) => {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    // 如果为空，直接跳过
    if (!value) { callback() }
    // 如果不为空，验证是否正确
    else if (!pattern.test(value)) {
        callback(new Error('邮箱地址有误！'))
    } else {
        callback()
    }
}

const Form = reactive({
    username: '',
    password: '',
    password2: '',
    email: '',
})

const rules = reactive<FormRules<typeof Form>>({
    username: [{ validator: usernameV, trigger: 'blur' }],
    password: [{ validator: passwordV, trigger: 'blur' }],
    password2: [{ validator: password2V, trigger: 'blur' }],
    email: [{ validator: emailV, trigger: 'blur' }],
})

// 单击提交按钮后
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            'vcodeShow.value = true'
        }
    })
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
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
    width: 100%;
    display: flex;
    justify-content: space-between;
}
</style>