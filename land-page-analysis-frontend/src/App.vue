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
      </el-radio-group>
    </el-header>

    <el-main>
      <el-card class="search-card" shadow="never">
        <el-form class="search-form" :inline="true" :model="form" label-width="80px">
          <div class="form-row">
            <el-form-item label="包名">
              <el-autocomplete
                v-model="form.package"
                :fetch-suggestions="querySearchHistory"
                placeholder="com.example.app"
                style="width: 280px"
                clearable
                @select="handleHistorySelect"
                @input="autoChoosePlatform"
              />
            </el-form-item>
            <el-form-item label="平台">
              <el-select v-model="form.platform" style="width: 140px">
                <el-option label="Google Play" value="google_play" />
                <el-option label="App Store" value="apple_store" />
              </el-select>
            </el-form-item>
            <el-form-item v-if="viewMode === 'task_board'" label="地区">
              <el-select v-model="form.region" filterable style="width: 140px" @change="handleRegionChange">
                <el-option v-for="(item, key) in regionMap" :key="key" :label="item.label" :value="key" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleMainSearch" :loading="submitting">
                {{ viewMode === 'task_board' ? '立即查询' : '同步全地区' }}
              </el-button>
            </el-form-item>
          </div>

          <div class="form-row filter-row">
            <el-form-item label="筛选包名">
              <el-input v-model="filterCriteria.package" placeholder="过滤当前列表..." style="width: 250px" clearable />
            </el-form-item>
            <el-form-item label="筛选地区">
              <el-select
                v-model="filterCriteria.region"
                multiple filterable collapse-tags collapse-tags-tooltip :max-collapse-tags="4"
                placeholder="全部地区" style="width: 380px" clearable class="filter-region-select"
              >
                <el-option v-for="(item, key) in regionMap" :key="key" :label="item.label" :value="key" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-text type="info">匹配: {{ currentDisplayData.length }} 项</el-text>
            </el-form-item>
          </div>
        </el-form>
      </el-card>

      <el-table :data="currentDisplayData" v-loading="loading" border row-key="id" class="task-list">
        <el-table-column label="应用详情" width="240px">
          <template #default="scope">
            <div class="app-info">
              <span class="pkg-name">{{ scope.row.package_name }}</span>
              <div class="tags">
                <el-tag size="small" effect="dark">{{ scope.row.platform }}</el-tag>
                <el-tag size="small" type="info" style="margin-left: 5px">{{ scope.row.region.toUpperCase() }}</el-tag>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="素材预览">
          <template #default="scope">
            <div class="media-container" v-if="getCurrentImageData(scope.row.id)">
              <el-image 
                class="img-icon" 
                v-if="getCurrentImageData(scope.row.id).icon" 
                :src="getCurrentImageData(scope.row.id).icon" 
                fit="cover" 
                :preview-src-list="[getCurrentImageData(scope.row.id).icon]" 
                preview-teleported
                referrerpolicy="no-referrer"
                hide-on-click-modal
                show-progress
              />
              <div class="screenshot-strip">
                <el-image 
                  v-for="(url, index) in getCurrentImageData(scope.row.id).others" 
                  :key="index" 
                  :src="url" 
                  class="img-screenshot" 
                  fit="cover" 
                  lazy 
                  :preview-src-list="getCurrentImageData(scope.row.id).others" 
                  :initial-index="index" 
                  preview-teleported
                  referrerpolicy="no-referrer"
                  hide-on-click-modal
                  show-progress
                />
              </div>
            </div>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty :description="taskList.length || regionTaskList.length ? '没有匹配的筛选结果' : '暂无数据，请先执行查询'" />
        </template>
      </el-table>
    </el-main>
    <el-footer class="footer" height="60px"><p>Copyright © 2026 - present IvoryGate. All Rights Reserved.</p></el-footer>
  </el-container>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { Monitor } from '@element-plus/icons-vue';
import axios from 'axios';


