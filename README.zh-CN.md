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

## 💡 特性实践

### 1. Context 作为持久化记忆

与传统编程需要手动在函数间传递状态不同，zai 中的 `context` 充当智能体的**长期记忆**——在整个会话期间自动持久化并保持可访问。

```zai
agent PersonalAssistant

context Memory {
    user_name: ""
    conversation_history: []
    preferences: {
        timezone: "UTC"
        language: "zh"
    }
}

skill Chat() {
    ask "你叫什么名字？{{user_name=}}"

    // 记忆自动累积
    context.conversation_history = context.conversation_history + [{
        role: "user",
        content: "我的名字是 {{user_name}}"
    }]

    // AI 可以访问完整的对话历史
    process "基于历史记录向用户致以个性化问候" {
        extract: ["greeting"]
    }

    say context.greeting
}
```

### 2. 反应式 Persona：动态认知框架

`Persona` 不是静态提示词——它是一个**反应式认知框架**，会根据当前 Context 自适应调整。就像人类在不同情境下调整自己的行为一样。

```zai
agent CrisisManager

context Situation {
    severity: "normal"  // "normal" | "warning" | "critical"
    system_load: 45
}

persona AdaptiveResponse {
    // 基于上下文的不同认知模式
    if (context.severity == "critical") {
        system: "你处于紧急模式：
                 1. 回复必须极度简洁
                 2. 优先立即行动
                 3. 使用紧急、清晰的语言"
    }
    else if (context.severity == "warning") {
        system: "你处于警告模式：
                 1. 突出潜在风险
                 2. 提供简洁的建议"
    }
    else {
        system: "你处于正常模式：
                 1. 全面且详细地解释
                 2. 探索多种选项"
    }
}

skill HandleAlert(alert_message) {
    context.current_alert = alert_message

    // AI 自动接收适当的 persona
    process "分析警报并确定严重程度" {
        extract: ["severity", "recommended_action"]
    }

    // 更新上下文 - persona 会反应式地自适应
    context.severity = context.severity

    say "警报已处理。模式：{{severity}}"
    say "行动建议：{{recommended_action}}"
}
```

### 3. Agent System Prompt：核心身份

使用 `<<< >>>` 语法定义智能体的**基础身份**。此基础身份保持稳定，而 Persona 提供情境化适应。

```zai
agent CustomerServiceBot
<<<
你是一位专业的客户服务代表。
核心价值观：同理心、效率、诚信
当前班次：{{shift_hours}}
>>>

context WorkContext {
    shift_hours: "9:00-17:00"
    customer_tier: "premium"
}

persona ToneAdapter {
    if (context.customer_tier == "premium") {
        system: "使用正式、尊重的语言。优先处理他们的请求。"
    }
    else {
        system: "保持友好、平易近人的态度。"
    }
}

skill HandleComplaint(issue) {
    context.current_issue = issue

    // System prompt 组成：
    // 1. Agent system prompt（基础身份）
    // 2. 活动的 persona 覆盖层（情境调整）

    process "起草对客户投诉的回复" {
        extract: ["response_text"]
    }

    say context.response_text
}
```

### 4. 认知循环：完整的智能周期

zai 实现了受人类认知科学启发的完整**感知-认知-行动-学习**循环：

```zai
agent LearningResearcher

context ResearchContext {
    topic: ""
    findings: []
    confidence_score: 0
}

persona ResearchMode {
    system: "你是一位严谨的研究员。始终引用来源并表达置信度。"
}

skill Research(topic) {
    // 1. 感知：收集信息
    context.topic = topic
    say "开始研究主题：{{topic}}"

    // 2. 认知：AI 分析并提取结构化数据
    process "深入研究此主题" {
        extract: ["key_findings", "sources", "confidence_score"]
    }

    // 3. 整合：用研究结果更新记忆
    context.findings = context.findings + [{
        topic: context.topic,
        findings: context.key_findings,
        sources: context.sources,
        confidence: context.confidence_score
    }]

    // 4. 决策：基于 AI 输出的条件逻辑
    if (context.confidence_score < 0.5) {
        say "置信度较低。需要更多研究..."
        // 5. 行动：递归学习
        invoke Research(topic + " - 补充细节")
    }
    else {
        // 6. 学习：持久化到长期记忆
        context.confidence_score = context.confidence_score
        say "研究完成。置信度：{{confidence_score}}"
    }
}
```

