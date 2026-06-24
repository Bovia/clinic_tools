---
title: 齿科设计助手
description: 为口腔诊所一键生成排班表、护理卡片、节日海报等宣传物料的在线工具
published: true
tags:
  - HTML
  - JavaScript
  - Tailwind CSS
  - html2canvas
demoUrl: https://clinictools.vercel.app
githubUrl: https://github.com/Bovia/clinic_tools
date: 2026-06
devices:
  - desktop
  - mobile
  - tablet
---

## 为什么做这个

诊所前台每周要手动排班、手工做节日推文，费时又不统一。需要一个不依赖任何后端、打开即用的工具，让没有设计背景的诊所员工也能快速出图。

## 它解决了什么

覆盖排班表、护理提醒卡、节日海报、通知公告四类物料，模板切换后表单自动联动，最终一键导出为适配微信的图片。所有资源内嵌，离线也能用。

## 一个值得说的技术决定

图片导出依赖 `html2canvas`，但字体渲染在不同系统上不一致。最终把关键字体和图标资源全部 base64 内嵌进 `assets-embed.js`，在 `init()` 阶段预注入，保证截图与预览像素级一致。

```js
async function loadEmbeddedAssets() {
  // 将 base64 字体注入 <style>，再注入背景图到 Image 缓存
  // 确保 html2canvas 截图时所有资源已就绪
}
```

## 结果

部署后诊所员工反馈"比之前用 PS 快多了"，排班表出图从 20 分钟缩短到 2 分钟。作为纯静态页面托管在 Vercel，零运维成本。