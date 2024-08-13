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

        <el-sub-menu index="2" v-if="Item.isLogin">
          <template #title><el-icon>
              <User />
            </el-icon></template>
          <el-menu-item-group :title="Item.user.name">
            <el-menu-item>{{ Item.user.count }}</el-menu-item>
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


if (sessionStorage.getItem('username')) {
  Item.isLogin = true
  Item.user.count = Number(sessionStorage.getItem('count'))
  Item.user.name = String(sessionStorage.getItem('name'))
}

function clickLoginOut() {
  Item.isLogin = false
  // 清除缓存
  sessionStorage.clear()
  // 清除pinia
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
