# 闲鱼自动化运营插件 (xianyu)

Claude Code 插件 — 一句话上架闲鱼商品，全流程自动化。

## 功能

| 场景 | 说什么 | 插件做什么 |
|------|--------|-----------|
| 上架商品 | "帮我上架一个 Claude Code 教程" | 调研 → 文案 → 生图 → 发布 |
| 自动回复 | "生成自动回复" | 输出暗号→链接模板 + 设置指引 |
| 推广动态 | "写条推广动态" | 按模板生成动态文案 |

## 前置依赖

| 组件 | 安装 |
|------|------|
| Python ≥ 3.11 | https://python.org |
| goofish-cli | `pip install goofish-cli` |
| 闲鱼账号 | goofish.com 已登录 |

## 安装

```bash
# 1. 安装插件
claude plugins install xianyu

# 或本地安装
claude --plugin-dir /path/to/plugin-xianyu

# 2. 运行初始化
python scripts/setup.py
```

初始化检查：Python → goofish-cli → 登录闲鱼 → Skills → MCP 配置。缺什么自动装。

## 使用方式

### 上架商品

```
帮我上架一个「Claude Code 全自动发小红书」教程，价格 19.9
```

Claude Code 自动执行：

```
[1/7] 环境检查 ✅
[2/7] 市场调研 → 分析竞品价格和关键词
[3/7] 文案生成 → 标题 + 描述 + 暗号
[4/7] 封面渲染 → professional 主题 800x800
[5/7] 保存归档 → data/ 目录
[6/7] 确认发布 → 展示参数等你确认
[7/7] 发布 + 自动回复设置提醒
```

### 生成自动回复

```
帮我生成自动回复，暗号 xiaohongshu，夸克链接 https://pan.quark.cn/s/xxx
```

### 写推广动态

```
帮我写条推广动态，商品是 Claude Code 全家桶教程
```

## 目录结构

```
plugin-xianyu/
├── .claude-plugin/plugin.json  # 插件清单
├── .mcp.json                    # goofish-cli MCP 配置
├── skills/                      # 3 个工作流 Skill
│   ├── xianyu-publish/          # 商品发布
│   ├── xianyu-reply/            # 自动回复
│   └── xianyu-feed/             # 推广动态
├── scripts/                     # 工具脚本
│   ├── setup.py                 # 一键初始化
│   └── check.py                 # 快速诊断
├── templates/                   # 可复用模板
│   ├── description.md           # 商品描述模板
│   ├── auto-reply.md            # 自动回复模板
│   └── feed-text.md             # 动态文案模板
└── README.md
```

## 商品数据归档

每个商品保存在 `data/YYYY-MM-DD-HHMM-product-slug/`：

```
data/2026-05-25-1130-claude-code-xhs/
├── title.txt             # 商品标题
├── description.md         # 商品描述（含暗号）
├── keywords.txt           # 搜索关键词
├── feed_text.md           # 推广动态
├── 自动回复模板.md         # 暗号→回复（卖家用）
├── images/cover.png       # 封面
└── delivery/              # 给客户的交付文件
```

## License

MIT
