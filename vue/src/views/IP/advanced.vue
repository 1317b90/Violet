<template>

    <el-text>补充该知识产权的介绍文件：</el-text>
    <upfileView :upType="parentID" />
    <br>
    <div v-if="S.C[parentID]" class="contentDiv">
        <el-text>生成知识产权先进性说明：</el-text>
        <el-input v-model="S.C[parentID]" :autosize="{ minRows: 3 }" type="textarea" show-word-limit :maxlength="400"
            placeholder="Please input" />

        <div class="bottomDiv">
            <el-button type="primary" round @click="clickGener" :loading="isLoading">重新生成</el-button>
            <el-button type="success" :icon="DocumentCopy" circle @click="onCopy" />
        </div>
    </div>
    <el-button v-else type="primary" plain @click="clickGener" :loading="isLoading">生成知识产权先进性说明</el-button>

</template>

<script lang="ts" setup>
import upfileView from './upfile.vue'

import { ref } from 'vue';
import { DocumentCopy } from '@element-plus/icons-vue'
import useClipboard from "vue-clipboard3";
import { generIPadvanced } from '@/request/api'

const { toClipboard } = useClipboard();


import { useIP } from '@/stores/IP'
const S = useIP()

const propsData = defineProps(['parentID'])
const parentID = propsData.parentID

const parentFile = S.F['知识产权资料'].find((f) => f.uid === parentID);

let isLoading = ref(false)

// 点击生成后
async function clickGener() {
    isLoading.value = true

    // 将知识产权的文件存入,parentFile肯定是存在的 忽略报错
    // @ts-ignore
    let fileList: Object[] = [parentFile]
    if (S.F["公司基本资料"].length == 0) {
        ElMessage.error("请先上传公司基本资料！")
        return false
    } else {
        fileList = fileList.concat(S.F["公司基本资料"])
    }

    if (S.F[parentID]) {
        fileList = fileList.concat(S.F[parentID])
    }

    try {
        const res = await generIPadvanced(fileList);
        S.C[parentID] = res.data;
        ElNotification({
            title: '生成成功',
            message: '知识产权先进性说明生成成功！',
            type: 'success',
            position: 'bottom-right',
        });


        isLoading.value = false
    } catch (err) {
        const errMsg = '知识产权先进性说明生成失败，请重试！';
        ElNotification({
            title: '生成失败',
            message: errMsg,
            type: 'error',
            position: 'bottom-right',
        });
        isLoading.value = false
    }

}


// 点击复制后
async function onCopy() {
    try {
        await toClipboard(S.C[parentID])
        ElMessage.success("复制成功！");
    }
    catch {
        ElMessage.error("复制失败");
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

.bottomDiv {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
}
</style>