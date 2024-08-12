<template>
    <el-container class="container">
        <el-main id="content">
            <div ref="containerRef" id="content-main">
                <el-collapse v-model="activeNames">
                    <el-collapse-item class="collapse_item" id="upfile" title="上传文件" name="upfile">
                        <el-switch class="softSwitch" v-model="isSoft" style="--el-switch-off-color: #4cce66"
                            active-text="软著" inactive-text="专利" @change="changeSwitch" size="large" />
                        <el-tabs v-model="tabsActiveName" type="card">
                            <upfileView v-for="upType in fileNameList" :upType="upType" />
                        </el-tabs>

                    </el-collapse-item>
                    <generView v-for="generType in generNameList" :generType="generType" />
                </el-collapse>
            </div>
            <div id="content-progress">
                <el-progress :percentage="progressValue" :indeterminate="progressRun" />
            </div>
        </el-main>
        <el-aside width="220px" id="aside">
            <div id="asideContainer">
                <div id="asideContent">
                    <el-anchor :container="containerRef" :offset="60" :bound="100" direction="vertical"
                        @click="clickAnchor">

                        <el-anchor-link class="anchor_title" href="#upfile" title="上传文件" />
                        <!-- <el-anchor-link class="anchor_title" href="#itemResolution" title="项目立项决议" /> -->

                        <el-anchor-link v-for="generType in generNameList" class="anchor_title" :href="'#' + generType"
                            :title="generType" />


                    </el-anchor>
                </div>
                <div id="asideBottom">
                    <el-button @click="clickGener" type="primary" :loading="progressRun">生成所有报告内容</el-button>
                    <br>
                    <el-button plain type="primary" @click="clickGenerDoc" :loading="isGenerDoc">生成报告文件</el-button>
                    <br>
                    <el-button plain @click="clickClear">清空所有内容</el-button>
                </div>
            </div>
        </el-aside>
    </el-container>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue'


import type { UploadProps, UploadUserFile } from 'element-plus'
import { generDoc } from "@/request/api"

import { usesetup1 } from '@/stores/setup1'
import { usesetup2 } from '@/stores/setup2'

// 根据本地的缓存，判断软著或专利
// 默认为软著
const isSoft = ref(JSON.parse(sessionStorage.getItem('isSoft') || 'true'))

let S: any

if (isSoft.value) {
    S = usesetup1()
} else {
    S = usesetup2()
}

function changeSwitch() {
    sessionStorage.setItem('isSoft', String(isSoft.value))
    clearSession()
}

import upfileView from './upfile.vue'
import generView from './gener.vue'


const containerRef = ref<HTMLElement | null>(null)

// 折叠框展开的部分
const activeNames = ref(['upfile'])

const generNameList = Object.keys(S.C)
const fileNameList = Object.keys(S.F)


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

// 获取生成内容的本地缓存
function getGenerSession(generType: string) {
    const Sgener = sessionStorage.getItem(generType)
    if (Sgener) {
        S.C[generType] = Sgener
    }
}

// 获取本地缓存
function getSession() {
    // 文件
    for (const fileName of fileNameList) {
        getFileSession(fileName)
    }

    // 生成内容
    for (const generName of generNameList) {
        getGenerSession(generName)
    }

}

getSession()

// 清空缓存
function clearSession() {
    for (const fileName of fileNameList) {
        if (fileName != "公司基本资料") {
            sessionStorage.removeItem(fileName)
        }
    }
    for (const generName of generNameList) {
        sessionStorage.removeItem(generName)
    }
    window.location.reload()
}

const progressRun = ref(false)

// 更新进度值
const progressValue = computed(() => {
    const totalKeys = Object.keys(S.C).length;
    const trueKeys = Object.values(S.C).filter(value => value !== '').length;

    return Math.round((trueKeys / totalKeys) * 100)
});


