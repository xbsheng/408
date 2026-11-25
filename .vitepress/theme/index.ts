import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { inBrowser } from 'vitepress'
import Layout from './Layout.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp() {
    // Vercel Web Analytics / Speed Insights。
    // 用无框架的 inject()：vue 版本依赖 vue-router，VitePress 没把它暴露成直接依赖。
    // 两个脚本只在 Vercel 部署上真正上报，本地和其他平台会自己跳过。
    if (!inBrowser) return
    import('@vercel/analytics').then(({ inject }) => inject())
    import('@vercel/speed-insights').then(({ injectSpeedInsights }) => injectSpeedInsights())
  },
} satisfies Theme
