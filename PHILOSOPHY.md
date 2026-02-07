# zai Language Philosophy: The Cognitive Computing Model

[English](PHILOSOPHY.md) | [中文](PHILOSOPHY.zh-CN.md)

The design philosophy of zai-lang stems from simulating human cognitive processes. We believe that building AI Agents should be as natural as human thinking.

---

## Brain Analogies for Core Concepts

### Context = Long-term Memory

**Corresponds to in the brain**: Long-term memory storage in the cerebral cortex

Just as the human brain stores past experiences, knowledge, and current perceptions of the world, zai's `context` is the Agent's **persistent memory field**. It's not a parameter passed between functions, but an ever-present cognitive background.

```zai
context Memory {
    user_preferences: ""           // User preference memory
    conversation_history: []       // Conversation history memory
    current_task_state: ""         // Current task state
    learned_knowledge: ""          // Knowledge acquired through learning
}
```

**Key Insight**:
- Humans don't reintroduce themselves every conversation, and neither does context
- Humans adjust behavior based on memory, Agents adjust responses based on context
- Human memory accumulates continuously, context also evolves throughout the session

---

### Persona = Cognitive Framework and Decision Tendency

**Corresponds to in the brain**: Executive function of the prefrontal cortex + situational awareness modulation

Humans activate different cognitive frameworks in different contexts:
- When facing emergency danger, "fight or flight" mode activates
- When facing friends, social affinity mode activates
- When facing work problems, analytical mode activates

`persona` is this **contextualized cognitive framework**, which determines how the AI "thinks" and "makes decisions".

```zai
persona CrisisHandler {
    // Cognitive framework in emergency situations
    if (context.severity == "critical") {
        system: "You are in crisis handling mode:
                 1. Prioritize damage control, respond quickly
                 2. Focus only on the most critical information
                 3. Give clear, executable instructions"
    }

    // Cognitive framework in daily situations
    else {
        system: "You are in analysis mode:
                 1. Consider various factors comprehensively
                 2. Provide detailed explanations
                 3. Explore multiple solutions"
    }
}
```

**Key Insight**:
- The same person behaves differently in different situations, the same persona can adjust dynamically based on context
- Persona is not a fixed "character setting", but a **situation-sensitive cognitive strategy**
- Like human social roles, it determines "how to think in what situation"

---

### Agent System Prompt (Base Identity) = Core Self-Cognition

**Corresponds to in the brain**: Self-representation in the cerebral cortex + emotional tone of the amygdala

Human self-cognition is relatively stable: no matter what situation you face, you know who you are and have your own core values and behavioral bottom lines. The Agent System Prompt is this **base self-cognition**.

```zai
agent CustomerServiceBot
<<<
You are a professional customer service representative.
Core values: Empathy, Efficiency, Integrity
Current customer: {{customer_name}}
>>>
```

**Difference from Persona**:
- **Agent System Prompt**: Base identity (stable, defines "who you are")
- **Persona**: Situational adaptation (dynamic, defines "how to behave in this scenario")

Just like a doctor, the base identity is "a medical worker dedicated to saving lives" (Agent System Prompt), but when facing emergency patients, "emergency rescue mode" is activated, and when facing outpatients, "diagnostic consultation mode" is activated (Persona).

---

### Skill (Skill) = Complete Task Execution Process

**Corresponds to in the brain**: Procedural memory of the basal ganglia + real-time scheduling of the prefrontal cortex

When humans execute complex tasks:
1. Recall relevant knowledge (read context)
2. Activate cognitive framework suitable for the current situation (apply persona)
3. Interact with the environment (perception/action loop)
4. Adjust based on feedback (state update)

`skill` is such a **complete cognition-action pipeline**.

```zai
skill HandleEmergency() {
    // 1. Perception: Get current situation (read context)
    say "Current situation: {{current_situation}}"

    // 2. Thinking: AI analysis (activate persona's cognitive framework)
    process CrisisHandler.system {
        extract: ["risk_level", "recommended_action"]
    }

    // 3. Action: Execute decision
    if (context.risk_level == "high") {
        exec "trigger_evacuation_protocol()"
    }

    // 4. Learning: Update memory
    context.action_history = "Executed {{recommended_action}} at {{timestamp}}"
}
```

**Key Insight**:
- Skill is not a simple "function", but a **complete intelligent agent with memory, personality, and learning ability**
- Just like human experts executing tasks, combining experience (context) and professional intuition (persona)
- Each execution enriches the agent's "experience"

---

## Execution Model: The Cognitive Loop

![Cognitive Model](./docs/cognitive_model_en.png)

*Figure 1: zai-lang Cognitive Architecture and Brain Analogy*

The above diagram shows the core design philosophy of zai-lang:
- **Left side (Human Brain)**: Cerebral cortex (long-term memory) → Prefrontal cortex (cognitive framework) → Basal ganglia (program execution)
- **Right side (zai Agent)**: Perfect mapping of Context → Persona → Skill
- **Bottom loop**: Complete cognitive closed loop of perception-integration-cognition-decision-action-learning

