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
              <el-button type="primary" @click="submit">查询</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </el-main>
    <el-footer class="footer">
      <p>Copyright © 2026 - present IvoryGate. All Rights Reserved.</p>
    </el-footer>
  </el-container>
</template>

<script setup>
import { Monitor } from '@element-plus/icons-vue';
import { ref, reactive } from 'vue'

// ---- 状态变量 -----
const viewMode = ref('task_board')

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
  console.log(`change platform to ${form.platform}`)
}

// 
const handleRegionChange = (value) => {
  form.region = value
  console.log(`current region is ${form.region}`)
}

// 提交请求
const submit = () => {
  console.log("提交")
}

</script>

<style>
.main-layout { background: #f0f2f5; min-height: 100vh; }
.header { background: #fff; border-bottom: 1px solid #dcdfe6; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.brand { display: flex; align-items: center; gap: 10px; color: #409eff; font-weight: bold; font-size: 1.2rem; }
.logo.el-icon { height: 32px; width: 32px; padding-right: px; }
.footer { display: flex; justify-content: center; background: #fff; color: rgb(196, 196, 196) }
.search-form { margin-top: 18px; }
</style>

