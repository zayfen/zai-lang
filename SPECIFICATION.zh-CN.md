# zai 语言规范
版本：1.4

[English](SPECIFICATION.md) | [中文](SPECIFICATION.zh-CN.md)

## 概述

**zai** 是一种面向上下文的语言，专为 AI 编排而设计。本文档定义了形式化语法和语句语义。

### 文件扩展名
- `.zai`：zai 源文件（包含 `agent` 和 `skill` 逻辑）
- `.zaih`：zai 头文件（包含 `context` 和 `persona` 定义）

## 2. EBNF 语法

```ebnf
agent               ::= "agent" identifier [agent_system_prompt] import_stmt* (context_def | persona_def)* skill_def+
agent_system_prompt ::= "<<<" agent_sys_content ">>>"
agent_sys_content   ::= /[^>]+/s
import_stmt         ::= "import" string

config_file         ::= (context_def | persona_def)*

context_def         ::= "context" identifier "{" (identifier ":" expression)* "}"
persona_def         ::= "persona" identifier "{" persona_item* "}"
persona_item        ::= identifier (":" expression | persona_block)
persona_block       ::= "{" persona_fragment* "}"
persona_fragment    ::= expression | persona_if
persona_if          ::= "if" condition persona_block ["else" persona_block]

skill_def           ::= "skill" identifier "(" [params] ")" "{" statement* "}"

params              ::= identifier ("," identifier)*
statement           ::= var_decl
                      | assignment
                      | if_stmt
                      | while_stmt
                      | response_stmt
                      | process_stmt
                      | ask_stmt
                      | exec_stmt
                      | notify_stmt
                      | wait_stmt
                      | skill_invoke
                      | return_stmt

var_decl            ::= "var" identifier "=" expression
assignment          ::= target "=" expression
target              ::= identifier | context_var
context_var         ::= "context." identifier

if_stmt             ::= "if" condition "{" statement* "}" ["else" "{" statement* "}"]
while_stmt          ::= "while" condition "{" statement* "}"

process_stmt        ::= "process" expression ["{" "extract" ":" "[" string ("," string)* "]" "}"]
ask_stmt            ::= "ask" string
exec_stmt           ::= "exec" expression ["{" "filter" ":" "[" string ("," string)* "]" "}"]

notify_stmt         ::= "notify" identifier expression expression
wait_stmt           ::= "[" identifier "," identifier "]" "=" "wait" identifier

skill_invoke        ::= "invoke" identifier "(" [args] ")"
args                ::= assignment ("," assignment)*
return_stmt         ::= ("success" | "fail") expression expression
response_stmt       ::= ("reply" | "say") expression

expression          ::= binary_op | simple_expression | template_render | context_var | persona_ref
simple_expression   ::= string | number | boolean | identifier | "(" expression ")"
boolean             ::= "true" | "false"
persona_ref         ::= identifier "." identifier
template_render     ::= identifier "{" [args] "}"
binary_op           ::= expression OPERATOR expression
OPERATOR            ::= "+" | "-" | "*" | "/" | "==" | "!=" | ">" | "<" | ">=" | "<=" | "&&" | "||"
condition           ::= expression
```

## 3. 详细语句说明

### 3.1 `agent`
`.zai` 文件的入口点。定义智能体的命名空间和唯一身份。

**Agent 系统提示词**：可以在智能体名称后指定一个可选的基础系统提示词，使用 `<<< ... >>>` 包裹。这定义了智能体的基础身份和行为，始终包含在 AI 交互中。内容支持使用 `{{variable}}` 或 `{{context.variable}}` 语法进行模板渲染。

```zai
agent CustomerServiceBot
<<<
你是一位专业的客户服务代表。
当前客户：{{customer_name}}
请始终保持礼貌和乐于助人。
>>>

context { ... }
persona { ... }
```

`process` 期间的系统提示词组合顺序：
1. Agent 级系统提示词（基础身份，模板在运行时解析）
2. 活跃的 persona 覆盖层（情境调整）

### 3.2 `import`（模块化）
允许从外部文件导入 `context` 和 `persona` 定义。
- **语法**：`import "filename.zaih"`
- **作用域**：导入文件的定义合并到当前 `agent` 作用域。
- **约定**：使用 `.zaih` 作为意图导入的文件（例如 `brain.zaih`）。

### 3.3 `context`
定义**托管状态**。此块中的所有变量都是持久化的，可通过 `context.` 前缀访问。AI 通过 `process` 的更新目标这些字段。
> **注意**：智能体只能定义**一个** `context` 块（即使在导入文件中）。多个 `context` 定义会导致运行时错误。

### 3.4 `var` & `assignment`
- **`var`**：在技能内声明局部变量。
- **赋值**：更新局部变量或 `context` 字段。
- **语法**：`var x = 10` 或 `context.x = 20`。

### 3.5 `persona`
定义**转换层**。它将当前状态（Context）转换为 AI 指令。这里可以存在多个模板，它们在 `process` 调用期间自动渲染。

### 3.6 `skill`
**最小可调度单元**。
- **参数**：执行 `invoke` 时传递的输入值。
- **逻辑**：混合传统命令式流程（if、while、变量）与 AI 原语。

### 3.7 `process`
**AI 推理桥**。
- **输入**：用户提示词或模板。
- **提取**：JSON 模式风格的提取，自动更新 `context`。
- **定制**：行为可通过第三方 `AIBridge` 实现覆盖。

### 3.8 `if` & `while`
- **`if`**：条件执行。
- **`while`**：循环执行。
- 两者使用标准布尔条件（`==`、`!=`、`\u0026\u0026`、`||` 等）。

## 4. 模板系统

zai 使用 `{{variable}}` 语法进行模板渲染。支持的上下文：
- `say`、`ask` 语句中的字符串插值
- `process`、`exec` 命令中的参数
- Agent 系统提示词中的动态内容

示例：
```zai
context User { name: "Alice" }
skill Main() {
    say "你好，{{name}}！"  // 渲染：你好，Alice！
}
```
