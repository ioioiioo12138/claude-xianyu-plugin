---
name: xianyu-publish
description: >-
  Use when user wants to publish a product on 闲鱼 (Xianyu/idlefish).
  Trigger phrases: "上架商品", "发布到闲鱼", "帮我发布", "publish to xianyu",
  "list this on goofish", "上新", "帮我上架". Covers end-to-end:
  market research → copywriting → cover image → upload → publish.
  Based on goofish-cli MCP and xhs-note-creator rendering.
argument-hint: <product-topic> [price] [keyword]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__goofish__search_items, mcp__goofish__item_publish, mcp__goofish__media_upload, mcp__goofish__category_recommend, mcp__goofish__auth_status
---

# 闲鱼商品发布工作流

你是闲鱼商品发布的 orchestrator。按以下步骤执行，每步完成后向用户确认再进入下一步。

## Step 1：环境检查

调用 `mcp__goofish__auth_status` 确认 goofish-cli 已连接且已登录。

若未连接：检查 `.claude/mcp.json` 确认 goofish 配置。
若未登录：引导用户运行 `goofish auth login --qr` 扫码。

## Step 2：市场调研

调用 `mcp__goofish__search_items` 搜索用户给出的关键词，分析竞品：
- 价格区间
- 标题关键词模式
- 竞争饱和度
- 差异化机会

向用户报告调研结论，给出定价建议。

## Step 3：商品文案

生成以下内容，请用户审核：

**标题**（≤30 字）：包含核心关键词，用 1-3 个卖点吸引点击。

**描述**（Markdown 格式）：参考 `templates/description.md` 模板结构：
- 这是什么？（一句话定义）
- 覆盖内容（表格列出模块）
- 为什么需要（痛点列表）
- 适合谁（目标用户）
- 获取方式（暗号 + 自动秒发）
- 常见问题（Q&A 3-5 个）

> 文案风格参考 copywriting-pro skill（如已安装）。若无，遵循：短句短段、适度 Emoji、口语化。

**⚠️ 平台敏感词规避**：闲鱼会检测竞品 App 名称（如小红书、抖音、淘宝、拼多多等），标题和描述中必须使用替代词：
- 小红书 → 小红薯
- 抖音 → 抖声/短视频平台
- 淘宝 → 某宝
- 微信 → 薇信/绿泡泡
- 类似处理其他竞品名称

> delivery/ 交付文件不受此限制，因为客户收货后看，不在闲鱼公开展示。

**暗号**：每个商品一个独特英文关键词（如 xiaohongshu, quanjiatong），用于触发自动回复。

## Step 4：封面图生成

使用 xhs-note-creator skill 渲染封面：

1. 创建 `cover_render.md`，只含 YAML frontmatter：
```yaml
---
emoji: "{匹配主题的 emoji}"
title: "{大标题，≤12字}"
subtitle: "{副标题，≤15字}"
---
```

2. 运行渲染：
```bash
cd <product-dir>
PYTHONIOENCODING=utf-8 python ~/.claude/skills/xhs-note-creator/scripts/render_xhs.py \
  cover_render.md -t professional -m auto-fit -o images --width 800 --height 800
```

3. 确认生成 `images/cover.png`。

备选主题：`sketch`（手绘）、`terminal`（极客）、`neo-brutalism`（醒目）、`botanical`（清新）。

## Step 5：保存内容

创建 `data/{YYYY-MM-DD-HHMM}-{product-slug}/` 目录结构：

```
data/YYYY-MM-DD-HHMM-product-slug/
├── title.txt             # 纯标题
├── description.md         # 商品描述（含暗号提示）
├── keywords.txt           # 搜索关键词
├── feed_text.md           # 推广动态文案
├── 自动回复模板.md         # 暗号→回复模板（卖家工具）
├── images/
│   └── cover.png          # 封面
└── delivery/              # 纯交付物（给客户的文件）
    ├── README.md           # 主教程
    └── ...
```

## Step 6：发布

向用户展示发布参数确认：

| 字段 | 值 |
|------|-----|
| 标题 | ... |
| 价格 | ¥... |
| 图片 | 列表 |
| 类目 | 电子资料 |
| 暗号 | ... |

确认后调用 `mcp__goofish__item_publish` 发布。

> 如 MCP 工具不可用，使用 CLI 直调：`goofish item publish "title" "desc" image1 image2 price`

## Step 7：收尾

1. 展示已发布商品链接
2. 将 `自动回复模板.md` 内容展示给用户，提醒去闲鱼 App 设置自动回复
3. 提醒用户上传 `delivery/` 到网盘并更新回复链接
4. 提醒用户在闲鱼 App 发推广动态（文案已保存在 `feed_text.md`）
