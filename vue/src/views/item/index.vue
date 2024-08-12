<template>
    <div class="content">
        <el-select v-model.number="Item.id" placeholder="选择项目" style="width: 240px;margin-right: 10px;"
            @change="changeItem">
            <el-option v-for="item in itemSelect" :key="item.id" :label="item.itemName" :value="item.id" />
        </el-select>
        <el-button type="primary" round :icon="CirclePlus" @click="clickAddItem">新建项目</el-button>
        <el-button v-if="Item.id" type="danger" :icon="Delete" circle @click="clickDelItem" />
        <el-divider />
        <div v-if="Item.id">
            <el-card style="max-width: 480px">
                <template #header>
                    <div class="card-header">
                        <span>项目名称</span>
                    </div>
                </template>
                <el-input v-model="Item.name" style="max-width: 600px" placeholder="Please input">
                    <template #append>
                        <el-button @click="clickSetItemName">保存</el-button>
                    </template>
                </el-input>
            </el-card>
            <br />
            <el-card style="max-width: 800px">
                <template #header>
                    <div class="card-header">
                        <span>公司基本资料</span>
                    </div>
                </template>
                <companyForm />
            </el-card>

        </div>

    </div>
</template>

<script lang="ts" setup>

import { reactive, ref } from 'vue'

import { CirclePlus, Delete } from '@element-plus/icons-vue'
import companyForm from './companyForm.vue'
import type { itemSelectI } from "@/interface"

import { getItem, getItems_by_user, addItem, delItem, setItemName } from '@/request/api'
import { useitem } from '@/stores/item'
const Item = useitem()

const username = sessionStorage.getItem('username') || ''


// 可选择的项目列表
const itemSelect = reactive<itemSelectI[]>([])

async function getData() {
    // 根据用户名获取所有项目
    await getItems_by_user(username).then(res => {

        for (const item of res.data) {
            itemSelect.push({
                id: item.id,
                itemName: item.itemName
            }
            )
        }
    }).catch(
        err => {
            console.log(err)
        }
    )
}

getData()

// 点击增加项目 
async function clickAddItem() {
    await addItem(username).then(res => {
        // 修改默认的指针
        localStorage.setItem(username + "itemId", String(res.data.id))
        window.location.reload()
        ElMessage.success("创建成功！");
    }).catch(
        err => {
            ElMessage.error("创建失败，" + err)
        }
    )
}

// 点击修改项目名称
async function clickSetItemName() {
    await setItemName(Item.id, Item.name).then(res => {
        const index = itemSelect.findIndex((item) => item.id === Item.id);
        if (index !== -1) {
            itemSelect[index].itemName = Item.name;
        }
        ElMessage.success("修改成功！");
    }).catch(
        err => {
            ElMessage.error("修改失败，" + err)
        }
    )
}


// 项目选择改变时,根据id查询项目，并更新值
async function changeItem() {

    localStorage.setItem(username + "itemId", String(Item.id))

    await getItem(Item.id).then(res => {
        Object.assign(Item.company, res.data)
        Item.name = res.data.itemName

        // 为了形式一致而构建的
        const saveValue = {
            "name": "公司基本资料",
            "percentage": 100,
            "status": "success",
            "size": 1314520,
            "raw": {
                "uid": 1314520
            },
            "uid": 1314520,
            "response": res.data.companyFile
        }
        const saveFileList = [
            saveValue
        ]
        // 以文件的id等信息存储到本地
        sessionStorage.setItem('公司基本资料', JSON.stringify(saveFileList))

    }

    ).catch(err => {
        ElMessage.error("项目获取失败！" + err)
    })
}


// 点击删除项目后
async function clickDelItem() {
    await ElMessageBox.confirm("确定删除项目吗？", "删除项目", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
    }).then(async () => {
        await delItem(Item.id).then(res => {
            // 删除默认的指针
            localStorage.removeItem(username + "itemId")
            window.location.reload()
            ElMessage.success("删除成功！")
        }).catch(err => { ElMessage.error("删除失败," + err) })
    })
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
</style>