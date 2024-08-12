<template>
  <el-container>
    <el-header id="appHeader">
      <el-menu id="appMenu" :default-active="$route.fullPath" mode="horizontal" :ellipsis="false"
        background-color="#031629" text-color="#fff" active-text-color="#fff" :router="true">
        <el-menu-item>
          <img src="@/assets/images/logo_title.png" style="height: 50px;" alt="Logo" class="logo-img">
        </el-menu-item>
        <!-- <el-menu-item index="/">首页</el-menu-item> -->
        <el-menu-item index="/item">项目管理</el-menu-item>
        <el-menu-item index="/IP">知识产权</el-menu-item>
        <el-menu-item index="/setup">立项报告</el-menu-item>
        <el-menu-item index="/RDactivate">研发活动情况表</el-menu-item>
        <el-menu-item index="/highTech">高新技术产品情况表</el-menu-item>
        <el-menu-item index="/achieve">成果转化说明</el-menu-item>
        <el-menu-item index="/innovative">企业创新能力评价</el-menu-item>
        <el-menu-item index="/manage">研究开发组织管理水平</el-menu-item>
        <div class="flex-grow" />

        <el-sub-menu index="2" v-if="username">
          <template #title><el-icon>
              <User />
            </el-icon></template>
          <el-menu-item-group :title="name">
            <el-menu-item>{{ count }}</el-menu-item>
            <el-menu-item @click="clickLoginOut">退出</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item index="/login" v-else>登陆</el-menu-item>

      </el-menu>
    </el-header>
    <el-main id="appMain">
      <RouterView />
    </el-main>
    <el-footer id="appFooter"><el-text>滇ICP备2024033664号</el-text></el-footer>
  </el-container>


</template>

<script setup lang="ts">
import { User } from '@element-plus/icons-vue'
import { RouterLink, RouterView } from 'vue-router'
import router from './router';
import { useitem } from '@/stores/item'
const Item = useitem()

const username = sessionStorage.getItem('username') || ''
const name = sessionStorage.getItem('name')
const count = sessionStorage.getItem('count')

import { getItem, getItems_by_user, addItem } from '@/request/api'

// 初始化数据
async function getData() {
  // 默认选择的项目id
  const itemID = localStorage.getItem(username + "itemId")

  // 如果本地存在默认id的情况下：
  if (itemID) {
    Item.id = Number(itemID)
    await getItem(Number(itemID)).then(res => {
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
      ElMessage.error("项目获取失败，" + err)
    })
  }



}

getData()


function clickLoginOut() {
  sessionStorage.clear()
  window.location.reload()
  router.push('login')
}
</script>

<style scoped>
#appHeader {
  padding: 0px;
}

#appMain {
  padding: 20px 20px 0px 20px;
  /*整个页面高度-导航栏（60）-底部备案（30）*/
  height: calc(100vh - 60px - 30px);
  width: 100vw;

  /* 装修线 */
  /* border: solid 1px red; */
}

#appMenu {
  width: 100%;
}

#appMenu li {
  font-size: 16px;
  /* letter-spacing: 2px; */
}

#appMenu .is-active {
  background-color: #317cff;
  color: white;
  border-bottom-color: #317cff;
}


#appFooter {
  padding: 0px;
  height: 30px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  /* border: solid red 1px; */
}

/* 让用户编辑在最右边 */
.flex-grow {
  flex-grow: 1;
}
</style>
