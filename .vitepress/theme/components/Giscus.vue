<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()
const container = ref<HTMLElement>()

// 用页面 pathname 作为 discussion 的标识（含 /408/ 前缀，与站点一致）
function term() {
  return window.location.pathname.replace(/\.html$/, '')
}

function render() {
  if (!container.value) return
  container.value.innerHTML = ''

  const script = document.createElement('script')
  script.src = 'https://giscus.app/client.js'
  script.async = true
  script.crossOrigin = 'anonymous'
  script.setAttribute('data-repo', 'xbsheng/408')
  script.setAttribute('data-repo-id', 'R_kgDOV7nbTg')
  script.setAttribute('data-category', 'Announcements')
  script.setAttribute('data-category-id', 'DIC_kwDOV7nbTs4DL85F')
  script.setAttribute('data-mapping', 'specific')
  script.setAttribute('data-term', term())
  script.setAttribute('data-strict', '1')
  script.setAttribute('data-reactions-enabled', '1')
  script.setAttribute('data-emit-metadata', '0')
  script.setAttribute('data-input-position', 'top')
  script.setAttribute('data-theme', 'preferred_color_scheme')
  script.setAttribute('data-lang', 'zh-CN')
  script.setAttribute('data-loading', 'lazy')
  container.value.appendChild(script)
}

onMounted(render)
watch(() => route.path, render)
</script>

<template>
  <div class="giscus-wrapper">
    <div ref="container" class="giscus" />
  </div>
</template>
