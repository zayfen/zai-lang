# zai

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
    ask "What is your name? {name=}"
    say "Hello, {name}!"
}
```

## 📖 Learn More

-   [Specification](SPECIFICATION.md): Dive into the formal grammar and statement semantics.
-   [Tutorial (USAGE.md)](USAGE.md): Learn how to build your first intelligent agent.
-   [Technical Guide](DOCUMENTATION.md): Explore the underlying architecture and bridge system.

## License

MIT
