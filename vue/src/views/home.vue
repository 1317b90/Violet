<template>
    <div class="content">
        <img src="@/assets/images/fix.jpg" style="height: 250px;">
    </div>

</template>

<script lang="ts" setup>
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

#nei {
    border: solid 1px red;
    height: 300px;
}
</style>