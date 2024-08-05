<template>
  <el-container>
    <el-header id="header">
      <el-menu :default-active="$route.fullPath" id="menu" mode="horizontal" background-color="#031629"
        text-color="#fff" active-text-color="#fff" :router="true">
        <el-menu-item>
          <!-- <img src="@/assets/images/logo.png" style="height: 50px;" alt="Logo" class="logo-img"> -->
          AI申请书系统
        </el-menu-item>
        <!-- <el-menu-item index="/home">首页</el-menu-item> -->
        <el-menu-item index="/itemSetup">立项报告</el-menu-item>
        <!-- <el-menu-item index="test">测试</el-menu-item> -->

      </el-menu>
    </el-header>
    <el-main id="main">
      <RouterView id="RouterView" />
    </el-main>
    <el-footer id="footer"><el-text>滇ICP备2024033664号</el-text></el-footer>
  </el-container>


</template>

<script setup lang="ts">


import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
#header {
  padding: 0px;
}

#main {
  padding: 30px 30px 0px 30px;
  height: calc(100vh - 60px - 40px);
}

#menu li {
  font-size: 16px;
  letter-spacing: 2px;
}

#menu .is-active {
  background-color: #317cff;
  color: white;
  border-bottom-color: #317cff;
}

#RouterView {
  background-color: white;
  height: 100%;
  /* height: calc(100vh - 60px - 40px - 50px); */
  width: 100%;
  /* padding: 20px; */
}

#footer {
  padding: 0px;
  height: 40px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