// 点击导航后
function clickAnchor(e: MouseEvent, href: string) {
    const newp = href.replace(/^#/, '');
    if (!activeNames.value.includes(newp)) {
        activeNames.value.push(newp);
    }
    e.preventDefault()
}



// 点击一键生成后，同时发起多个请求
async function clickGener() {

    // 判断文件是否齐全
    function isComplete() {
        for (const key in S.F) {
            if (S.F[key].length === 0) {
                ElMessage.error(key + "还未上传！")
                return false;
            }
        }
        return true;
    }
    progressRun.value = true
    // 确认文件齐全后
    if (isComplete()) {
        const tasks = await S.getGeners()
        try {
            // 同时发送所有请求，并等待所有请求完成
            const results = await Promise.all(tasks);
            console.log(results)
            ElMessage.success("所有任务已完成！")
        } catch (error) {
            // 处理其他错误
            console.error(error);
        } finally {
            progressRun.value = false
        }
    } else {
        progressRun.value = false
    }
}

// 点击一键清空后
function clickClear() {
    clearSession()
}

const isGenerDoc = ref(false)

// 点击生成文档后
async function clickGenerDoc() {
    // 判断内容是否齐全
    function isComplete() {
        for (const key in S.C) {
            if (S.C[key] == "") {
                ElMessage.error(key + "内容为空！")
                return false;
            }
        }
        return true;
    }
    isGenerDoc.value = true

    if (isComplete()) {
        await generDoc(S.C).then(res => {
            console.log(res)
            isGenerDoc.value = false
            ElMessage.success("生成成功！")
            window.open(res.data, '_blank');
        }).catch(err => {
            isGenerDoc.value = false
            console.log(err)
            ElMessage.error("生成失败")
        })
    } else {
        isGenerDoc.value = false
    }


}

</script>

<style scoped>
/* 这是一整个区域 */
.container {
    /* 为什么不用100%-40px？ 我也不知道，反正就是这么神奇 */
    height: 100%;
}

/* 布局里的main，默认有20padding，所以要去掉 */
/* 这里的main包括了主要页面和进度条 */
#content {
    /* border-radius: 10px; */
    padding: 0px;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
    background-color: white;
}

/* 左边真正内容区域  */
#content-main {
    overflow-y: auto;
    /* 此处减去的40px是进度条 */
    height: calc(100% - 20px);
    /* border: #529b2e solid 1px; */
}

/* 内容区域的进度条 */
#content-progress {
    height: 20px;
    padding-left: 20px;
    width: calc(100% - 20px);
    /* padding-top: 5px; */
    /* border: #529b2e solid 1px; */
}

/* 右边导航栏 */
#aside {
    /* border-radius: 10px; */
    margin-left: 20px;
    height: 100%;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
    background-color: white;
}

#asideContainer {
    display: flex;
    flex-direction: column;
    height: 100%;
}

#asideContent {
    padding-right: 10px;
    flex-grow: 1;
}

#asideBottom {
    padding: 5px 15px 15px 15px;
}

#asideBottom .el-button {
    width: 100%;
    /* width: 160px; */
    margin-top: 10px;
}



/* 导航栏文字 */
::v-deep(.anchor_title a) {
    margin-top: 5px;
    font-size: 15px;
    line-height: 40px;
    padding: 0px 0px 0px 20px;
    color: rgba(0, 0, 0, 0.88);
    border-radius: 10px;
}

::v-deep(.anchor_title a:hover) {
    background-color: #f0f0f0;
    /* color: #031629; */
}

::v-deep(.anchor_title .is-active) {
    font-weight: 600;
    background-color: #e8f4ff;
    color: rgb(22, 119, 255);
}

::v-deep(.el-anchor__marker) {
    display: none;
}



.titleIcon {
    margin-left: 10px;
    color: #529b2e;
}


.el-collapse {
    border: 0;
}

/* 折叠框文本 */
::v-deep(.el-collapse-item) {
    /* border: solid 2px #f5f5f5; */
    margin-bottom: 15px;
    /* border-radius: 15px; */
}

::v-deep(.el-collapse-item__header) {
    padding-left: 20px;
    font-size: 16px;
    border-bottom: solid 2px #f5f5f5;
}

::v-deep(.el-collapse-item__content) {
    padding: 20px;
}

::v-deep(.collapse_item .is-active) {
    color: rgb(64, 158, 255);
    font-weight: 600;
}

.softSwitch {
    float: right;
    border-bottom: solid 1px rgb(228, 231, 237);
}
</style>