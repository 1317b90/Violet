import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const usehighTech = defineStore('highTech', () => {
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "知识产权资料  ": [],
    "知识产权证书或高新技术产品证书（如有）": [],
  })


  return { F }
})
