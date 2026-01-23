<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="brand">
        <el-icon><Monitor /></el-icon>
        <span>App Landing Page Analyzer</span>
      </div>
      
      <div class="search-section">
        <el-input
          v-model="form.package"
          placeholder="请输入应用包名 (如: com.instagram.android)"
          class="package-input"
        >
          <template #prepend>
            <el-select v-model="form.platform" style="width: 120px">
              <el-option label="Google Play" value="google_play" />
              <el-option label="App Store" value="apple_store" />
            </el-select>
          </template>
        </el-input>

        <el-select v-model="form.region" @change="handleRegionChange" style="width: 100px; margin: 0 10px">
          <el-option v-for="r in regionOptions" :key="r.value" :label="r.label" :value="r.value" />
        </el-select>

        <el-button type="primary" :loading="submitting" @click="submitTask">
          开始抓取
        </el-button>
      </div>
    </el-header>

    <el-main>
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <span>分析记录 (近 7 天)</span>
            <el-button size="small" @click="fetchTasks">手动刷新</el-button>
          </div>
        </template>

        <el-table :data="tasks" v-loading="loading" style="width: 100%" border>
          <el-table-column label="应用详情" width="220">
            <template #default="scope">
              <div class="app-info">
                <span class="pkg-name">{{ scope.row.package_name }}</span>
                <div class="tags">
                  <el-tag size="small" :type="scope.row.platform === 'google_play' ? 'success' : 'primary'">
                    {{ scope.row.platform }}
                  </el-tag>
                  <el-tag size="small" effect="dark" type="info">
                    {{ scope.row.region.toUpperCase() }} / {{ scope.row.language }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="素材资源 (Icon + 截图)">
            <template #default="scope">
              <div v-if="scope.row.status === 'success'" class="media-container">
                <div v-if="imageData[scope.row.id]?.icon" class="media-item icon-wrapper">
                  <el-image 
                    :src="imageData[scope.row.id].icon" 
                    :preview-src-list="[imageData[scope.row.id].icon]"
                    fit="cover"
                    class="img-icon"
                  />
                  <span class="img-label">Icon</span>
                </div>
                
                <div 
                  v-for="(url, index) in imageData[scope.row.id]?.others" 
                  :key="index" 
                  class="media-item screenshot-wrapper"
                >
                  <el-image 
                    :src="url" 
                    :preview-src-list="imageData[scope.row.id].others"
                    :initial-index="index"
                    lazy
                    fit="cover"
                    class="img-screenshot"
                  />
                </div>
              </div>

              <div v-else-if="scope.row.status === 'failed'" class="status-error">
                <el-alert :title="scope.row.erro_log || '抓取过程发生异常'" type="error" :closable="false" show-icon />
              </div>
              <div v-else class="status-loading">
                <el-progress :percentage="50" indeterminate :format="() => '正在努力抓取资源...'" />
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="scope">
              <el-tag :type="statusTypeMap[scope.row.status]">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="update_at" label="时间" width="160" align="center" />
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Monitor } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 1. 基础配置与表单数据
const API_BASE = "/api" // 依赖 vite.config.js 的 proxy
const loading = ref(false)
const submitting = ref(false)
const tasks = ref([])
const imageData = reactive({}) // 存储格式 { taskId: { icon: '', others: [] } }

const regionOptions = [
  { label: '美国 (US)', value: 'us', lang: 'en' },
  { label: '中国 (CN)', value: 'cn', lang: 'zh' },
  { label: '日本 (JP)', value: 'jp', lang: 'ja' },
  { label: '韩国 (KR)', value: 'kr', lang: 'ko' },
  { label: '台湾 (TW)', value: 'tw', lang: 'zh-tw' }
]

const form = reactive({
  package: '',
  platform: 'google_play',
  region: 'us',
  lang: 'en'
})

const statusTypeMap = {
  success: 'success',
  running: 'warning',
  failed: 'danger',
  pending: 'info'
}

// 2. 地区语言联动
const handleRegionChange = (val) => {
  const opt = regionOptions.find(o => o.value === val)
  if (opt) form.lang = opt.lang
}

// 3. 获取任务列表
const fetchTasks = async () => {
  loading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/tasks`)
    tasks.value = data
    // 对成功的任务并行加载图片详情
    tasks.value.forEach(task => {
      if (task.status === 'success' && !imageData[task.id]) {
        loadTaskImages(task.id)
      }
    })
  } catch (err) {
    ElMessage.error('获取列表失败，请检查后端服务')
  } finally {
    loading.value = false
  }
}

// 4. 加载特定任务的图片详情
const loadTaskImages = async (taskId) => {
  try {
    const { data } = await axios.get(`${API_BASE}/task/${taskId}/images`)
    const imgs = data.images || []
    imageData[taskId] = {
      icon: imgs.find(i => i.Image_type === 'icon')?.url,
      others: imgs.filter(i => i.Image_type === 'other').map(i => i.url)
    }
  } catch (err) {
    console.error(`ID:${taskId} 图片加载失败`)
  }
}

// 5. 提交抓取任务
const submitTask = async () => {
  submitting.value = true;
  try {
    const res = await axios.post('/api/crawl', form);
    // 此时 res.data 已经直接包含了 images 数组
    const { task_id, images } = res.data;
    
    // 立即更新前端本地数据，无需等待轮询
    imageData[task_id] = {
      icon: images.find(i => i.type === 'icon')?.url,
      others: images.filter(i => i.type === 'other').map(i => i.url)
    };
    
    await fetchTasks(); // 刷新下方的历史列表
    ElMessage.success('抓取成功');
  } catch (err) {
    ElMessage.error('抓取失败');
  } finally {
    submitting.value = false;
  }
}


onMounted(() => {
  fetchTasks()
  // 每 10 秒自动刷新一次，追踪 running 状态
  setInterval(fetchTasks, 10000)
})
</script>

<style scoped>
.main-layout { background: #f5f7fa; min-height: 100vh; }

.header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.brand { display: flex; align-items: center; gap: 10px; font-weight: bold; color: #409EFF; font-size: 18px; }
.search-section { display: flex; align-items: center; }
.package-input { width: 450px; }

.card-header { display: flex; justify-content: space-between; align-items: center; }

.app-info { display: flex; flex-direction: column; gap: 6px; }
.pkg-name { font-family: monospace; font-weight: bold; font-size: 13px; color: #333; }
.tags { display: flex; gap: 4px; }

/* 资源预览样式 */
.media-container {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 8px 0;
  overflow-x: auto;
  scrollbar-width: thin;
}

.media-item { flex-shrink: 0; display: flex; flex-direction: column; align-items: center; }

.img-icon {
  width: 64px;
  height: 64px;
  border-radius: 14px;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.img-screenshot {
  width: 110px;
  height: 200px;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.img-label { font-size: 11px; color: #999; margin-top: 5px; font-weight: bold; }

.status-error { padding: 10px; }
.status-loading { padding: 20px; width: 300px; }

/* 自定义滚动条 */
.media-container::-webkit-scrollbar { height: 6px; }
.media-container::-webkit-scrollbar-thumb { background: #ddd; border-radius: 10px; }
</style>