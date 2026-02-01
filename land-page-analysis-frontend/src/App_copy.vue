<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="brand">
        <el-icon class="logo"><Monitor /></el-icon>
        <span>Landing Page Analyser</span>
      </div>
      <el-radio-group v-model="viewMode" fill="#409eff">
        <el-radio-button label="任务看板" value="task_board" />
        <el-radio-button label="地区对比" value="region_compare" />
        <el-radio-button label="批量管理" value="batch_manage" />
      </el-radio-group>
    </el-header>
    <el-main>
      <div v-if="viewMode === 'task_board'">
        <el-card class="search-card" shadow="never">
          <el-form class="search-form" :inline="true" :model="form" >
            <el-form-item label="包名">
              <el-input 
              v-model="form.package"
              placeholder="com.example.app / 6636468266" 
              style="width: 280px" 
              @change = "autoChoosePlatform"
              clearable/>
            </el-form-item>
            <el-form-item label="平台">
              <el-select v-model="form.platform" style="width: 160px">
                <el-option label="Google Play" value="google_play" />
                <el-option label="App Store" value="apple_store" />
              </el-select>
            </el-form-item>
            <el-form-item label="地区">
              <el-select v-model="form.region" @change="handleRegionChange" style="width: 160px">
                <el-option v-for="(item, region) in regionMap" :key="region" :label="item.label" :value="region" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchSingleRecord" :loading="submitting">查询</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        <el-table :data="taskList" v-loading="loading" border class="task-list" row-key="id">
          <el-table-column label="应用详情" width="240px">
            <template #default="scope">
              <div class="app-info">
                <span class="pkg-name">{{ scope.row.package_name }}</span>
                <div class="tags">
                  <el-tag size="default" effect="dark">{{ scope.row.platform }}</el-tag>
                  <el-tag size="default" type="info" style="margin-left: 5px">{{ scope.row.region.toUpperCase() }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="素材预览">
            <template #default="scope">
              <div class="media-container" v-if="imageData[scope.row.id]">
                <el-image 
                class="img-icon"
                v-if="imageData[scope.row.id].icon"
                  :src="imageData[scope.row.id].icon"
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
                    show-progress  
                  />
                </div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-if="viewMode === 'region_compare'">
        <el-card class="search-card" shadow="never">
          <el-form class="search-form" :inline="true" :model="form" >
            <el-form-item label="包名">
              <el-input 
              v-model="form.package"
              placeholder="com.example.app / 6636468266" 
              style="width: 280px" 
              @change = "autoChoosePlatform"
              clearable/>
            </el-form-item>
            <el-form-item label="平台">
              <el-select v-model="form.platform" style="width: 160px">
                <el-option label="Google Play" value="google_play" />
                <el-option label="App Store" value="apple_store" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchAllRegion" :loading="submitting">查询</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        <el-table :data="regionTaskList" v-loading="loading" border class="task-list" row-key="id">
          <el-table-column label="应用详情" width="240px">
            <template #default="scope">
              <div class="app-info">
                <span class="pkg-name">{{ scope.row.package_name }}</span>
                <div class="tags">
                  <el-tag size="default" effect="dark">{{ scope.row.platform }}</el-tag>
                  <el-tag size="default" type="info" style="margin-left: 5px">{{ scope.row.region.toUpperCase() }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="素材预览">
            <template #default="scope">
              <div class="media-container" v-if="regionImageData[scope.row.id]">
                <el-image 
                class="img-icon"
                v-if="regionImageData[scope.row.id].icon"
                  :src="regionImageData[scope.row.id].icon"
                  fit="cover"
                  :preview-src-list="[regionImageData[scope.row.id].icon]"
                  preview-teleported
                />
                <div class="screenshot-strip">
                  <el-image 
                    v-for="(url, index) in regionImageData[scope.row.id].others" 
                    :key="index" 
                    :src="url" 
                    class="img-screenshot"
                    fit="cover"
                    lazy
                    :preview-src-list="regionImageData[scope.row.id].others"
                    :initial-index="index"
                    preview-teleported
                    show-progress  
                  />
                </div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-main>
    <el-footer class="footer" height="60px">
      <p>Copyright © 2026 - present IvoryGate. All Rights Reserved.</p>
    </el-footer>
  </el-container>
</template>

<script setup>
import { Monitor } from '@element-plus/icons-vue';
import axios from 'axios';
import { ref, reactive } from 'vue'
import { watch } from 'vue'

// ---- 状态变量 -----
const viewMode = ref('task_board')    // 当前渲染面板
const submitting = ref(false)         // 查询按钮，点击后变成加载状体，避免重复提交
const loading = ref(false)
const taskList = ref([])              // 存放组织好的任务列表数据，用于渲染展示任务列
const imageData = reactive({})        // 存放组织好的图片url数据，用于渲染素材列
const regionTaskList = ref([])        // 存放用于构建分地区任务列表的任务列数据
const regionImageData = reactive({})  // 纯放用于渲染分地区的素材列的数据

const form = reactive({ package: '', platform: 'google_play', region: 'us', lang: 'en' })

const regionMap = {
  us: { label: '美国 (US)', lang: 'en' },
  cn: { label: '中国 (CN)', lang: 'zh' }
}

// ---- 方法 ----

// 根据包名自动推断平台
const autoChoosePlatform = (value) => {
  if (/^\d/.test(value)) {
    form.platform = "apple_store"
  } else {
    form.platform = "google_play"
  }
}

// 切换国家
const handleRegionChange = (value) => {
  form.region = value
}

watch(viewMode, (newMode) => {

  submitting.value = false;
  loading.value = false;
  
  form.package = ''; 
  
})

// 提交请求
const fetchSingleRecord = async () => {
  if (!form.package) return ElMessage.warning('包名缺失')
  submitting.value = true
  loading.value = true
  try {
    const { data } = await axios.post('/api/get', { ...form })
    handleSingleResponse(data, form)
  } catch (error) {
    console.warn("check POST /api/get interface")
  } finally {
    submitting.value = false
    loading.value = false
  }
}

// 处理单条数据
const handleSingleResponse = (data, originForm) => {
  const taskId = data.task_id
  imageData[taskId] = {
    icon: data.images.find(i => i.type === 'icon')?.url,
    others: data.images.filter(i => i.type === 'other').map(i => i.url)
  }
  const taskEntry = {
    id: taskId,
    package_name: originForm.package,
    platform: originForm.platform,
    region: originForm.region,
    status: data.status
  }
  const idx = taskList.value.findIndex(t => t.id === taskId)
  if (idx !== -1) {
    taskList.value[idx] = taskEntry
  } else {
    taskList.value.unshift(taskEntry)
  }
}

// 处理多条数据
const handleMultipleResponse = (data, package_name, platform) => {
  const taskId = data.task_id;
  if(!taskId) return;
  regionImageData[taskId] = {
    icon: data.images.find(i => i.type === 'icon')?.url,
    others: data.images.filter(i => i.type === 'other').map(i => i.url)
  }
  const taskEntry = {
    id: taskId,
    package_name: package_name,
    platform: platform,
    region: (data.region || 'Unknown').toUpperCase(),
    status: data.status
  };
  const idx = regionTaskList.value.findIndex(t => t.id === taskId);
  if (idx !== -1) {
    regionTaskList.value[idx] = taskEntry;
  } else {
    regionTaskList.value.push(taskEntry);
  }
}

const fetchAllRegion = async () => {
  if (!form.package) return ElMessage.warning('包名缺失');

  // 初始化状态
  submitting.value = true;
  loading.value = true;
  regionTaskList.value = [];

  try {
    const response = await fetch('/api/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        package: form.package,
        platform: form.platform
      })
    });

    if (!response.body) throw new Error('ReadableStream not supported');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (loading.value) loading.value = false;

      buffer += decoder.decode(value, { stream: true });

      let lines = buffer.split('\n');

      buffer = lines.pop();

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);

          handleMultipleResponse(data, form.package, form.platform);
        } catch (e) {
          console.error("解析流式JSON失败", e);
        }
      }
    }
  } catch (error) {
    console.error("获取流数据失败", error);
    ElMessage.error('地区对比请求失败');
  } finally {
    submitting.value = false;
    loading.value = false;
  }
};

</script>

<style>
.main-layout { background: #f0f2f5; min-height: 100vh; }
.header { background: #fff; border-bottom: 1px solid #dcdfe6; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.brand { display: flex; align-items: center; gap: 10px; color: #409eff; font-weight: bold; font-size: 1.2rem; }
.logo.el-icon { height: 32px; width: 32px; padding-right: px; }
.footer { display: flex; justify-content: center; background: #fff; color: rgb(196, 196, 196) }
.search-form { margin-top: 18px; }

.app-info { display: flex; flex-direction: column; gap: 5px; }
.pkg-name { font-family: monospace; font-size: 13px; color: #303133; font-weight: bold; word-break: break-all; }

.media-container { display: flex; gap: 15px; align-items: flex-start; padding: 10px 0; }
.img-icon { width: 60px; height: 60px; border-radius: 12px; flex-shrink: 0; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); }
.screenshot-strip { display: flex; gap: 10px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px; }
.img-screenshot { height: 180px; border-radius: 6px; flex-shrink: 0; border: 1px solid #ebeef5; cursor: pointer; transition: transform 0.2s; }
.img-screenshot:hover { transform: scale(1.05); }

</style>

