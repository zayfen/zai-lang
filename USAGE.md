# Getting Started with zai 🚀

Welcome to **zai**, the programming language designed to help you build AI agents as easily as writing a script. If you've ever wanted to automate a complex task using AI but found existing tools too complicated, you're in the right place!

This guide will take you from "Hello World" to building your first modular AI agent.

---

## 1. Installation

`zai` uses `uv`, a fast Python package manager.

1.  **Install uv** (if you don't have it):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Clone the project**:
    ```bash
    git clone https://github.com/your-repo/zai-lang.git
    cd zai-lang
    ```
3.  **Run your first file**:
    ```bash
    uv run zai examples/full_demo.zai
    ```

---

## 2. Your First Code: "The Greeting Agent"

Create a file named `hello.zai` and paste this in:

```zai
agent GreetingAgent

context UserProfile {
    name: "Stranger"
}

skill Main() {
    ask "What's your name? {name=}"
    say "Welcome to the future, {name}!"
    success 0 "Greeted user"
}
```

### What's happening here?
- **`agent`**: Every project starts with an `agent`. It's the name of your intelligent assistant.
- **`context`**: This is your agent's "memory." We save the user's name here.
- **`skill`**: This is where logic happens. `Main()` is the first skill your agent performs.
- **`{name=}`**: This special tag in `ask` tells `zai` to save whatever the user types into the `name` field in our context.

---

## 3. Powering Up: Talking to AI

The real power of `zai` is the `process` command. It sends your context to an AI and updates it automatically.

```zai
agent SmartAgent

context Brain {
    input: "I am feeling hungry",
    mood: "Unknown"
}

persona Personality {
    base_instruction {
        "You are a helpful psychologist."
    }
}

skill Main() {
    process "Analyze the user's mood" { extract: ["mood"] }
    say "I see you are feeling {mood} today."
    success 0 "Analyzed mood"
}
```

### How it works:
1. `process` takes your instruction ("Analyze the user's mood").
2. It looks at the **`persona`** (our Personality) to know how to behave.
3. It "extracts" the result and puts it directly into `context.mood`. No manual parsing required!

---

## 4. Keeping it Clean: Modular Projects

As your agents get smarter, your files get longer. `zai` lets you move your context and personality into separate "header" files (ending in `.zaih`).

**File: `brain.zaih`**
```zai
context MyData {
    user_name: "Admin"
}

persona MyPrompts {
    base_instruction {
        "You are a technical expert."
    }
}
```

**File: `main.zai`**
```zai
agent ModularAgent
import "brain.zaih"

skill Main() {
    say "Hello, {user_name}!"
    // ... logic ...
}
```

---

## 5. Pro Tip: Reactive Personas

Sometimes you want your AI to behave differently based on the situation. `zai` makes this incredibly easy with `if` blocks inside your **`persona`**:

```zai
persona SmartPersonality {
    base_instruction {
        "You are a helpful assistant."
        if context.is_urgent {
            "!!! IMPORTANT: The user is in a hurry. Be extremely brief !!!"
        }
    }
}
```

If `context.is_urgent` is true, `zai` will automatically add that extra warning to the AI's instructions. You don't have to write complex code to change prompts!

---

## Summary Table

| Command | What it does | Example |
| :--- | :--- | :--- |
| `say` | Prints a message | `say "Hello!"` |
| `ask` | Gets user input | `ask "Age? {age=}"` |
| `process` | Asks AI to do something | `process "Summarize" { extract: ["summary"] }` |
| `exec` | Runs a system command | `exec "ls -la" { filter: ["files"] }` |
| `import` | Loads another file | `import "config.zaih"` |
| `invoke` | Executes a recursive skill | `invoke MySkill()` |

Ready to build? Check out the `examples/` folder for more complex agents!
