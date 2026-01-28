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
  </el-container>
</template>

<script setup>
import { Monitor } from '@element-plus/icons-vue';
import { ref, reactive } from 'vue'

// ---- 状态变量 -----
const viewMode = ref('task_board')

</script>

<style>
.main-layout { background: #f0f2f5; min-height: 100vh; }
.header { background: #fff; border-bottom: 1px solid #dcdfe6; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.brand { display: flex; align-items: center; gap: 10px; color: #409eff; font-weight: bold; font-size: 1.2rem; }
.logo.el-icon { height: 32px; width: 32px; padding-right: px; }
</style>