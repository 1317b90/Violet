<template>
    <el-collapse-item class="collapse_item" :id="generType" :name="generType">
        <template #title>
            {{ generType }}
            <el-icon v-show="S.C[generType]" class="titleIcon">
                <SuccessFilled />
            </el-icon>
        </template>
        <div v-if="S.C[generType]" class="contentDiv">
            <el-input v-model="S.C[generType]" :autosize="{ minRows: 3 }" type="textarea" show-word-limit
                placeholder="Please input" @change="onSave" />

            <div class="bottomDiv">
                <el-button type="primary" round @click="clickGener" :loading="isLoading">重新生成</el-button>
                <el-button type="success" :icon="DocumentCopy" circle @click="onCopy" />
            </div>

        </div>
        <el-button v-else type="primary" plain @click="clickGener" :loading="isLoading">生成内容</el-button>
    </el-collapse-item>

</template>

<script lang="ts" setup>
import { ref } from 'vue'

import { SuccessFilled } from '@element-plus/icons-vue'
import { DocumentCopy } from '@element-plus/icons-vue'

import useClipboard from "vue-clipboard3";
const { toClipboard } = useClipboard();

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




const propsData = defineProps(['generType'])
const generType: string = propsData.generType



let isLoading = ref(false)


// 点击生成项目背景后
async function clickGener() {
    isLoading.value = true
    await S.getGener(generType)
    isLoading.value = false
}

function onSave() {
    sessionStorage.setItem(generType, S.C[generType])
}


// 点击复制后
async function onCopy() {
    try {
        await toClipboard(S.C[generType])
        ElMessage.success("复制成功！");
    }
    catch {
        ElMessage.error("复制失败");
    }
}

</script>

<style scoped>
.bottomDiv {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
}

.saveButton {

    width: 80px;
}

.titleIcon {
    margin-left: 10px;
    color: #529b2e;
}
</style>