# AgentLang Grammar Specification v1.0

## 1. Overview
AgentLang is a context-oriented DSL designed for AI orchestration. It focuses on the mapping between State (Context), Prompt Logic (Conversion), and Execution (Task).

## 2. EBNF Grammar

```ebnf
job          ::= "job" identifier context_def conversion_def task_def+
context_def  ::= "context" identifier "{" (identifier ":" expression)* "}"
conversion_def ::= "conversion" identifier "{" (identifier ":" expression)* "}"
task_def     ::= "task" identifier "(" [params] ")" "{" (statement)* "}"

params       ::= identifier ("," identifier)*
statement    ::= var_decl | assignment | if_stmt | response_stmt | process_stmt | ask_stmt | exec_stmt | notify_stmt | wait_stmt | task_call | return_stmt

var_decl     ::= "var" identifier "=" expression
assignment   ::= (identifier | "context." identifier) "=" expression
if_stmt      ::= "if" condition "{" (statement)* "}" [ "else" "{" (statement)* "}" ]

process_stmt ::= "process" expression [ "{" "extract" ":" "[" (string ("," string)*) "]" "}" ]
ask_stmt     ::= "ask" string
exec_stmt    ::= "exec" expression [ "{" "filter" ":" "[" (string ("," string)*) "]" "}" ]

notify_stmt  ::= "notify" identifier expression expression
wait_stmt    ::= "[" identifier "," identifier "]" "=" "wait" identifier

task_call    ::= "call" identifier "(" [args] ")"
args         ::= assignment ("," assignment)*
return_stmt  ::= ("success" | "fail") expression expression
response_stmt::= ("reply" | "say") expression

expression   ::= string | number | identifier | binary_op | template_render
template_render ::= identifier "{" (assignment ("," assignment)*) "}"
condition    ::= expression ( "==" | "!=" | ">" | "<" ) expression
```

## 3. Detailed Statement Descriptions

### 3.1 `job`
The entry point of an `.al` file. Defines the namespace and unique identity of the agent.

### 3.2 `context`
Defines the **Managed State**. All variables within this block are persistent and accessible via the `context.` prefix. AI updates via `process` target these fields.

### 3.3 `conversion`
Defines the **Translation Layer**. It converts the current state (Context) into AI instructions. Multiple templates can exist here, and they are rendered automatically during `process` calls.

### 3.4 `task`
The **Minimal Schedulable Unit**.
- **Parameters**: Must correspond to keys in the `context`.
- **Logic**: Traditional imperative flow mixed with AI primitives.

### 3.5 `process`
The **AI Reasoning Bridge**.
- **Input**: User prompt or template.
- **Extract**: JSON-schema style extraction that updates the `context` automatically.

### 3.6 `ask`
The **Human Input Primitive**.
- Format: `ask "Message {var_name=}"`.
- Automatically waits for user input and updates `context.var_name`.

### 3.7 `exec`
The **External System Interface**.
- **Synchronous/Blocking**.
- Supports `HTTPS`, `Shell`, and `FS` engines.
- **Filter**: Maps engine output (JSON/Text) into `context` fields.

### 3.8 `notify` & `wait`
The **Coordination Layer**.
- `notify`: Non-blocking signal sent to another `job`.
- `wait`: Blocking wait for a signal from another `job`, destructuring the result into `[code, message]`.

### 3.9 `success` / `fail`
Standardized task return types. Every task must terminate with one of these to provide predictable results to the orchestrator.
