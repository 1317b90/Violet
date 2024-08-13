import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'
import { generInnovative } from '@/request/api'

// 任务需要的文件
const generForFile: { [key: string]: string[] } = {
  "知识产权对企业竞争力作用": ["知识产权证书   ", "公司基本资料"],
  "研究开发与技术创新管理组织情况": ["管理制度文件"],
  "科技成果转化情况": ["成果转化材料", "公司基本资料"],
  "管理与科技人员": ["人员情况说明"]

}


export const useinnovative = defineStore('innovative', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "知识产权证书   ": [],
    "成果转化材料": [],
    "人员情况说明": [],
    "管理制度文件": [],
    "公司基本资料": []

  })

  // 内容数据
  const C: { [key: string]: string } = reactive({
    "知识产权对企业竞争力作用": "",
    "研究开发与技术创新管理组织情况": "",
    "科技成果转化情况": "",
    "管理与科技人员": "",
  })


  // 发起请求，获取生成内容
  async function getGener(generType: string) {
    let fileList: Object[] = []
    for (const fileType of generForFile[generType]) {
      let fileList1 = F[fileType]

      if (fileList1.length == 0) {
        ElMessage.error("请先上传" + fileType + "！")
        // 如果发现文件不齐全，返回一个值，打断函数
        return false
      } else {
        fileList = fileList.concat(fileList1)
      }
    }

    try {
      const res = await generInnovative(fileList, generType);
      C[generType] = res.data;
      ElNotification({
        title: '生成成功',
        message: generType + '生成成功！',
        type: 'success',
        position: 'bottom-right',
      });

      // 生成完毕后自动保存一次
      sessionStorage.setItem(generType, res.data);
      return true
    } catch (err) {
      const errMsg = generType + '生成失败，请重试！';
      ElNotification({
        title: '生成失败',
        message: errMsg,
        type: 'error',
        position: 'bottom-right',
      });
      return false
    }
  }

  // 获取批量任务
  async function getGeners() {
    let tasks = []
    // 依次添加每一项任务
    for (const generType of Object.keys(C)) {
      tasks.push(getGener(generType))
    }
    return tasks
  }


  return { F, C, getGener, getGeners }
})
