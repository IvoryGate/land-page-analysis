<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="brand">
        <el-icon><Monitor /></el-icon>
        <span>Landing Page Analyser</span>
      </div>
      
      <div class="header-actions">
        <el-radio-group v-model="viewMode" size="large">
          <el-radio-button value="list">任务看板</el-radio-button>
          <el-radio-button value="compare">地区对比</el-radio-button>
          <el-radio-button value="batch">批量管理</el-radio-button>
        </el-radio-group>
      </div>
    </el-header>

    <el-main>
      <div v-if="viewMode === 'list'">
        <el-card shadow="never" class="search-card">
          <el-form :inline="true" :model="form">
            <el-form-item label="包名">
              <el-input v-model="form.package" placeholder="com.example.app / 6636468266" style="width: 280px" />
            </el-form-item>
            <el-form-item label="平台">
              <el-select v-model="form.platform" style="width: 140px">
                <el-option label="Google Play" value="google_play" />
                <el-option label="App Store" value="apple_store" />
              </el-select>
            </el-form-item>
            <el-form-item label="地区">
              <el-select v-model="form.region" @change="handleRegionChange" style="width: 130px">
                <el-option v-for="r in regionOptions" :key="r.value" :label="r.label" :value="r.value" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitTask(false)" :loading="submitting">查询</el-button>
              <el-button type="success" plain @click="submitTask(true)" :loading="submitting">全地区添加</el-button>
              <el-button @click="fetchTasks">刷新列表</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-table :data="tasks" v-loading="loading" border class="main-table">
          <el-table-column label="应用详情" width="240">
            <template #default="scope">
              <div class="app-info">
                <span class="pkg-name">{{ scope.row.package_name }}</span>
                <div class="tags">
                  <el-tag size="middle" effect="dark">{{ scope.row.platform }}</el-tag>
                  <el-tag size="middle" type="info" style="margin-left: 5px">{{ scope.row.region.toUpperCase() }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="素材预览">
            <template #default="scope">
              <div v-if="imageData[scope.row.id]" class="media-container">
                <el-image 
                  v-if="imageData[scope.row.id].icon"
                  :src="imageData[scope.row.id].icon" 
                  class="img-icon"
                  fit="cover"
                  :preview-src-list="[imageData[scope.row.id].icon]"
                  preview-teleported
                />
                <div class="screenshot-strip">
                  <el-image 
                    v-for="(url, index) in imageData[scope.row.id].others" 
                    :key="index" 
                    :src="url" 
                    class="img-screenshot"
                    fit="cover"
                    lazy
                    :preview-src-list="imageData[scope.row.id].others"
                    :initial-index="index"
                    preview-teleported
                  />
                </div>
              </div>
              <div v-else-if="scope.row.status === 'running'">
                <el-text type="primary"><el-icon class="is-loading"><Loading /></el-icon> 正在实时分析抓取中...</el-text>
              </div>
              <div v-else>
                <el-text type="info">无数据或等待抓取 ({{ scope.row.status }})</el-text>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="120" align="center">
            <template #default="scope">
              <el-button type="danger" size="small" :icon="Delete" circle @click="handleDelete(scope.row.id)" />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-if="viewMode === 'compare'">
        <el-card shadow="never">
          <template #header>
            <el-input v-model="comparePkg" placeholder="输入包名对比多地区素材" style="width: 450px">
              <template #append><el-button @click="runCompare">开始对比</el-button></template>
            </el-input>
          </template>
          <div class="compare-grid" v-if="compareResults.length">
            <div v-for="item in compareResults" :key="item.id" class="compare-column">
              <div class="column-title">{{ item.region.toUpperCase() }}</div>
              <div class="column-content" v-if="imageData[item.id]">
                <el-image :src="imageData[item.id].icon" class="compare-icon" />
                <el-divider>预览</el-divider>
                <el-image 
                  v-for="img in imageData[item.id].others.slice(0, 3)" 
                  :key="img" :src="img" 
                  class="compare-ss" 
                  fit="contain" 
                />
              </div>
            </div>
          </div>
          <el-empty v-else description="请输入包名进行对比" />
        </el-card>
      </div>

      <div v-if="viewMode === 'batch'">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="never" header="批量添加任务">
              <el-upload drag action="#" :auto-upload="false" :on-change="(file) => handleCSV(file, 'add')">
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">拖拽 CSV 文件上传</div>
              </el-upload>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="never" header="批量删除记录">
              <el-upload drag action="#" :auto-upload="false" :on-change="(file) => handleCSV(file, 'delete')">
                <el-icon class="el-icon--upload" style="color: #f56c6c"><DeleteFilled /></el-icon>
                <div class="el-upload__text">拖拽 CSV 文件批量删除</div>
              </el-upload>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Monitor, Delete, Loading, UploadFilled, DeleteFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

// --- 状态定义 ---
const viewMode = ref('list')
const loading = ref(false)
const submitting = ref(false)
const tasks = ref([])
const compareResults = ref([])
const comparePkg = ref('')
const imageData = reactive({}) // 存储格式：{ taskId: { icon: '', others: [] } }

const regionOptions = [
  { label: '美国 (US)', value: 'us', lang: 'en' },
  { label: '中国 (CN)', value: 'cn', lang: 'zh' },
  { label: '日本 (JP)', value: 'jp', lang: 'ja' },
  { label: '韩国 (KR)', value: 'kr', lang: 'ko' }
]

const form = reactive({ package: '', platform: 'google_play', region: 'us', lang: 'en' })

// --- 核心逻辑 ---

// 1. 提交任务（单条分析 / 全地区添加）
const submitTask = async (allRegions = false) => {
  if (!form.package) return ElMessage.warning('请输入包名')
  submitting.value = true
  
  try {
    if (allRegions) {
      for (const opt of regionOptions) {
        const res = await axios.post('/api/get', { ...form, region: opt.value, lang: opt.lang })
        console.log(res.data)
        handleSingleResponse(res.data, { ...form, region: opt.value })
      }
      ElMessage.success('全地区任务已添加')
    } else {
      const { data } = await axios.post('/api/get', form)
      handleSingleResponse(data, form)
      ElMessage.success('分析完成')
    }
  } catch (error) {
    ElMessage.error('请求失败，请检查后端 API')
  } finally {
    submitting.value = false
  }
}

// 2. 处理 API 返回的数据并渲染
const handleSingleResponse = (data, originForm) => {
  const taskId = data.task_id
  
  // 解析后端 images 结构 (后端返回 type: "icon" / "other")
  imageData[taskId] = {
    icon: data.images.find(i => i.type === 'icon')?.url,
    others: data.images.filter(i => i.type === 'other').map(i => i.url)
  }

  // 构造展示用的任务对象
  const taskEntry = {
    id: taskId,
    package_name: originForm.package,
    platform: originForm.platform,
    region: originForm.region,
    status: data.status
  }

  // 如果列表中已有该任务，则更新；否则插入到首行
  const idx = tasks.value.findIndex(t => t.id === taskId)
  if (idx !== -1) {
    tasks.value[idx] = taskEntry
  } else {
    tasks.value.unshift(taskEntry)
  }
}

// 3. 获取任务列表 (假设后端有对应的 GET 接口)
const fetchTasks = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/get') 
    // 注意：如果列表接口不带 images 详情，你可能需要循环请求或后端支持 JOIN
    tasks.value = data
  } catch (e) {
    console.warn('获取列表失败，请确保 GET /api/get 接口可用')
  } finally {
    loading.value = false
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除该记录吗？').then(async () => {
    // 假设后端有 DELETE 接口
    await axios.delete(`/api/task/${id}`)
    tasks.value = tasks.value.filter(t => t.id !== id)
    delete imageData[id]
    ElMessage.success('已删除')
  })
}

