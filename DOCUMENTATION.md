# AgentLang Technical Documentation

## 1. Introduction
AgentLang is a next-generation context-oriented programming language designed to replace fragmented technologies like MCP and standalone skills. It provides a native, unified framework for building complex AI agents where state, logic, and reasoning are deeply integrated.

## 2. Core Architecture: The Tri-Partite Model

AgentLang manages the interaction between three primary entities:

1.  **Human**: The end-user providing instructions and receiving feedback via `ask` and `say`.
2.  **AI (LLM)**: The reasoning engine that processes context and extracts structured data via `process`.
3.  **The Task (Code)**: The orchestration logic written in AgentLang that governs the flow and integrates **External Systems** via `exec`.

### Context-Oriented Design
In AgentLang, **Context is King**.
- **Context (State)**: What the agent knows.
- **Conversion (Voice)**: How the agent talks to the AI.
- **Task (Behavior)**: What the agent does.

## 3. Language Features

### Dynamic Templating
Strings assigned to variables act as templates. They support deep nesting and dynamic resolution.
```agentlang
var Welcome = "Hi {USER}!"
var Page = "{HEADER} Content goes here."
var out = Page { HEADER = Welcome { USER = "Riven" } }
```

### Context-Aware AI Interaction
The `process` command is the "brain" of the language. It doesn't just call an LLM; it synchronizes the entire Context state with the AI, allowing for precise data extraction and state transitions.

### Synchronous External Integration
Unlike MCP's async overhead, AgentLang's `exec` primitive is synchronous and blocking. It treats external systems (API/Shell) as reliable extensions of the state machine.

### Distributed Coordination
Multiple AgentLang `jobs` can work together. Using `notify` and `wait`, you can build a swarm of specialized agents that collaborate on complex tasks with standardized communication protocol `[code, message]`.

## 4. Lifecycle of an AgentLang Job

1.  **Boot**: The interpreter loads the `.al` file.
2.  **Init**: The `context` is instantiated.
3.  **Invoke**: A `task` is called (usually the entry task).
4.  **Execute**: The task runs, interacting with AI, Humans, and External Systems.
5.  **Standardized Terminate**: The task returns `success` or `fail`, and the job state is persisted or passed to the next job via `notify`.

---

## 5. Vision: Replacing MCP and Skills
AgentLang eliminates the "glue code" problem. By treating context as a first-class language construct, it removes the need for complex RPC protocols (MCP) and disjointed tool definitions (Skills). An AgentLang file is a self-documenting, executable blueprint for an AI's behavior.
