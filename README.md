# zai

[English](README.md) | [中文](README.zh-CN.md)

**zai** is a context-oriented programming language designed for seamless AI orchestration. It allows developers to define AI-driven workflows where state (**Context**), AI personality (**Persona**), and external interaction (**Skill**) are treated as first-class language constructs.

## 🧠 Philosophy: Context-Oriented Programming

Current AI development often suffers from "glue code death"—manually passing state between prompts, APIs, and logic. **zai** flips this model:

1.  **Context is the Source of Truth**: Data isn't just passed to the AI; the AI lives *inside* the data. Any change in the `Context` is instantly available to the AI's reasoning engine.
2.  **Reactive Identity**: Instead of static prompts, `Persona` blocks are reactive. They change their behavior automatically based on the evolving `Context`.
3.  **Human-AI Symbiosis**: We don't view AI as a black box API. In zai, AI is a first-class control flow primitive, capable of updating the program state directly through the `process` command.

## 🏗️ Architecture: The Tri-Partite Model

zai manages the interaction between three primary entities:

-   **The Human**: Provides high-level intent and feedback via `ask` and `say`.
-   **The AI (Reasoning Engine)**: Processes the current `Context` and `Persona` to make decisions or extract data.
-   **The Agent (Orchestration Logic)**: The zai code itself, which governs the flow, handles `Skill` execution, and manages external systems via `exec`.

## ✨ Key Features

-   **Context-First State Management**: Automatic synchronization between code variables and AI prompts.
-   **Modular AI Brains**: Share memory (`Context`) and personality (`Persona`) across projects using `.zaih` brain files.
-   **Skill-Based Architecture**: Build complex intelligence from small, reusable, and testable `Skill` units.
-   **Extensible Runtimes**: Customizable bridges (`AIBridge`, `ExecBridge`) for local LLMs, cloud APIs, or custom system tools.

## 🚀 Quick Start

### Installation

Requires Python 3.12+ and `uv`.

```bash
git clone https://github.com/your-repo/zai.git
cd zai
uv run zai examples/full_demo.zai
```

### Basic Syntax

```zai
agent HelloZai

context User {
    name: "Guest"
}

skill Main() {
    ask "What is your name? {{name=}}"
    say "Hello, {{name}}!"
}
```

## 💡 Features in Action

### 1. Context as Persistent Memory

Unlike traditional programming where state must be manually passed between functions, `context` in zai acts as the Agent's **long-term memory**—automatically persisted and accessible throughout the session.

```zai
agent PersonalAssistant

context Memory {
    user_name: ""
    conversation_history: []
    preferences: {
        timezone: "UTC"
        language: "en"
    }
}

skill Chat() {
    ask "What's your name? {{user_name=}}"

    // Memory accumulates automatically
    context.conversation_history = context.conversation_history + [{
        role: "user",
        content: "My name is {{user_name}}"
    }]

    // AI can access complete conversation history
    process "Greet the user personally based on history" {
        extract: ["greeting"]
    }

    say context.greeting
}
```

### 2. Reactive Persona: Dynamic Cognitive Framework

`Persona` is not a static prompt—it's a **reactive cognitive framework** that adapts based on the current Context. Like humans adjust their behavior in different situations.

```zai
agent CrisisManager

context Situation {
    severity: "normal"  // "normal" | "warning" | "critical"
    system_load: 45
}

persona AdaptiveResponse {
    // Different cognitive modes based on context
    if (context.severity == "critical") {
        system: "You are in EMERGENCY MODE:
                 1. Respond with extreme brevity
                 2. Prioritize immediate action
                 3. Use urgent, clear language"
    }
    else if (context.severity == "warning") {
        system: "You are in CAUTION MODE:
                 1. Highlight potential risks
                 2. Provide concise recommendations"
    }
    else {
        system: "You are in NORMAL MODE:
                 1. Be thorough and explanatory
                 2. Explore multiple options"
    }
}

skill HandleAlert(alert_message) {
    context.current_alert = alert_message

    // AI automatically receives the appropriate persona
    process "Analyze alert and determine severity" {
        extract: ["severity", "recommended_action"]
    }

    // Update context - persona will adapt reactively
    context.severity = context.severity

    say "Alert processed. Mode: {{severity}}"
    say "Action: {{recommended_action}}"
}
```

### 3. Agent System Prompt: Core Identity

Define the Agent's **fundamental identity** using the `<<< >>>` syntax. This base identity remains stable while Personas provide situational adaptation.

```zai
agent CustomerServiceBot
<<<
You are a professional customer service representative.
Core values: Empathy, Efficiency, Integrity
Current shift: {{shift_hours}}
>>>

context WorkContext {
    shift_hours: "9AM-5PM"
    customer_tier: "premium"
}

persona ToneAdapter {
    if (context.customer_tier == "premium") {
        system: "Use formal, respectful language. Prioritize their requests."
    }
    else {
        system: "Be friendly and approachable."
    }
}

skill HandleComplaint(issue) {
    context.current_issue = issue

    // System prompt composition:
    // 1. Agent system prompt (base identity)
    // 2. Active persona overlay (situational adjustment)

    process "Draft a response to the customer complaint" {
        extract: ["response_text"]
    }

    say context.response_text
}
```