### 5. 多智能体协作

使用 `notify` 和 `wait` 原语构建分布式智能，实现智能体间通信。

```zai
// 文件：coordinator.zai
agent TaskCoordinator

context CoordinationContext {
    task_id: ""
    results: []
}

skill DelegateTask(task_description) {
    context.task_id = "TASK-" + timestamp()

    // 通知 WorkerAgent 处理任务
    notify "WorkerAgent" "new_task" task_description

    say "任务 {{task_id}} 已委派给 WorkerAgent"

    // 等待完成信号
    [code, message] = wait "WorkerAgent"

    if (code == "success") {
        context.results = context.results + [message]
        say "任务成功完成：{{message}}"
    }
    else {
        say "任务失败：{{message}}"
    }
}
```

```zai
// 文件：worker.zai
agent WorkerAgent

context WorkerContext {
    current_task: ""
    processing_time: 0
}

skill ProcessTask() {
    // 等待来自协调器的任务
    [task_type, task_data] = wait "TaskCoordinator"

    context.current_task = task_data
    say "正在处理：{{task_data}}"

    // 执行任务
    exec "analyze_data.sh {{task_data}}" {
        filter: ["result", "duration"]
    }

    // 通知协调器完成
    notify "TaskCoordinator" "success" context.result
}
```

### 6. 外部工具集成

使用 `exec` 原语无缝集成外部系统，并自动过滤输出。

```zai
agent DevOpsAgent

context DeploymentContext {
    version: ""
    deployment_status: "pending"
    metrics: {}
}

skill Deploy(version) {
    context.version = version
    say "正在部署版本 {{version}}..."

    // 执行部署命令
    exec "deploy.sh {{version}}" {
        filter: ["status", "duration", "error_count"]
    }

    context.deployment_status = context.status

    // 查询监控指标
    exec "get_metrics.sh {{version}}" {
        filter: ["cpu", "memory", "latency"]
    }

    context.metrics = {
        cpu: context.cpu,
        memory: context.memory,
        latency: context.latency
    }

    // AI 分析部署健康状况
    process "分析部署指标并确定是否需要回滚" {
        extract: ["health_status", "recommendation"]
    }

    if (context.health_status == "unhealthy") {
        say "⚠️ 部署不健康！建议：{{recommendation}}"
        exec "rollback.sh {{version}}"
    }
    else {
        say "✅ 部署成功！健康状况：{{health_status}}"
    }
}
```

### 7. 模块化大脑文件（.zaih）

使用可导入的头文件跨项目共享记忆和个性。

```zai
// 文件：brain.zaih（共享定义）
context SharedMemory {
    company_name: "Acme Corp"
    api_endpoint: "https://api.acme.com"
    user_session: {}
}

persona ProfessionalTone {
    system: "你代表 {{company_name}}。始终保持专业且乐于助人。"
}
```

```zai
// 文件：main.zai
agent ModularAgent
import "brain.zaih"

skill Main() {
    // 访问导入的上下文
    say "欢迎来到 {{company_name}}！"

    // 使用导入的 persona
    process ProfessionalTone.system {
        extract: ["response"]
    }

    say context.response
}
```

## 📖 了解更多

-   [规范 (SPECIFICATION.md)](SPECIFICATION.zh-CN.md)：深入形式化语法和语句语义。
-   [教程 (USAGE.md)](USAGE.zh-CN.md)：学习如何构建你的第一个智能体。
-   [技术指南 (DOCUMENTATION.md)](DOCUMENTATION.zh-CN.md)：探索底层架构和桥接系统。
-   [设计哲学 (PHILOSOPHY.md)](PHILOSOPHY.zh-CN.md)：理解语言背后的认知计算模型。

## 许可证

MIT
