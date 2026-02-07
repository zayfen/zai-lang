# zai 入门指南 🚀

[English](USAGE.md) | [中文](USAGE.zh-CN.md)

欢迎来到 **zai**，一种专为帮助您轻松构建 AI 智能体而设计的编程语言。如果您曾经想使用 AI 自动化复杂任务，但发现现有工具过于复杂，那么您来对地方了！

本指南将带您从 "Hello World" 到构建您的第一个模块化 AI 智能体。

---

## 1. 安装

`zai` 使用 `uv`，一个快速的 Python 包管理器。

1.  **安装 uv**（如果您还没有）：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **克隆项目**：
    ```bash
    git clone https://github.com/your-repo/zai-lang.git
    cd zai-lang
    ```
3.  **运行您的第一个文件**：
    ```bash
    uv run zai examples/full_demo.zai
    ```

---

## 2. 您的第一行代码："问候智能体"

创建一个名为 `hello.zai` 的文件并粘贴以下内容：

```zai
agent GreetingAgent

context UserProfile {
    name: "陌生人"
}

skill Main() {
    ask "你叫什么名字？{{name=}}"
    say "欢迎来到未来，{{name}}！"
    success 0 "已问候用户"
}
```

### 这里发生了什么？
- **`agent`**：每个项目都以 `agent` 开头。它是您的智能助手的名称。
- **`context`**：这是智能体的"记忆"。我们在这里保存用户的名字。
- **`skill`**：这是逻辑发生的地方。`Main()` 是智能体执行的第一个技能。
- **`{{name=}}`**：`ask` 中的这个特殊标签告诉 `zai` 将用户输入的内容保存到 context 的 `name` 字段。

---

## 3. 增强能力：与 AI 对话

`zai` 的真正强大之处在于 `process` 命令。它将您的上下文发送给 AI 并自动更新。

```zai
agent SmartAgent

context Brain {
    input: "我觉得饿了",
    mood: "未知"
}

persona Personality {
    base_instruction {
        "你是一位有帮助的心理学家。"
    }
}

skill Main() {
    process "分析用户的情绪" { extract: ["mood"] }
    say "我感觉到你今天{{mood}}。"
    success 0 "已分析情绪"
}
```

### 工作原理：
1. `process` 接收您的指令（"分析用户的情绪"）。
2. 它查看 **`persona`**（我们的 Personality）以了解如何表现。
3. 它"提取"结果并直接放入 `context.mood`。无需手动解析！

---

## 4. 保持整洁：模块化项目

随着智能体变得更智能，您的文件会变得更长。`zai` 允许您将 context 和 personality 移动到单独的"头文件"（以 `.zaih` 结尾）中。

**文件：`brain.zaih`**
```zai
context MyData {
    user_name: "管理员"
}

persona MyPrompts {
    base_instruction {
        "你是一位技术专家。"
    }
}
```

**文件：`main.zai`**
```zai
agent ModularAgent
import "brain.zaih"

skill Main() {
    say "你好，{{user_name}}！"
    // ... 逻辑 ...
}
```

---

## 5. 专业技巧：反应式人格

有时您希望 AI 根据不同情况表现不同。`zai` 通过在 **`persona`** 中使用 `if` 块让这变得非常容易：

```zai
persona SmartPersonality {
    base_instruction {
        "你是一位有帮助的助手。"
        if context.is_urgent {
            "!!! 重要：用户很着急。请极其简洁 !!!"
        }
    }
}
```

如果 `context.is_urgent` 为真，`zai` 会自动将该额外警告添加到 AI 的指令中。您无需编写复杂代码来更改提示词！

---

## 6. Agent 基础系统提示词

定义智能体的基础身份，使用 `<<< >>>` 语法：

```zai
agent CustomerServiceBot
<<<
你是一位专业的客户服务代表。
核心价值观：同理心、效率、诚信
当前客户：{{customer_name}}
>>>

context CustomerContext {
    customer_name: "访客"
}

skill HandleInquiry() {
    ask "请问您叫什么名字？{{customer_name=}}"
    process "有什么可以帮您的？" { extract: ["response"] }
}
```

系统提示词组合顺序：
1. **Agent 级系统提示词**（基础身份，使用 `{{variable}}` 模板）
2. **活跃的 persona 覆盖层**（情境调整）

---

## 命令摘要表

| 命令 | 作用 | 示例 |
| :--- | :--- | :--- |
| `say` | 打印消息 | `say "你好！"` |
| `ask` | 获取用户输入 | `ask "年龄？{{age=}}"` |
| `process` | 请求 AI 做某事 | `process "总结" { extract: ["summary"] }` |
| `exec` | 运行系统命令 | `exec "ls -la" { filter: ["files"] }` |
| `import` | 加载另一个文件 | `import "config.zaih"` |
| `invoke` | 执行技能 | `invoke MySkill()` |
| `notify` | 向另一个智能体发送消息 | `notify "AgentName" "类型" "内容"` |
| `wait` | 等待来自另一个智能体的消息 | `[code, msg] = wait AgentName` |

准备好构建了吗？查看 `examples/` 文件夹获取更多复杂的智能体示例！
