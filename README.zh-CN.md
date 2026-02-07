# zai

[English](README.md) | [中文](README.zh-CN.md)

**zai** 是一种面向上下文的编程语言，专为 AI 编排而设计。它允许开发者定义 AI 驱动的工作流，将状态（**Context**）、AI 个性（**Persona**）和外部交互（**Skill**）作为语言的一等公民。

## 🧠 编程哲学：面向上下文编程

当前的 AI 开发常常陷入"胶水代码地狱"——手动在提示词、API 和逻辑之间传递状态。**zai** 颠覆了这个模型：

1.  **上下文即真相**：数据不只是传递给 AI，AI 生活在数据*内部*。`Context` 的任何变化都会立即被 AI 的推理引擎感知。
2.  **反应式身份**：不同于静态提示词，`Persona` 块是反应式的。它们会根据不断演化的 `Context` 自动改变行为。
3.  **人机共生**：我们不将 AI 视为黑盒 API。在 zai 中，AI 是一等控制流原语，能够通过 `process` 命令直接更新程序状态。

## 🏗️ 架构：三位一体模型

zai 管理三个主要实体之间的交互：

-   **人类**：通过 `ask` 和 `say` 提供指令和接收反馈的终端用户。
-   **AI（推理引擎）**：处理当前 `Context` 和 `Persona` 以做出决策或提取数据。
-   **智能体（编排逻辑）**：zai 代码本身，控制流程、处理 `Skill` 执行，并通过 `exec` 集成外部系统。

## ✨ 主要特性

-   **上下文优先的状态管理**：代码变量和 AI 提示词之间的自动同步。
-   **模块化 AI 大脑**：使用 `.zaih` 大脑文件跨项目共享记忆（`Context`）和个性（`Persona`）。
-   **基于技能的架构**：从小型、可重用、可测试的 `Skill` 单元构建复杂智能。
-   **可扩展运行时**：通过自定义桥接器（`AIBridge`, `ExecBridge`）支持本地 LLM、云 API 或自定义系统工具。

## 🚀 快速开始

### 安装

需要 Python 3.12+ 和 `uv`。

```bash
git clone https://github.com/your-repo/zai.git
cd zai
uv run zai examples/full_demo.zai
```

### 基础语法

```zai
agent HelloZai

context User {
    name: "Guest"
}

skill Main() {
    ask "你叫什么名字？{{name=}}"
    say "你好，{{name}}！"
}
```

## 📖 了解更多

-   [规范 (SPECIFICATION.md)](SPECIFICATION.zh-CN.md)：深入形式化语法和语句语义。
-   [教程 (USAGE.md)](USAGE.zh-CN.md)：学习如何构建你的第一个智能体。
-   [技术指南 (DOCUMENTATION.md)](DOCUMENTATION.zh-CN.md)：探索底层架构和桥接系统。
-   [设计哲学 (PHILOSOPHY.md)](PHILOSOPHY.zh-CN.md)：理解语言背后的认知计算模型。

## 许可证

MIT
