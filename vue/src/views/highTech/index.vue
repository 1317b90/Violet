<template>
    <div class="content">
        <div class="title-div">
            <span class="title">上传文件</span>
        </div>

        <el-tabs v-model="tabsActiveName" type="card">
            <upfileView v-for="upType in fileNameList" :upType="upType" />
        </el-tabs>

        <!-- <generView v-for="generType in generNameList" :generType="generType" /> -->
        <div class="title-div">
            <span class="title">{{ generType }}</span>
        </div>

        <div v-if="generContent" class="contentDiv">
            <el-input v-model="generContent" :autosize="{ minRows: 3 }" type="textarea" show-word-limit
                placeholder="Please input" @change="onSave" />

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
import { DocumentCopy } from '@element-plus/icons-vue'

import useClipboard from "vue-clipboard3";
const { toClipboard } = useClipboard();
import type { UploadProps, UploadUserFile } from 'element-plus'
import { usehighTech } from '@/stores/highTech'
import { generHighTech } from '@/request/api'


const S = usehighTech()

import upfileView from './upfile.vue'

const fileNameList = Object.keys(S.F)

const generContent = ref('')
const generType = "高新技术产品情况表"

// 上传tabs的默认
let tabsActiveName = ref(fileNameList[0])

// 获取文件信息的本地缓存
function getFileSession(fileType: string) {
    // 如果已经有数据，就不用重复读
    if (S.F[fileType].length != 0) {
        return
    }
    const Sfile = sessionStorage.getItem(fileType)
    if (Sfile) {
        let SfileJson = JSON.parse(Sfile)
        // 依次读取，并放入fileList
        SfileJson.forEach((value: UploadUserFile) => {
            S.F[fileType].push(value)
        });
    }
}

// 获取所有本地缓存
function getSession() {
    // 文件
    for (const fileName of fileNameList) {
        getFileSession(fileName)
    }

    const Sgener = sessionStorage.getItem(generType)
    if (Sgener) {
        generContent.value = Sgener
    }

}

getSession()


let isLoading = ref(false)


// 生成内容
async function getGener() {
    let fileList: Object[] = []
    for (const fileType of fileNameList) {
        let fileList1 = S.F[fileType]
        // 如有
        if (fileList1.length == 0 && fileType != fileNameList[1]) {
            ElMessage.error("请先上传" + fileType + "！")
            // 如果发现文件不齐全，返回一个值，打断函数
            return false
        }
        else {
            fileList = fileList.concat(fileList1)
        }
    }

    try {
        const res = await generHighTech(fileList);
        generContent.value = res.data;
        ElNotification({
            title: '生成成功',
            message: generType + '生成成功！',
            type: 'success',
            position: 'bottom-right',
        });

        // 生成完毕后自动保存一次
        sessionStorage.setItem(generType, res.data);
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

// 内容修改后自动保存
function onSave() {
    sessionStorage.setItem(generType, generContent.value)
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