### 4. The Cognitive Loop: Complete Intelligence Cycle

zai implements the full **perception-cognition-action-learning** loop inspired by human cognitive science:

```zai
agent LearningResearcher

context ResearchContext {
    topic: ""
    findings: []
    confidence_score: 0
}

persona ResearchMode {
    system: "You are a meticulous researcher. Always cite sources and express confidence levels."
}

skill Research(topic) {
    // 1. PERCEPTION: Gather information
    context.topic = topic
    say "Starting research on: {{topic}}"

    // 2. COGNITION: AI analyzes and extracts structured data
    process "Research this topic thoroughly" {
        extract: ["key_findings", "sources", "confidence_score"]
    }

    // 3. INTEGRATION: Update memory with findings
    context.findings = context.findings + [{
        topic: context.topic,
        findings: context.key_findings,
        sources: context.sources,
        confidence: context.confidence_score
    }]

    // 4. DECISION: Conditional logic based on AI output
    if (context.confidence_score < 0.5) {
        say "Confidence is low. Need more research..."
        // 5. ACTION: Recursive learning
        invoke Research(topic + " - additional details")
    }
    else {
        // 6. LEARNING: Persist to long-term memory
        context.confidence_score = context.confidence_score
        say "Research complete. Confidence: {{confidence_score}}"
    }
}
```

### 5. Multi-Agent Collaboration

Build distributed intelligence with `notify` and `wait` primitives for agent-to-agent communication.

```zai
// File: coordinator.zai
agent TaskCoordinator

context CoordinationContext {
    task_id: ""
    results: []
}

skill DelegateTask(task_description) {
    context.task_id = "TASK-" + timestamp()

    // Notify WorkerAgent to process the task
    notify "WorkerAgent" "new_task" task_description

    say "Task {{task_id}} delegated to WorkerAgent"

    // Wait for completion signal
    [code, message] = wait "WorkerAgent"

    if (code == "success") {
        context.results = context.results + [message]
        say "Task completed successfully: {{message}}"
    }
    else {
        say "Task failed: {{message}}"
    }
}
```

```zai
// File: worker.zai
agent WorkerAgent

context WorkerContext {
    current_task: ""
    processing_time: 0
}

skill ProcessTask() {
    // Wait for task from coordinator
    [task_type, task_data] = wait "TaskCoordinator"

    context.current_task = task_data
    say "Processing: {{task_data}}"

    // Execute the task
    exec "analyze_data.sh {{task_data}}" {
        filter: ["result", "duration"]
    }

    // Notify coordinator of completion
    notify "TaskCoordinator" "success" context.result
}
```

### 6. External Tool Integration

Seamlessly integrate external systems using the `exec` primitive with automatic output filtering.

```zai
agent DevOpsAgent

context DeploymentContext {
    version: ""
    deployment_status: "pending"
    metrics: {}
}

skill Deploy(version) {
    context.version = version
    say "Deploying version {{version}}..."

    // Execute deployment command
    exec "deploy.sh {{version}}" {
        filter: ["status", "duration", "error_count"]
    }

    context.deployment_status = context.status

    // Query monitoring metrics
    exec "get_metrics.sh {{version}}" {
        filter: ["cpu", "memory", "latency"]
    }

    context.metrics = {
        cpu: context.cpu,
        memory: context.memory,
        latency: context.latency
    }

    // AI analyzes deployment health
    process "Analyze deployment metrics and determine if rollback is needed" {
        extract: ["health_status", "recommendation"]
    }

    if (context.health_status == "unhealthy") {
        say "⚠️ Deployment unhealthy! Recommendation: {{recommendation}}"
        exec "rollback.sh {{version}}"
    }
    else {
        say "✅ Deployment successful! Health: {{health_status}}"
    }
}
```

### 7. Modular Brain Files (.zaih)

Share memory and personality across projects using importable header files.

```zai
// File: brain.zaih (shared definitions)
context SharedMemory {
    company_name: "Acme Corp"
    api_endpoint: "https://api.acme.com"
    user_session: {}
}

persona ProfessionalTone {
    system: "You represent {{company_name}}. Always be professional and helpful."
}
```

```zai
// File: main.zai
agent ModularAgent
import "brain.zaih"

skill Main() {
    // Access imported context
    say "Welcome to {{company_name}}!"

    // Use imported persona
    process ProfessionalTone.system {
        extract: ["response"]
    }

    say context.response
}
```

## 📖 Learn More

-   [Specification](SPECIFICATION.md): Dive into the formal grammar and statement semantics.
-   [Tutorial (USAGE.md)](USAGE.md): Learn how to build your first intelligent agent.
-   [Technical Guide](DOCUMENTATION.md): Explore the underlying architecture and bridge system.

## License

MIT