const COUNTRY_LANG_MAP = {
  'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 'NZ': 'en',
  'JP': 'ja', 'KR': 'ko', 'FR': 'fr', 'DE': 'de', 'IT': 'it', 'ES': 'es', 'BR': 'pt', 'PT': 'pt',
  'RU': 'ru', 'IN': 'en', 'ID': 'id', 'TH': 'th', 'VN': 'vi', 'TR': 'tr', 'SA': 'ar', 'AE': 'ar',
  // ... 其他所有 A-Z 数据 ... 
  'AD': 'ca', 'AF': 'fa', 'AG': 'en', 'AI': 'en', 'AL': 'sq', 'AM': 'hy', 'AO': 'pt', 'AQ': 'und', 
  'AR': 'es', 'AS': 'sm', 'AT': 'de', 'AW': 'nl', 'AX': 'sv', 'AZ': 'az', 'BA': 'bs', 'BB': 'en', 
  'BD': 'bn', 'BE': 'nl', 'BF': 'fr', 'BG': 'bg', 'BH': 'ar', 'BI': 'rn', 'BJ': 'fr', 'BL': 'fr', 
  'BM': 'en', 'BN': 'ms', 'BO': 'es', 'BQ': 'nl', 'BS': 'en', 'BT': 'dz', 'BV': 'no', 'BW': 'en', 
  'BY': 'be', 'BZ': 'en', 'CC': 'en', 'CD': 'fr', 'CF': 'fr', 'CG': 'fr', 'CH': 'de', 'CI': 'fr', 
  'CK': 'en', 'CL': 'es', 'CM': 'fr', 'CO': 'es', 'CR': 'es', 'CU': 'es', 'CV': 'pt', 'CW': 'nl', 
  'CX': 'en', 'CY': 'el', 'CZ': 'cs', 'DJ': 'fr', 'DK': 'da', 'DM': 'en', 'DO': 'es', 'DZ': 'ar',
  'EC': 'es', 'EE': 'et', 'EG': 'ar', 'EH': 'ar', 'ER': 'ti', 'ET': 'am', 'FI': 'fi', 'FJ': 'en', 
  'FK': 'en', 'FM': 'en', 'FO': 'fo', 'GA': 'fr', 'GD': 'en', 'GE': 'ka', 'GF': 'fr', 'GG': 'en', 
  'GH': 'en', 'GI': 'en', 'GL': 'kl', 'GM': 'en', 'GN': 'fr', 'GP': 'fr', 'GQ': 'es', 'GR': 'el', 
  'GS': 'en', 'GT': 'es', 'GU': 'en', 'GW': 'pt', 'GY': 'en', 'HM': 'en', 'HN': 'es', 'HR': 'hr', 
  'HT': 'fr', 'HU': 'hu', 'IE': 'en', 'IL': 'he', 'IM': 'en', 'IO': 'en', 'IQ': 'ar', 'IR': 'fa', 
  'IS': 'is', 'JE': 'en', 'JM': 'en', 'JO': 'ar', 'KE': 'en', 'KG': 'ky', 'KH': 'km', 'KI': 'en', 
  'KM': 'ar', 'KN': 'en', 'KW': 'ar', 'KY': 'en', 'KZ': 'ru', 'LA': 'lo', 'LB': 'ar', 'LC': 'en', 
  'LI': 'de', 'LK': 'si', 'LR': 'en', 'LS': 'en', 'LT': 'lt', 'LU': 'fr', 'LV': 'lv', 'LY': 'ar',
  'MA': 'ar', 'MC': 'fr', 'MD': 'ro', 'ME': 'sr', 'MF': 'fr', 'MG': 'mg', 'MH': 'en', 'MK': 'mk', 
  'ML': 'fr', 'MM': 'my', 'MN': 'mn', 'MO': 'zh', 'MP': 'en', 'MQ': 'fr', 'MR': 'ar', 'MS': 'en', 
  'MT': 'mt', 'MU': 'en', 'MV': 'dv', 'MW': 'en', 'MX': 'es', 'MY': 'en', 'MZ': 'pt', 'NA': 'en', 
  'NC': 'fr', 'NE': 'fr', 'NF': 'en', 'NG': 'en', 'NI': 'es', 'NL': 'nl', 'NO': 'no', 'NP': 'ne', 
  'NR': 'en', 'NU': 'en', 'OM': 'ar', 'PA': 'es', 'PE': 'es', 'PF': 'fr', 'PG': 'en', 'PH': 'en', 
  'PK': 'en', 'PL': 'pl', 'PM': 'fr', 'PN': 'en', 'PR': 'es', 'PS': 'ar', 'PW': 'en', 'PY': 'es',
  'QA': 'ar', 'RE': 'fr', 'RO': 'ro', 'RS': 'sr', 'RW': 'rw', 'SB': 'en', 'SC': 'fr', 'SD': 'ar', 
  'SE': 'sv', 'SG': 'en', 'SH': 'en', 'SI': 'sl', 'SJ': 'no', 'SK': 'sk', 'SL': 'en', 'SM': 'it', 
  'SN': 'fr', 'SO': 'so', 'SR': 'nl', 'SS': 'en', 'ST': 'pt', 'SV': 'es', 'SX': 'nl', 'SY': 'ar', 
  'SZ': 'en', 'TC': 'en', 'TD': 'fr', 'TF': 'fr', 'TG': 'fr', 'TJ': 'tg', 'TK': 'en', 'TL': 'pt', 
  'TM': 'tk', 'TN': 'ar', 'TO': 'to', 'TT': 'en', 'TV': 'en', 'TZ': 'sw', 'UA': 'uk', 'UG': 'en', 
  'UM': 'en', 'UY': 'es', 'UZ': 'uz', 'VA': 'it', 'VC': 'en', 'VE': 'es', 'VG': 'en', 'VI': 'en', 
  'VU': 'fr', 'WF': 'fr', 'WS': 'sm', 'YE': 'ar', 'YT': 'fr', 'ZA': 'en', 'ZM': 'en', 'ZW': 'en'
};

const regionMap = Object.fromEntries(
  Object.entries(COUNTRY_LANG_MAP).map(([code, lang]) => [
    code.toLowerCase(), { label: code, lang: lang }
  ])
);

