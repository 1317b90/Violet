<template>
    <el-tab-pane :label="upType" :name="upType" v-if="upType != '公司基本资料'">
        <el-upload v-model:file-list="S.F[upType]" :action="actionUrl" drag multiple :on-success="handleSuccess"
            :on-error="handleError" :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove"
            :on-exceed="handleExceed">
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                将文件拖拽到这里 或者 <em>点击上传</em>
                <br>
                文件格式支持(doc docx pdf txt md)，可上传多文件，单个文件最大30MB。
            </div>
        </el-upload>
    </el-tab-pane>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadProps, UploadUserFile } from 'element-plus'
import urlJson from '@/request/url.json';

const propsData = defineProps(['upType'])
const upType = propsData.upType

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


// 一般都使用千问
let actionUrl = ref(urlJson.url + "/qwenUpFile")


// 在上传之前的钩子，返回 false 可以取消上传
function beforeUpload(file: any) {
    return true;
}

// 文件上传成功的回调
function handleSuccess(response: any) {
    // 存储数据
    sessionStorage.setItem(upType, JSON.stringify(S.F[upType]))
    const lastFileName = S.F[upType][S.F[upType].length - 1].name;
    ElNotification({
        title: '文件上传成功',
        message: lastFileName + "上传成功！",
        type: 'success',
        position: 'bottom-right',
    })
}
// 文件上传失败的回调
function handleError(error: string) {
    ElMessage.error(
        "文件上传失败，请重试！"
        // error
    )
    console.log(error)
}

// 在文件列表中点击删除
const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
    // 存储一次更新后的uploadFiles
    sessionStorage.setItem(upType, JSON.stringify(S.F[upType]))
}

// 点击了文件列表
const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
    console.log(uploadFile)
}


// 文件数超过限制时
const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
    ElMessage.error(
        "上传的文件数超过限制！"
    )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
        `确认删除 ${uploadFile.name} ?`
    ).then(
        () => true,
        () => false
    )
}
</script>

<style scoped>
.upfile_container {
    display: flex;
    /* 确保容器能够容纳两个子元素 */
    width: 100%;
}

.upfile_left,
.upfile_right {
    flex: 1;
    padding-right: 20px;

}

.upfile_left {
    border-right: 2px solid #f5f5f5;
}

.upfile_right {
    padding-left: 20px;
}
</style>