<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import Giscus from './components/Giscus.vue'

const { Layout } = DefaultTheme
const { frontmatter } = useData()
</script>

<template>
  <Layout>
    <template #doc-after>
      <!-- 首页、目录页（frontmatter 里写 comments: false）不挂评论区 -->
      <Giscus v-if="frontmatter.comments !== false" />
    </template>
  </Layout>
</template>
