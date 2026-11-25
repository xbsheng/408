import type { DefaultTheme } from 'vitepress'

const C_VIDEO = 'https://www.bilibili.com/video/BV1Bh4y1q7Nt/'
const CO_VIDEO = 'https://www.bilibili.com/video/BV1vt421L7oc/'

export const cSidebar: DefaultTheme.SidebarItem[] = [
  {
    text: 'C 语言课件',
    items: [
      { text: '第01章 · C 语言入门', link: '/c/chapter-01-introduction' },
      { text: '第02章 · 变量与进制', link: '/c/chapter-02-variables-and-number-systems' },
      { text: '第03章 · 运算符与流程控制', link: '/c/chapter-03-operators-and-control-flow' },
      { text: '第04章 · 数组（重点）', link: '/c/chapter-04-arrays' },
      { text: '第05章 · 指针（重点）', link: '/c/chapter-05-pointers' },
      { text: '第06章 · 函数', link: '/c/chapter-06-functions' },
      { text: '第07章 · 结构体与共用体', link: '/c/chapter-07-structures-and-unions' },
      { text: '第08章 · C 语言常用函数', link: '/c/chapter-08-library-functions' },
      { text: '第09章 · 文件操作', link: '/c/chapter-09-file-operations' },
    ],
  },
  {
    text: '附录',
    items: [
      { text: 'MinGW 编译器的安装和配置', link: '/c/appendix-mingw-setup' },
      { text: 'C 开发利器：CLion 的使用', link: '/c/appendix-clion' },
    ],
  },
  {
    text: '相关链接',
    items: [
      { text: '考研真题精选', link: '/c/exam-questions' },
      { text: '视频分 P 目录', link: '/c/videos' },
      { text: 'B 站视频', link: C_VIDEO },
    ],
  },
]

export const computerOrganizationSidebar: DefaultTheme.SidebarItem[] = [
  {
    text: '计算机组成原理课件',
    items: [
      { text: '第一章 · 计算机系统概述', link: '/computer-organization/chapter-01-overview' },
      {
        text: '第二章 · 数据的表示和运算',
        link: '/computer-organization/chapter-02-data-representation-and-arithmetic',
      },
      { text: '第三章 · 存储器', link: '/computer-organization/chapter-03-memory' },
      { text: '第四章 · 指令系统', link: '/computer-organization/chapter-04-instruction-set' },
      { text: '第五章 · 中央处理器', link: '/computer-organization/chapter-05-cpu' },
      { text: '第六章 · 总线和输入输出系统', link: '/computer-organization/chapter-06-bus-and-io' },
    ],
  },
  {
    text: '相关链接',
    items: [
      { text: '章节总览', link: '/computer-organization/' },
      { text: '视频分 P 目录', link: '/computer-organization/videos' },
      { text: 'B 站视频', link: CO_VIDEO },
    ],
  },
]

function subjectSidebar(name: string, dir: string): DefaultTheme.SidebarItem[] {
  return [
    {
      text: name,
      items: [{ text: '章节总览', link: `/${dir}/` }],
    },
  ]
}

export const dataStructureSidebar = subjectSidebar('数据结构', 'data-structure')
export const operatingSystemSidebar = subjectSidebar('操作系统', 'operating-system')
export const computerNetworkSidebar = subjectSidebar('计算机网络', 'computer-network')
