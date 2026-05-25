---
name: xianyu-reply
description: >-
  Use when user needs to set up auto-reply for a 闲鱼 product or reply to buyers.
  Trigger phrases: "生成自动回复", "设置自动回复", "自动发货", "auto reply",
  "暗号回复", "自动回复模板", "怎么回复买家".
  Generates keyword→reply mappings and delivery instructions.
allowed-tools: Read, Write, Edit, Bash, mcp__goofish__message_list_chats, mcp__goofish__message_history, mcp__goofish__message_send
---

# 闲鱼自动回复生成

## 你的职责

帮用户为每个已发布/待发布的商品生成自动回复配置：暗号→网盘链接的映射关系，并输出可直接粘贴到闲鱼 App 自动回复设置的内容。

## 工作步骤

### Step 1：确认商品信息

向用户确认：
- 商品名称（用于模板中说明）
- 暗号（触发关键词，如 `xiaohongshu`, `quanjiatong`）
- 网盘链接 + 提取码
- 网盘类型（夸克/百度/阿里云盘）

### Step 2：生成回复模板

按 `templates/auto-reply.md` 格式输出：

```
感谢购买！以下是{商品简称}下载链接：

📥 {网盘名称}：{链接}
🔑 提取码：{提取码}

{文件内容一句话说明}

有任何问题随时私信我，看到会回复~
```

### Step 3：输出设置指引

输出以下操作步骤给用户：

1. 打开闲鱼 App → 我 → ⚙️ 设置 → **自动回复**
2. 点击「添加关键词回复」
3. 关键词填：`{暗号}`
4. 回复内容粘贴上面的模板
5. 保存

### Step 4：存档

将自动回复配置保存到 `{商品目录}/自动回复模板.md`（不在 delivery/ 内——这是卖家工具，不给客户）。

## 多商品管理

如果用户有多个商品，汇总输出一个对照表：

| 暗号 | 商品 | 链接状态 |
|------|------|---------|
| xiaohongshu | Claude Code 发小红书 | ✅ 已配置 |
| quanjiatong | 全家桶环境搭建 | ✅ 已配置 |
| {新暗号} | {新商品} | ⚠️ 待上传网盘 |

## 买家咨询回复

当买家通过闲鱼聊天咨询时，使用 goofish-cli 的 message 工具：

1. `mcp__goofish__message_list_chats` — 获取会话列表
2. `mcp__goofish__message_history` — 查看具体消息
3. `mcp__goofish__message_send` — 发送回复

> 如果商品描述中已写明暗号，大多数买家会直接发暗号触发自动回复，无需手动回复。
