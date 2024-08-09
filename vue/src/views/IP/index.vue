<template>
    <div class="content">
        <div class="title-div">
            <span class="title">上传知识产权资料</span>
        </div>

        <upfileView :upType="'知识产权资料'" />

        <div class="title-div">
            <span class="title">知识产权先进性说明</span>
        </div>
        <el-tabs lazy class="demo-tabs">
            <el-tab-pane v-for="f in S.F['知识产权资料']" :key="f.uid" :label="f.name">
                <advancedView :parentID="f.uid" />

            </el-tab-pane>
        </el-tabs>

        <div class="title-div">
            <span class="title">{{ generType }}</span>
        </div>

        <div v-if="generContent" class="contentDiv">
            <el-input v-model="generContent" :autosize="{ minRows: 3 }" type="textarea"  placeholder="Please input" />

            <div class="bottomDiv">

                <el-button type="primary" round @click="clickGener" :loading="isLoading">重新生成</el-button>
                <el-button type="success" :icon="DocumentCopy" circle @click="onCopy" />
            </div>

        </div>

        <el-button v-else type="primary" plain @click="clickGener" :loading="isLoading">生成内容</el-button>
    </div>
</template>

<script lang="ts" setup>
import { computed, reactive, ref } from 'vue'
import useClipboard from "vue-clipboard3";
const { toClipboard } = useClipboard();
import type { UploadUserFile } from 'element-plus'
import { DocumentCopy } from '@element-plus/icons-vue'

import { generIPRD } from '@/request/api'

import { useIP } from '@/stores/IP'
const S = useIP()

import upfileView from './upfile.vue'
import advancedView from './advanced.vue'


const generContent = ref('')
const generType = "研发活动专利关联表"


let isLoading = ref(false)

// 生成内容
async function getGener() {

    if (S.F["知识产权资料"].length == 0) {
        ElMessage.error("请先上传知识产权资料！")
        // 如果发现文件不齐全，返回一个值，打断函数
        return false
    }

    try {
        const res = await generIPRD(S.F["知识产权资料"]);
        generContent.value = res.data;
        ElNotification({
            title: '生成成功',
            message: generType + '生成成功！',
            type: 'success',
            position: 'bottom-right',
        });

        return true
    } catch (err) {
        const errMsg = generType + '生成失败，请重试！';
        ElNotification({
            title: '生成失败',
            message: errMsg,
            type: 'error',
            position: 'bottom-right',
        });
        console.log(err)
        return false

    }
}

// 点击生成项目背景后
async function clickGener() {
    isLoading.value = true
    await getGener()
    isLoading.value = false
}


// 点击复制后
async function onCopy() {
    try {
        await toClipboard(generContent.value)
        ElMessage.success("复制成功！");
    }
    catch {
        ElMessage.error("复制失败");
    }
}


</script>

<style scoped>
.content {
    padding: 20px;
    /*
    原始高度减去padding * 2
     */
    height: calc(100% - 40px);
    /* border: solid 1px red; */
    background-color: white;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
}

.title {
    font-size: 16px;
    color: rgb(64, 158, 255);
    font-weight: 600;

}

.title-div {
    border-bottom: solid 2px #f5f5f5;
    padding-bottom: 15px;
    margin-bottom: 15px;
    margin-top: 15px;
}

.bottomDiv {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
}
</style>