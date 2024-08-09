<template>
    <div class="content">
        <!-- style 必须写在这 不然不生效 -->
        <!-- <el-select v-model="value" placeholder="选择项目" style="width: 240px">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-button type="primary" round>新建项目</el-button> -->

        <div class="title-div">
            <span class="title">公司基本资料</span>
        </div>
        <companyForm />
    </div>
</template>

<script lang="ts" setup>

import { ref } from 'vue'


import companyForm from './companyForm.vue'


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
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
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
</style>