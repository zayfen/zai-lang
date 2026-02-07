# zai Technical Guide
Version: 1.2

[English](DOCUMENTATION.md) | [中文](DOCUMENTATION.zh-CN.md)

## Introduction
**zai** is a programming language built specifically for modern AI workflows. It prioritizes state management (Context) and AI personality (Persona) as first-class citizens.
It is designed to provide a native, unified framework for building complex AI agents where state, logic, and reasoning are deeply integrated.

## 2. Core Architecture: The Tri-Partite Model

zai manages the interaction between three primary entities:

1.  **Human**: The end-user providing instructions and receiving feedback via `ask` and `say`.
2.  **AI (LLM)**: The reasoning engine that processes context and extracts structured data via `process`.
3.  **The Skill (Code)**: The orchestration logic written in zai that governs the flow and integrates **External Systems** via `exec`.

### Context-Oriented Design
In zai, **Context is King**.
- **Context (State)**: What the agent knows.
- **Persona (Voice)**: How the agent talks to the AI.
- **Skill (Behavior)**: What the agent does.
- **Agent System Prompt**: Base identity of the agent, defined with `<<< ... >>>` syntax.

### Agent System Prompt
An optional base system prompt can be defined at the agent level using the `<<< ... >>>` syntax. This establishes the agent's fundamental identity and is always included in AI interactions.

```zai
agent CustomerServiceBot
<<<
You are a professional customer service representative.
Current customer: {{customer_name}}
Always be polite and helpful.
>>>

context CustomerContext {
    customer_name: "Guest"
}

skill HandleInquiry() {
    ask "What's your name? {{customer_name=}}"
    process "How can I help?" { extract: ["response"] }
}
```

The system prompt composition order during `process`:
1. **Agent-level system prompt** (base identity, with `{{variable}}` templates resolved at runtime)
2. **Active persona overlays** (contextual adjustments)

## 3. Language Features

### Dynamic Templating
Strings support template rendering using `{{variable}}` syntax. Context variables and local variables are automatically interpolated.
```zai
var Welcome = "Hi {{user_name}}!"
var Page = "{{header}} Content goes here."
context.user_name = "Riven"
context.header = Welcome
say Page  // Output: Hi Riven! Content goes here.
```

### Context-Aware AI Interaction
The `process` command is the "brain" of the language. It doesn't just call an LLM; it synchronizes the entire Context state with the AI, allowing for precise data extraction and state transitions.

### Synchronous External Integration
zai's `exec` primitive is synchronous and blocking. It treats external systems (API/Shell) as reliable extensions of the state machine.

### Distributed Coordination
Multiple zai `agents` can work together. Using `notify` and `wait`, you can build a swarm of specialized agents that collaborate on complex tasks with standardized communication protocol `[code, message]`.

## 4. Lifecycle of a zai Agent

1.  **Boot**: The interpreter loads the `.zai` file.
2.  **Init**: The `context` is instantiated.
3.  **Invoke**: A `skill` is invoked (usually the entry skill).
4.  **Execute**: The skill runs, interacting with AI, Humans, and External Systems.
5.  **Standardized Terminate**: The skill returns `success` or `fail`, and the agent state is persisted or passed to the next agent via `notify`.

---

## 5. Vision
zai eliminates the "glue code" problem. By treating context as a first-class language construct, it removes the need for complex protocols and disjointed tool definitions. A zai file is a self-documenting, executable blueprint for an AI's behavior.
