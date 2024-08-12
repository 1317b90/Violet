<template>
    <div class="content">
        <div class="title-div">
            <span class="title">上传知识产权资料</span>
        </div>
        <upfileView :upType="'知识产权资料'" />
        <el-alert title="每项知识产权上传一份资料即可" type="info" show-icon />
        <div class="title-div">
            <span class="title">知识产权先进性说明</span>
        </div>
        <el-tabs lazy class="demo-tabs">
            <el-tab-pane v-for="f in S.F['知识产权资料']" :key="f.uid" :label="f.name">
                <advancedView :parentID="f.uid" />

            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script lang="ts" setup>
import type { UploadProps, UploadUserFile } from 'element-plus'

import { useIP } from '@/stores/IP'
const S = useIP()

import upfileView from './upfile.vue'
import advancedView from './advanced.vue'


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

getFileSession("公司基本资料")

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