# 408 考研笔记

408 笔记站：C 语言、数据结构、计算机组成原理、操作系统、计算机网络。


## 添加新章节

1. 在对应科目目录下新建 `xxx.md`，文件名用英文，例如 `data-structure/chapter-01-introduction.md`
2. 在 `.vitepress/sidebars.ts` 对应侧边栏里加一条 `{ text: '01 · 绪论', link: '/data-structure/chapter-01-introduction' }`

文件名一律用英文：中文路径在 URL 里会变成 `%E8%AF%BE...` 这种百分号编码，链接容易出错。
图片同理，统一放在各科目的 `images/` 目录，文件名用 `img-001.png` 这类形式。

`base` 默认 `/408/`（本地开发）；CI 里通过环境变量 `DOCS_BASE=/<仓库名>/` 覆盖，仓库改名无需改配置。

## 统计（Vercel Analytics / Speed Insights）

`.vitepress/theme/index.ts` 的 `enhanceApp` 里动态注入 `@vercel/analytics` 和
`@vercel/speed-insights` 的 `inject()` / `injectSpeedInsights()`。

- 用无框架版 `inject()`，不用 `@vercel/analytics/vue`：vue 版依赖 `vue-router`，
  而 VitePress 没把它暴露成可直接引用的依赖，打包会报 `"useRoute" is not exported`。
- 只在 Vercel 部署上真正上报；本地和其他平台（含 GitHub Pages）会自动跳过。
  想看数据就得在 Vercel 上也挂一份，那边记得配 `DOCS_BASE=/`。

## 评论（giscus）

评论区基于 [giscus](https://giscus.app/zh-CN)，数据存在本仓库的 GitHub Discussions 里。

- 配置在 `.vitepress/theme/components/Giscus.vue`：`repo` / `repo-id` / `category` / `category-id`。
  `repo-id` 和 `category-id` 变了要同步改（用 <https://giscus.app/zh-CN> 页面或 GraphQL 查）。
- 某个页面不想开评论，frontmatter 里写 `comments: false`。
- 首次启用需要在仓库上装一次 [giscus App](https://github.com/apps/giscus)（只装一次，之后不用管），
  否则评论区会提示无权限。

## 部署

推送到 `main` 自动触发 `.github/workflows/deploy.yml` → 构建 → 发布到 GitHub Pages。

- 仓库 Settings → Pages → Source 必须是 **GitHub Actions**（`base` 由工作流里的
  `DOCS_BASE=/<仓库名>/` 注入，仓库改名不用改配置）。
- 工作流权限：`pages: write` + `id-token: write`，`actions/configure-pages` 要求 Pages 已经启用，
  所以新的仓库第一次运行时如果报 `Get Pages site failed`，先在 Settings → Pages 里启用一次再重跑。

### 部署到域名根目录（Vercel / 自定义域名）

`base` 只由环境变量决定，默认 `/408/`：

```bash
npm run build                  # base 为 /408/，对应 https://<user>.github.io/408/
DOCS_BASE=/ npm run build      # base 为 /，对应 https://your-domain.com/
```

Vercel 之类的平台在项目的环境变量里加 `DOCS_BASE=/`（或直接写进 Build Command：
`DOCS_BASE=/ npm run build`），Build Command 用 `npm run build`、Output Directory 用 `.vitepress/dist`。

## 内容说明

- C 语言课件整理自尚硅谷宋红康《C 语言精讲版》（[B 站视频](https://www.bilibili.com/video/BV1Bh4y1q7Nt/)）。
- 相对原课件做了两处适配：
  - 少量正文里的双大括号（如 `int a[][3]＝{ {1,2,3} }` 的真题选项）改成 HTML 实体，避免被 Vue 当成插值语法导致构建失败；
  - 原始 HTML 的 `<img src="images/...">` 改成 Markdown 图片语法，图片才会被 VitePress 正常打包。
- 计算机组成原理课件来自单文件 `计算机组成原理.md`，用 `scripts/import-computer-organization.py`
  按章节拆成 6 个文件。源文件更新后重跑即可：

  ```bash
  python3 scripts/import-computer-organization.py /path/to/计算机组成原理.md computer-organization
  ```

  脚本会顺带处理原文件的 Typora 特色写法（`pictures\x.png`、`<img>`、pandoc 的 `T~1~` / `2^10^`、缺 `</table>`、`{{`），
  并把图片改名为 `img-001.png` 之类拷到 `computer-organization/images/`。
- 站点开了 MathJax（`markdown.math: true`），公式用 `$$...$$` / `$...$` 写。
- 开了 `markdown.breaks: true`：课件是在 Typora 里写的，单换行就是换行；默认 CommonMark
  会把软换行当空格，选项和答案会挤成一行，跟原文件对不上。
- 正文里的制表符换成了 `&emsp;`：Typora 用 tab 做缩进和列对齐，HTML 会把 tab 压成一个空格，
  真题的 A/B/C/D 选项就会糊成一行。
- 视频分 P 汇总页（`c/videos.md`、`computer-organization/videos.md`）由脚本从 B 站
  pagelist 接口实时生成，不用手抄：

  ```bash
  python3 scripts/gen-videos.py
  ```

  章节与分 P 的对应区间写在脚本顶部的 `SUBJECTS` 里，视频更新后改区间重跑。
- 数据结构、操作系统、计算机网络目前只有章节大纲占位，逐章补充即可。
