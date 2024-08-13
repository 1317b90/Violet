import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'

import type { companyI } from "@/interface"
import { getItem } from '@/request/api'

export const useitem = defineStore('item', () => {
  // 当前被选中的项目id
  const id = ref()

  // 项目的名称
  const name = ref()

  const isLogin = ref(false)

  // 用户数据
  const user = ref({
    name: "",
    count: 0
  })
  // 公司基本资料
  const company = reactive<companyI>({
    id: 0,
    companyName: "",
    companyMoney: 0,
    companyIntro: "",
    companyTime: new Date(),
    companyScope: "",
    companyFile: ""
  })

  async function getItemFunc() {
    // 根据id获取具体项目数据
    await getItem(id.value).then(res => {
      Object.assign(company, res.data)
      name.value = res.data.itemName

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


  return { id, name, user, company, isLogin, getItemFunc }
})