```
┌─────────────────────────────────────────────────────────────┐
│                      Cognitive Loop                          │
│                                                             │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐         │
│   │  Memory  │─────▶│  Persona │─────▶│  Action  │         │
│   │(Context) │      │(Cognitive│      │ (Skill)  │         │
│   │          │      │Framework)│      │          │         │
│   └──────────┘      └──────────┘      └─────┬────┘         │
│         ▲                                   │               │
│         │                                   ▼               │
│         │                            ┌──────────┐          │
│         │                            │ External │          │
│         │                            │ World    │          │
│         │                            │          │          │
│         └────────────────────────────│ AI/Human/│          │
│                                      │ Systems  │          │
│                                      └──────────┘          │
└─────────────────────────────────────────────────────────────┘
```

**Loop Process**:

1. **Sense**: Acquire information from the external world (`ask`, `exec` results)
2. **Integrate**: Update memory (`context.xxx = value`)
3. **Cognize**: Reason based on memory and personality framework (`process`)
4. **Decide**: Determine actions based on reasoning results (`if/while` logic)
5. **Act**: Influence the external world (`exec`, `say`, `notify`)
6. **Learn**: Feed results back into memory (context update)

This is highly consistent with the [perception-cognition-action loop](https://en.wikipedia.org/wiki/Perception%E2%80%93cognition%E2%80%93action_loop) of human cognitive science.

---

## Comparison with Traditional Agent Development

![Comparison](./docs/comparison_en.png)

*Figure 2: Traditional Development vs zai-lang Development Paradigm Comparison*

### Traditional Development Mode

```python
# Traditional way: code + prompts separated
import openai

def handle_user_request(user_input, history, user_profile, settings):
    # 1. Manually build prompts (reassemble every time)
    prompt = f"""
    You are an assistant.
    User history: {history}
    User profile: {user_profile}
    Settings: {settings}

    User says: {user_input}
    Please reply:
    """

    # 2. Call LLM
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # 3. Manually parse results
    reply = response.choices[0].message.content

    # 4. Manually update state
    history.append({"user": user_input, "assistant": reply})
    save_to_database(history)

    return reply
```

**Problems**:
- ❌ State management is "external", easy to lose context
- ❌ Prompts are string concatenation, difficult to maintain and version control
- ❌ Cognitive framework (system prompt) is hardcoded, cannot be contextualized
- ❌ Every call requires manually passing all context

---

### zai-lang Mode

```zai
agent Assistant

// 1. Explicitly declare persistent memory
context Memory {
    history: []
    user_profile: {}
    preferences: {}
}

// 2. Explicitly declare cognitive framework
persona AdaptivePersona {
    if (context.user_emotion == "frustrated") {
        system: "You are a patient customer service agent, prioritize emotional comfort"
    } else {
        system: "You are an efficient problem solver"
    }
}

// 3. Complete cognition-action loop
skill HandleRequest(user_input) {
    // Perception: Understand user input
    context.current_input = user_input

    // Cognition: AI analysis (automatically carries complete context and persona)
    process AdaptivePersona.system {
        extract: ["intent", "emotion", "response"]
    }

    // Learning: Automatically update memory
    context.history = context.history + [{
        input: user_input,
        output: context.response,
        emotion: context.emotion
    }]

    // Action: Output reply
    say context.response
}
```

**Advantages**:
- ✅ **State is native**: context is a language-level feature, automatically persisted
- ✅ **Cognition is configurable**: persona is like CSS, declaratively defining behavior patterns
- ✅ **Context automatically passed**: process automatically carries complete context, no manual concatenation needed
- ✅ **Code is documentation**: .zai file is the complete definition of the Agent

---

## Key Advantage Summary

| Dimension | Traditional Development | zai-lang |
|-----------|------------------------|----------|
| **State Management** | External database/variables, manual passing | Native context, automatic persistence |
| **Prompt Engineering** | String concatenation, difficult to maintain | Declarative persona, version controllable |
| **Cognitive Framework** | Hardcoded system prompt | Dynamic persona, context-aware |
| **Context Passing** | Manual assembly every call | Automatic injection, complete state |
| **Human-AI Collaboration** | Requires additional development of interaction logic | Native `ask`/`say` primitives |
| **Tool Integration** | Requires writing call code | Native `exec` primitive |
| **Interpretability** | Scattered throughout code | Single .zai file, self-describing |
| **Evolvability** | High risk to modify code | Modify persona/context to adjust behavior |

---

## Paradigm Shift in Thinking

### From "Calling API" to "Designing Cognition"

Traditional development focuses on "how to call the LLM API", zai-lang focuses on "how to design the Agent's cognitive architecture".

Like:
- Traditional way is like manually operating a machine (focusing on buttons and levers)
- zai-lang is like training an employee (focusing on their knowledge and personality)

### From "Writing Code" to "Defining Mind"

In zai-lang, you are no longer just "writing programs", but **defining the mental structure of a digital life**:
- Its memory (context)
- Its personality (persona)
- Its base identity (agent system prompt)
- Its capabilities (skill)

This aligns with the [Society of Mind](https://en.wikipedia.org/wiki/Society_of_Mind) theory: intelligence emerges from the interaction of simple Agents.

---

## Conclusion

zai-lang is not just another LLM wrapper, but a **cognitive computing paradigm**. It liberates developers from "glue code" and allows them to focus on what truly matters:

> **Designing AI minds that can understand, remember, learn, and act.**
