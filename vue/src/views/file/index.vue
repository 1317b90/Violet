<template>
    <div class="content">
        <!-- style 必须写在这 不然不生效 -->
        <el-select v-model="value" placeholder="选择项目" style="width: 240px">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-button type="primary" round>新建项目</el-button>
        <br>
        <br>
        <img src="@/assets/images/fix.jpg" style="height: 250px;">
    </div>
</template>

<script lang="ts" setup>

import { ref } from 'vue'

const value = ref('')

const options = [
    {
        value: 'Option1',
        label: 'Option1',
    },
    {
        value: 'Option2',
        label: 'Option2',
    },
    {
        value: 'Option3',
        label: 'Option3',
    },
    {
        value: 'Option4',
        label: 'Option4',
    },
    {
        value: 'Option5',
        label: 'Option5',
    },
]
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
}
</style>