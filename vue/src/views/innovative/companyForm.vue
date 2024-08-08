<template>
    <el-form ref="ruleFormRef" style="max-width: 600px" :model="S.companyForm" status-icon :rules="rules"
        label-width="auto">
        <el-form-item label="公司创建时间" prop="creationTime">
            <el-date-picker v-model="S.companyForm.creationTime" type="date" />
        </el-form-item>
        <el-form-item label="公司注册资金" prop="registeredCapital">
            <el-input-number v-model="S.companyForm.registeredCapital" :min="1" controls-position="right" />
            <span>&nbsp;&nbsp;&nbsp;/万元</span>
        </el-form-item>
        <el-form-item label="公司经营范围" prop="businessScope">
            <el-input v-model="S.companyForm.businessScope" :autosize="{ minRows: 3 }" type="textarea" />
        </el-form-item>
        <el-form-item label="公司简介" prop="intro">
            <el-input v-model="S.companyForm.intro" :autosize="{ minRows: 3 }" type="textarea" />
        </el-form-item>
        <el-form-item>
            <div class="bottomDiv">
                <el-button type="primary" @click="submitForm(ruleFormRef)">
                    保存
                </el-button>
                <!-- <el-button @click="resetForm(ruleFormRef)">清空</el-button> -->
            </div>
        </el-form-item>
    </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

import { upCompanyForm } from '@/request/api'
import { useItemSetupS } from '@/stores/itemSetupS'

const S = useItemSetupS()


const ruleFormRef = ref<FormInstance>()


const creationTimeV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('公司创建时间不能为空！'))
    } else {
        callback()
    }
}

const registeredCapitalV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('公司注册资金不能为空！'))
    } else {
        callback()
    }
}

const businessScopeV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('公司经营范围不能为空！'))
    } else {
        callback()
    }
}


const introV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('公司简介不能为空！'))
    } else {
        callback()
    }
}


const rules = reactive<FormRules<typeof S.companyForm>>({
    creationTime: [{ validator: creationTimeV, trigger: 'blur' }],
    registeredCapital: [{ validator: registeredCapitalV, trigger: 'blur' }],
    businessScope: [{ validator: businessScopeV, trigger: 'blur' }],
    intro: [{ validator: introV, trigger: 'blur' }],
})



// 点击保存后
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate(async (valid) => {
        if (valid) {
            const jsonBase = JSON.stringify(S.companyForm)

            // 将表单存储到本地
            sessionStorage.setItem('companyForm', jsonBase)

            // 将表单构建为文件发送到后端
            const blob = new Blob([jsonBase], { type: 'text/plain;charset=utf-8' });
            const formData = new FormData();
            const timestamp = Date.now();
            const fileName = `公司基本资料${timestamp}.txt`;
            // 将Blob对象添加到FormData中
            // 注意：这个名字应该与服务器期望接收的字段名相匹配
            formData.append('file', blob, fileName); // 第三个参数是可选的，表示文件名
            await upCompanyForm(formData).then(res => {
                // 为了形式一致而构建的
                const saveValue = {
                    "name": fileName,
                    "percentage": 100,
                    "status": "success",
                    "size": 1314520,
                    "raw": {
                        "uid": 1314520
                    },
                    "uid": 1314520,
                    "response": res.data
                }
                const saveFileList = [
                    saveValue
                ]
                // 以文件的id等信息存储到本地
                sessionStorage.setItem('公司基本资料', JSON.stringify(saveFileList))

                // @ts-ignore
                S.F['公司基本资料'].push(saveValue)
                // 保存表单信息
                ElMessage.success("保存成功！")
            }).catch(err => {
                ElMessage.error("保存失败！")
                console.log(err)
            })


        } else {
            ElMessage.error("保存失败！")
        }
    })
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>

<style scoped>
.bottomDiv {
    width: 100%;
    display: flex;
    justify-content: flex-end;
}

.titleIcon {
    margin-left: 10px;
    color: #529b2e;
}
</style>