const runCompare = async () => {
  if (!comparePkg.value) return
  const { data } = await axios.get(`/api/get?package=${comparePkg.value}`)
  compareResults.value = data
  // 对比视图也需要加载图片
  data.forEach(item => {
    if (item.images) {
        imageData[item.id] = {
            icon: item.images.find(i => i.type === 'icon')?.url,
            others: item.images.filter(i => i.type === 'other').map(i => i.url)
        }
    }
  })
}

const handleRegionChange = (val) => {
  const opt = regionOptions.find(o => o.value === val)
  if (opt) form.lang = opt.lang
}

// 处理 CSV 略 (与之前逻辑一致，仅需注意调用 API 的参数)
const handleCSV = (file, mode) => { /* ... */ }

onMounted(fetchTasks)
</script>

<style scoped>
.main-layout { background: #f0f2f5; min-height: 100vh; }
.header { background: #fff; border-bottom: 1px solid #dcdfe6; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.brand { display: flex; align-items: center; gap: 10px; color: #409eff; font-weight: bold; font-size: 1.2rem; }

.search-card { margin-bottom: 20px; }
.main-table { background: #fff; }

.app-info { display: flex; flex-direction: column; gap: 5px; }
.pkg-name { font-family: monospace; font-size: 13px; color: #303133; font-weight: bold; word-break: break-all; }

.media-container { display: flex; gap: 15px; align-items: flex-start; padding: 10px 0; }
.img-icon { width: 60px; height: 60px; border-radius: 12px; flex-shrink: 0; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); }
.screenshot-strip { display: flex; gap: 10px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px; }
.img-screenshot { width: 100px; height: 180px; border-radius: 6px; flex-shrink: 0; border: 1px solid #ebeef5; cursor: pointer; transition: transform 0.2s; }
.img-screenshot:hover { transform: scale(1.05); }

.compare-grid { display: flex; gap: 20px; overflow-x: auto; margin-top: 20px; padding-bottom: 20px; }
.compare-column { width: 260px; flex-shrink: 0; background: #fafafa; border: 1px solid #ebeef5; border-radius: 8px; padding: 15px; }
.column-title { text-align: center; font-weight: bold; margin-bottom: 15px; color: #606266; }
.compare-icon { width: 80px; height: 80px; border-radius: 15px; display: block; margin: 0 auto; }
.compare-ss { width: 100%; height: 350px; border-radius: 8px; margin-top: 10px; }
</style>