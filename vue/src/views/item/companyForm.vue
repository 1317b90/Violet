<template>
    <el-form ref="ruleFormRef" :model="Item.company" status-icon :rules="rules" label-width="auto">

        <el-form-item label="公司名称" prop="companyName">
            <el-input v-model="Item.company.companyName" />
        </el-form-item>

        <el-form-item label="公司创建时间" prop="companyTime">
            <el-date-picker v-model="Item.company.companyTime" type="date" />
        </el-form-item>
        <el-form-item label="公司注册资金" prop="companyMoney">
            <el-input-number v-model.number="Item.company.companyMoney" :min="1" controls-position="right" />
            <span>&nbsp;&nbsp;&nbsp;/万元</span>
        </el-form-item>
        <el-form-item label="公司经营范围" prop="companyScope">
            <el-input v-model="Item.company.companyScope" :autosize="{ minRows: 3 }" type="textarea" />
        </el-form-item>
        <el-form-item label="公司简介" prop="companyIntro">
            <el-input v-model="Item.company.companyIntro" :autosize="{ minRows: 3 }" type="textarea" />
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

import { setItemCompany, upCompanyForm } from '@/request/api'

import { useitem } from '@/stores/item'
const Item = useitem()

const ruleFormRef = ref<FormInstance>()


const companyNameV = (rule: any, value: any, callback: any) => {
    if (value === '' || value === null) {
        callback(new Error('公司名称不能为空！'))
    } else {
        callback()
    }
}



const companyTimeV = (rule: any, value: any, callback: any) => {
    if (value === '' || value === null) {
        callback(new Error('公司创建时间不能为空！'))
    } else {
        callback()
    }
}

const companyMoneyV = (rule: any, value: any, callback: any) => {
    if (value === '' || value === null) {
        callback(new Error('公司注册资金不能为空！'))
    } else {
        callback()
    }
}

const companyScopeV = (rule: any, value: any, callback: any) => {
    if (value === '' || value === null) {
        callback(new Error('公司经营范围不能为空！'))
    } else {
        callback()
    }
}


const companyIntroV = (rule: any, value: any, callback: any) => {
    if (value === '' || value === null) {
        callback(new Error('公司简介不能为空！'))
    } else {
        callback()
    }
}


const rules = reactive<FormRules<typeof Item.company>>({
    companyName: [{ validator: companyNameV, trigger: 'blur' }],
    companyTime: [{ validator: companyTimeV, trigger: 'blur' }],
    companyMoney: [{ validator: companyMoneyV, trigger: 'blur' }],
    companyScope: [{ validator: companyScopeV, trigger: 'blur' }],
    companyIntro: [{ validator: companyIntroV, trigger: 'blur' }],
})


// 将表单转化为文件保存，并获取kimi的文件id
async function saveCompanyFile() {
    // 转为中文名
    const chinaCompany = {
        "公司名称": Item.company.companyName,
        "公司创建时间": Item.company.companyTime,
        "公司注册资金": Item.company.companyMoney,
        "公司经营范围": Item.company.companyScope,
        "公司简介": Item.company.companyIntro
    }
    const jsonBase = JSON.stringify(chinaCompany)
    const blob = new Blob([jsonBase], { type: 'text/plain;charset=utf-8' });
    const formData = new FormData();
    const timestamp = Date.now();
    const fileName = `公司基本资料${timestamp}.txt`;

    // 将Blob对象添加到FormData中
    // 注意：这个名字应该与服务器期望接收的字段名相匹配
    formData.append('file', blob, fileName); // 第三个参数是可选的，表示文件名

    await upCompanyForm(formData).then(res => {

        Item.company.companyFile = res.data
        // 为了形式一致而构建的
        const saveValue = {
            "name": "公司基本资料",
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
        return true
    }).catch(err => {
        throw new Error(err);
    })
}

// 保存整个表单
async function saveCompanyForm() {
    await setItemCompany(Item.company).then(res => {
        return true
    }).catch(err => {
        throw new Error(err);
    })
}


// 点击保存后
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate(async (valid) => {
        if (valid) {
            try {
                await saveCompanyFile();
                await saveCompanyForm();
                ElMessage.success("保存成功！")

            } catch (err) {
                ElMessage.error("保存失败，" + err)
            }
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