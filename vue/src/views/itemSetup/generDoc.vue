<template>
    <el-collapse-item class="collapse_item" id="generDoc" name="generDoc">
        <template #title>
            生成文档
            <el-icon class="titleIcon">
                <SuccessFilled />
            </el-icon>
        </template>
        <el-button type="primary" round>预览文档</el-button>
    </el-collapse-item>
</template>

<script lang="ts" setup>
import { SuccessFilled } from '@element-plus/icons-vue'


</script>

<style scoped>
.titleIcon {
    margin-left: 10px;
    color: #529b2e;
}
</style>