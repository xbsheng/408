import { defineConfig } from 'vitepress'
import {
  cSidebar,
  dataStructureSidebar,
  computerOrganizationSidebar,
  operatingSystemSidebar,
  computerNetworkSidebar,
} from './sidebars'

// GitHub Pages 项目站形如 https://<user>.github.io/<repo>/，base 必须是 /<repo>/。
// CI 里传入仓库名自动适配；本地开发默认 /408/。
const base = process.env.DOCS_BASE || '/408/'

const C_VIDEO = 'https://www.bilibili.com/video/BV1Bh4y1q7Nt/'
const CO_VIDEO = 'https://www.bilibili.com/video/BV1vt421L7oc/'

export default defineConfig({
  title: '408 考研笔记',
  description: 'C 语言 / 数据结构 / 计算机组成原理 / 操作系统 / 计算机网络 考研笔记',
  lang: 'zh-CN',
  base,
  cleanUrls: true,
  srcExclude: ['README.md'],

  themeConfig: {
    siteTitle: '408 考研笔记',

    nav: [
      { text: '首页', link: '/' },
      {
        text: 'C 语言',
        items: [
          { text: '课件目录', link: '/c/' },
          { text: '考研真题精选', link: '/c/exam-questions' },
          { text: '视频分 P 目录', link: '/c/videos' },
          { text: 'B 站视频', link: C_VIDEO },
        ],
      },
      { text: '数据结构', link: '/data-structure/' },
      {
        text: '计算机组成原理',
        items: [
          { text: '章节总览', link: '/computer-organization/' },
          { text: '视频分 P 目录', link: '/computer-organization/videos' },
          { text: 'B 站视频', link: CO_VIDEO },
        ],
      },
      { text: '操作系统', link: '/operating-system/' },
      { text: '计算机网络', link: '/computer-network/' },
    ],

    sidebar: {
      '/c/': cSidebar,
      '/data-structure/': dataStructureSidebar,
      '/computer-organization/': computerOrganizationSidebar,
      '/operating-system/': operatingSystemSidebar,
      '/computer-network/': computerNetworkSidebar,
    },

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索笔记', buttonAriaLabel: '搜索笔记' },
          modal: {
            noResultsText: '没有找到相关结果',
            resetButtonTitle: '清除查询',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },

    outline: { label: '本页目录', level: [2, 3] },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',

    footer: {
      message: '本站仅供学习交流',
      copyright: 'Copyright © 408 考研笔记',
    },
  },

  markdown: {
    lineNumbers: true,
    image: { lazyLoading: true },
    // 课件是在 Typora 里写的：单换行就是换行。默认 CommonMark 会把软换行变成空格，
    // 导致选项、答案挤成一行，和原文件不一样。
    breaks: true,
    // 组成原理笔记里有大量公式（$$...$$ / $...$），VitePress 内置 MathJax 支持
    math: true,
  },
})
