# zai Language Specification
Version: 1.4

## Overview
**zai** is a context-oriented language designed for AI orchestration. This document defines the formal grammar and statement semantics.

### Extensions
- `.zai`: zai Source File (contains `agent` and `skill` logic)
- `.zaih`: zai Header File (contains `context` and `persona` definitions)

## 2. EBNF Grammar

```ebnf
agent               ::= "agent" identifier [agent_system_prompt] import_stmt* (context_def | persona_def)* skill_def+
agent_system_prompt ::= "---" multiline_string "---"
import_stmt  ::= "import" string

config_file  ::= (context_def | persona_def)*

context_def  ::= "context" identifier "{" (identifier ":" expression)* "}"
persona_def  ::= "persona" identifier "{" persona_item* "}"
persona_item ::= identifier (":" expression | persona_block)
persona_block ::= "{" persona_fragment* "}"
persona_fragment ::= expression | persona_if
persona_if   ::= "if" condition persona_block ["else" persona_block]

skill_def    ::= "skill" identifier "(" [params] ")" "{" (statement)* "}"

params       ::= identifier ("," identifier)*
statement    ::= var_decl | assignment | if_stmt | while_stmt | response_stmt | process_stmt | ask_stmt | exec_stmt | notify_stmt | wait_stmt | skill_invoke | return_stmt

var_decl     ::= "var" identifier "=" expression
assignment   ::= (identifier | context_var) "=" expression
context_var  ::= "context." identifier

if_stmt      ::= "if" condition "{" (statement)* "}" [ "else" "{" (statement)* "}" ]
while_stmt   ::= "while" condition "{" (statement)* "}"

process_stmt ::= "process" expression [ "{" "extract" ":" "[" (string ("," string)*) "]" "}" ]
ask_stmt     ::= "ask" string
exec_stmt    ::= "exec" expression [ "{" "filter" ":" "[" (string ("," string)*) "]" "}" ]

notify_stmt  ::= "notify" identifier expression expression
wait_stmt    ::= "[" identifier "," identifier "]" "=" "wait" identifier

skill_invoke ::= "invoke" identifier "(" [args] ")"
args         ::= assignment ("," assignment)*
return_stmt  ::= ("success" | "fail") expression expression
response_stmt::= ("reply" | "say") expression

expression   ::= binary_op | simple_expression | template_render | context_var | persona_ref
simple_expression ::= string | number | boolean | identifier | "(" expression ")"
boolean      ::= "true" | "false"
persona_ref  ::= identifier "." identifier
template_render ::= identifier "{" [args] "}"
binary_op    ::= expression OPERATOR expression
OPERATOR     ::= "+" | "-" | "*" | "/" | "==" | "!=" | ">" | "<" | ">=" | "<=" | "&&" | "||"
condition    ::= expression
```

## 3. Detailed Statement Descriptions

### 3.1 `agent`
The entry point of a `.zai` file. Defines the namespace and unique identity of the agent.

**Agent System Prompt**: An optional base system prompt can be specified after the agent name, enclosed in `--- """ ... """ ---`. This defines the agent's fundamental identity and behavior, which is always included in AI interactions.

```zai
agent CustomerServiceBot
--- """
You are a professional customer service representative.
Always be polite, helpful, and concise.
""" ---

context { ... }
persona { ... }
```

The system prompt composition order during `process`:
1. Agent-level system prompt (base identity)
2. Active persona overlays (contextual adjustments)

### 3.2 `import` (Modularization)
Allows importing `context` and `persona` definitions from external files.
- **Syntax**: `import "filename.zaih"`
- **Scope**: Definitions from the imported file are merged into the current `agent` scope.
- **Convention**: Use `.zaih` for files intended for import (e.g., `brain.zaih`).

### 3.3 `context`
Defines the **Managed State**. All variables within this block are persistent and accessible via the `context.` prefix. AI updates via `process` target these fields.
> **Note**: An agent can define only **one** `context` block (even across imports). Multiple `context` definitions will cause a runtime error.

### 3.4 `var` & `assignment`
- **`var`**: Declares a local variable within a skill.
- **`assignment`**: Updates a local variable or a `context` field.
- **Syntax**: `var x = 10` or `context.x = 20`.

### 3.5 `persona`
Defines the **Translation Layer**. It converts the current state (Context) into AI instructions. Multiple templates can exist here, and they are rendered automatically during `process` calls.

### 3.6 `skill`
The **Minimal Schedulable Unit**.
- **Parameters**: Input values passed during `invoke`.
- **Logic**: Traditional imperative flow (if, while, variables) mixed with AI primitives.

### 3.7 `process`
The **AI Reasoning Bridge**.
- **Input**: User prompt or template.
- **Extract**: JSON-schema style extraction that updates the `context` automatically.
- **Customization**: Behavior can be overridden via third-party `AIBridge` implementations.

### 3.8 `if` & `while`
- **`if`**: Conditional execution.
- **`while`**: Looping execution.
- Both use standard boolean conditions (`==`, `!=`, `&&`, `||`, etc.).

### 3.9 `ask`
The **Human Input Primitive**.
- Format: `ask "Message {var_name=}"`.
- Automatically waits for user input and updates `context.var_name`.

### 3.10 `template_render`
The **String Interpolation Engine**. Allows dynamic variable replacement within strings.
- **Syntax**: `TemplateName { KEY = "VALUE" }`
- **Context Access**: Automatically resolves `{key}` from the local scope or `context`.

### 3.11 `exec`
The **External System Interface**.
- **Synchronous/Blocking**.
- **Engine**: Behavior can be overridden via third-party `ExecBridge` implementations.
- **Filter**: Maps engine output into `context` fields.

### 3.12 `notify` & `wait`
The **Coordination Layer**.
- `notify`: Non-blocking signal sent to another `agent`.
- `wait`: Blocking wait for a signal from another `agent`, destructuring the result into `[code, message]`.

### 3.13 `success` / `fail`
Standardized skill return types. Every skill must terminate with one of these to provide predictable results to the orchestrator.
- **Syntax**: `success code "message"` or `fail code "message"`.

### 3.14 `invoke`
The **Skill Execution Command**. Triggers a nested skill.
- **Syntax**: `invoke SkillName(arg1=val1, ...)`

## 4. Runtime Bridges
The `zai` runtime allows deep customization through bridges:
- `AIBridge`: Handles the interaction with LLMs.
- `ExecBridge`: Handles external command execution.
Custom implementations can be injected into the `Interpreter` to support different backends or local tool execution.