const viewMode = ref('task_board');
const submitting = ref(false);
const loading = ref(false);
const form = reactive({ package: '', platform: 'google_play', region: 'us', lang: 'en' });
const filterCriteria = reactive({ package: '', region: [] });
const taskList = ref([]);
const imageData = reactive({});
const regionTaskList = ref([]);
const regionImageData = reactive({});
const searchHistory = ref([]);

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/history');
    searchHistory.value = data.map(v => ({ value: v }));
  } catch (e) { console.error("History load error", e); }
});

const querySearchHistory = (queryString, cb) => {
  const results = queryString 
    ? searchHistory.value.filter(h => h.value.toLowerCase().includes(queryString.toLowerCase()))
    : searchHistory.value;
  cb(results);
};

const handleHistorySelect = (item) => {
  form.package = item.value;
  autoChoosePlatform(item.value);
};

const updateHistory = async (pkg) => {
  if (!pkg) return;
  try {
    const { data } = await axios.post('/api/history', { package: pkg });
    searchHistory.value = data.map(v => ({ value: v }));
  } catch (e) { console.warn("Update history failed"); }
};

const handleMainSearch = async () => {
  if (!form.package) return;
  updateHistory(form.package);
  viewMode.value === 'task_board' ? fetchSingleRecord() : fetchAllRegion();
};

const currentDisplayData = computed(() => {
  const source = viewMode.value === 'task_board' ? taskList.value : regionTaskList.value;
  return source.filter(item => {
    const matchPkg = (item.package_name || '').toLowerCase().includes(filterCriteria.package.toLowerCase());
    const matchReg = filterCriteria.region.length === 0 || filterCriteria.region.includes(item.region.toLowerCase());
    return matchPkg && matchReg;
  });
});
const getCurrentImageData = (id) => viewMode.value === 'task_board' ? imageData[id] : regionImageData[id];
const autoChoosePlatform = (v) => form.platform = /^\d/.test(v) ? "apple_store" : "google_play";
const handleRegionChange = (v) => form.lang = regionMap[v]?.lang || 'en';

const fetchSingleRecord = async () => {
  submitting.value = true; loading.value = true;
  try {
    const { data } = await axios.post('/api/get', { ...form });
    imageData[data.task_id] = { icon: data.images.find(i => i.type === 'icon')?.url, others: data.images.filter(i => i.type === 'other').map(i => i.url) };
    const entry = { id: data.task_id, package_name: form.package, platform: form.platform, region: form.region, status: data.status };
    const idx = taskList.value.findIndex(t => t.id === data.task_id);
    if (idx !== -1) taskList.value[idx] = entry; else taskList.value.unshift(entry);
  } finally { submitting.value = false; loading.value = false; }
};

const fetchAllRegion = async () => {
  submitting.value = true; loading.value = true; regionTaskList.value = [];
  try {
    const res = await fetch('/api/compare', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ package: form.package, platform: form.platform }) });
    const reader = res.body.getReader(); const decoder = new TextDecoder(); let buf = '';
    while (true) {
      const { value, done } = await reader.read(); if (done) break;
      loading.value = false; buf += decoder.decode(value, { stream: true });
      let lines = buf.split('\n'); buf = lines.pop();
      for (const line of lines) {
        if (!line.trim()) continue;
        const data = JSON.parse(line);
        regionImageData[data.task_id] = { icon: data.images.find(i => i.type === 'icon')?.url, others: data.images.filter(i => i.type === 'other').map(i => i.url) };
        regionTaskList.value.push({ id: data.task_id, package_name: form.package, platform: form.platform, region: (data.region || '').toLowerCase(), status: data.status });
      }
    }
  } finally { submitting.value = false; loading.value = false; }
};
</script>

<style>
.main-layout { background: #f0f2f5; min-height: 100vh; }
.header { background: #fff; border-bottom: 1px solid #dcdfe6; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.brand { display: flex; align-items: center; gap: 10px; color: #409eff; font-weight: bold; font-size: 1.2rem; }
.footer { display: flex; justify-content: center; align-items: center; background: #fff; color: #c4c4c4; margin-top: 20px; }

.search-card { margin-bottom: 20px; }
.form-row { display: flex; flex-wrap: wrap; align-items: center; }
.filter-row { margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ebeef5; }
.el-form-item { margin-bottom: 0 !important; margin-right: 20px !important; }

.filter-region-select .el-select__tags { max-width: none !important; }
.filter-region-select .el-select-tags-wrapper { display: flex; flex-wrap: nowrap !important; }
.filter-region-select .el-tag { margin-right: 4px !important; }
.app-info { display: flex; flex-direction: column; gap: 5px; }
.pkg-name { font-family: monospace; font-size: 13px; color: #303133; font-weight: bold; word-break: break-all; }
.media-container { display: flex; gap: 15px; align-items: flex-start; padding: 10px 0; }
.img-icon { width: 60px; height: 60px; border-radius: 12px; flex-shrink: 0; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); }
.screenshot-strip { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 5px; }
.img-screenshot { height: 180px; border-radius: 6px; flex-shrink: 0; border: 1px solid #ebeef5; }
</style>