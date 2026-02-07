#!/usr/bin/env python3
"""
Generate zai-lang cognitive philosophy diagrams (English version)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

def draw_brain_analogy():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 97, 'zai-lang Cognitive Computing Model: Brain Analogy',
            fontsize=18, fontweight='bold', ha='center', va='top')

    # ===== Left: Human Brain Structure =====
    brain_x = 25

    # Brain outline
    brain_outline = Circle((brain_x, 50), 20, fill=True,
                          facecolor='#FFE4B5', edgecolor='#8B4513', linewidth=3, alpha=0.3)
    ax.add_patch(brain_outline)

    # Cerebral Cortex (Context) - Long-term memory
    cortex = FancyBboxPatch((brain_x-12, 65), 24, 12,
                           boxstyle="round,pad=0.1",
                           facecolor='#87CEEB', edgecolor='#4682B4', linewidth=2)
    ax.add_patch(cortex)
    ax.text(brain_x, 71, 'Cerebral Cortex', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 67, '(Context / Long-term Memory)', fontsize=8, ha='center', va='center', style='italic')

    # Prefrontal Cortex (Persona) - Executive function
    prefrontal = FancyBboxPatch((brain_x-8, 48), 16, 12,
                               boxstyle="round,pad=0.1",
                               facecolor='#DDA0DD', edgecolor='#8B008B', linewidth=2)
    ax.add_patch(prefrontal)
    ax.text(brain_x, 54, 'Prefrontal Cortex', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 50, '(Persona / Cognitive Framework)', fontsize=8, ha='center', va='center', style='italic')

    # Basal Ganglia (Skill) - Procedural execution
    basal = FancyBboxPatch((brain_x-8, 30), 16, 12,
                          boxstyle="round,pad=0.1",
                          facecolor='#98FB98', edgecolor='#228B22', linewidth=2)
    ax.add_patch(basal)
    ax.text(brain_x, 36, 'Basal Ganglia', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 32, '(Skill / Procedural Execution)', fontsize=8, ha='center', va='center', style='italic')

    # Brain label
    ax.text(brain_x, 18, 'Human Brain', fontsize=14, ha='center', fontweight='bold', color='#8B4513')

    # ===== Middle: Connection Arrows =====
    arrow_x = 50

    ax.annotate('', xy=(arrow_x, 65), xytext=(arrow_x+8, 71),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+12, 68, 'Memory\nRetrieval', fontsize=8, ha='center', color='#FF6B6B')

    ax.annotate('', xy=(arrow_x, 54), xytext=(arrow_x+8, 60),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+12, 57, 'Framework\nActivation', fontsize=8, ha='center', color='#FF6B6B')

    ax.annotate('', xy=(arrow_x, 36), xytext=(arrow_x+8, 48),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+12, 42, 'Action\nExecution', fontsize=8, ha='center', color='#FF6B6B')

    # ===== Right: zai-lang Implementation =====
    zai_x = 75

    # Agent container
    agent_box = FancyBboxPatch((zai_x-20, 20), 40, 70,
                              boxstyle="round,pad=0.5",
                              facecolor='#F0F8FF', edgecolor='#4169E1', linewidth=3)
    ax.add_patch(agent_box)

    # Context layer
    ctx_box = FancyBboxPatch((zai_x-15, 65), 30, 18,
                            boxstyle="round,pad=0.1",
                            facecolor='#E1F5FF', edgecolor='#01579B', linewidth=2)
    ax.add_patch(ctx_box)
    ax.text(zai_x, 76, 'Context', fontsize=12, ha='center', va='center', fontweight='bold', color='#01579B')
    ax.text(zai_x, 72, 'Persistent State', fontsize=9, ha='center', va='center', color='#01579B')
    ax.text(zai_x, 68, '{ user_profile, history, state }', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # Persona layer
    per_box = FancyBboxPatch((zai_x-15, 45), 30, 16,
                            boxstyle="round,pad=0.1",
                            facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2)
    ax.add_patch(per_box)
    ax.text(zai_x, 55, 'Persona', fontsize=12, ha='center', va='center', fontweight='bold', color='#E65100')
    ax.text(zai_x, 51, 'Contextual Cognitive Framework', fontsize=8, ha='center', va='center', color='#E65100')
    ax.text(zai_x, 47, 'if/else + system prompt', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # Skill layer
    skill_box = FancyBboxPatch((zai_x-15, 25), 30, 16,
                              boxstyle="round,pad=0.1",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(skill_box)
    ax.text(zai_x, 35, 'Skill', fontsize=12, ha='center', va='center', fontweight='bold', color='#2E7D32')
    ax.text(zai_x, 31, 'Cognition-Action Loop', fontsize=9, ha='center', va='center', color='#2E7D32')
    ax.text(zai_x, 27, 'ask -> process -> exec', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # zai label
    ax.text(zai_x, 18, 'zai Agent', fontsize=14, ha='center', fontweight='bold', color='#4169E1')

    # ===== Bottom: Cognitive Cycle =====
    cycle_y = 8

    cycle_steps = [
        ('Sense\n(ask/exec)', '#FF6B6B'),
        ('Integrate\n(context)', '#4ECDC4'),
        ('Cognize\n(process)', '#45B7D1'),
        ('Decide\n(if/else)', '#96CEB4'),
        ('Act\n(exec/say)', '#FFEAA7'),
        ('Learn\n(update)', '#DDA0DD')
    ]

    step_width = 12
    start_x = 20

    for i, (step, color) in enumerate(cycle_steps):
        x = start_x + i * step_width
        circle = Circle((x, cycle_y), 4.5, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, cycle_y, step, fontsize=6.5, ha='center', va='center', fontweight='bold', color='white')

        if i < len(cycle_steps) - 1:
            ax.annotate('', xy=(x+7.5, cycle_y), xytext=(x+4.5, cycle_y),
                       arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    # Closing arrow
    ax.annotate('', xy=(start_x-2, cycle_y+5), xytext=(start_x + 5*step_width+2, cycle_y+5),
               arrowprops=dict(arrowstyle='->', color='#666', lw=1.5,
                              connectionstyle='arc3,rad=0.3'))

    ax.text(50, 2, 'Cognitive Loop (Perception-Cognition-Action)', fontsize=11, ha='center', style='italic', color='#666')

    plt.tight_layout()
    plt.savefig('/Users/riven/Github/zai-lang/docs/cognitive_model_en.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Saved: docs/cognitive_model_en.png")

def draw_comparison():
    """Traditional vs zai comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))

    # Left: Traditional Development
    ax1 = axes[0]
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title('Traditional Agent Development', fontsize=16, fontweight='bold', pad=20, color='#C0392B')

    # Scattered components
    components = [
        ('Code\n(Python/JS)', 20, 80, '#E8F8F5'),
        ('Prompt\nTemplates', 50, 80, '#E8F8F5'),
        ('State DB\n(Redis/Pg)', 80, 80, '#E8F8F5'),
        ('API Client\n(OpenAI)', 20, 50, '#FEF9E7'),
        ('String\nConcatenation', 50, 50, '#FEF9E7'),
        ('Result\nParsing', 80, 50, '#FEF9E7'),
    ]

    for name, x, y, color in components:
        box = FancyBboxPatch((x-12, y-8), 24, 16,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='#7F8C8D', linewidth=2)
        ax1.add_patch(box)
        ax1.text(x, y, name, fontsize=9, ha='center', va='center')

    # Chaotic arrows
    ax1.annotate('', xy=(45, 75), xytext=(28, 72),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, connectionstyle='arc3,rad=0.2'))
    ax1.annotate('', xy=(75, 75), xytext=(58, 72),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, connectionstyle='arc3,rad=-0.2'))
    ax1.annotate('', xy=(50, 58), xytext=(50, 72),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, connectionstyle='arc3,rad=0.1'))
    ax1.annotate('', xy=(25, 42), xytext=(20, 72),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, connectionstyle='arc3,rad=0.3'))
    ax1.annotate('', xy=(55, 42), xytext=(50, 58),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1))
    ax1.annotate('', xy=(75, 42), xytext=(80, 72),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, connectionstyle='arc3,rad=-0.3'))

    # Problems
    problems = [
        '❌ Glue code everywhere',
        '❌ Context easily lost',
        '❌ Prompts hard to maintain',
        '❌ State management scattered'
    ]
    for i, prob in enumerate(problems):
        ax1.text(50, 28 - i*6, prob, fontsize=10, ha='center', color='#C0392B')

    # Right: zai-lang
    ax2 = axes[1]
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title('zai-lang Development', fontsize=16, fontweight='bold', pad=20, color='#27AE60')

    # Unified container
    container = FancyBboxPatch((20, 25), 60, 60,
                              boxstyle="round,pad=0.5",
                              facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=3)
    ax2.add_patch(container)

    # Integrated components
    zai_components = [
        ('Context\n(Memory)', 50, 75, '#E1F5FF', '#01579B'),
        ('Persona\n(Cognition)', 50, 58, '#FFF3E0', '#E65100'),
        ('Skill\n(Action)', 50, 41, '#E8F5E9', '#2E7D32'),
    ]

    for name, x, y, bg_color, text_color in zai_components:
        box = FancyBboxPatch((x-18, y-8), 36, 16,
                            boxstyle="round,pad=0.1",
                            facecolor=bg_color, edgecolor=text_color, linewidth=2)
        ax2.add_patch(box)
        ax2.text(x, y, name, fontsize=11, ha='center', va='center',
                fontweight='bold', color=text_color)

    # Clear flow arrows
    ax2.annotate('', xy=(72, 62), xytext=(72, 75),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    ax2.text(78, 68, 'Retrieve', fontsize=8, ha='center', color='#666')

    ax2.annotate('', xy=(72, 45), xytext=(72, 58),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    ax2.text(78, 51, 'Frame', fontsize=8, ha='center', color='#666')

    ax2.annotate('', xy=(72, 35), xytext=(72, 41),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    ax2.text(78, 38, 'Execute', fontsize=8, ha='center', color='#666')

    # Feedback loop
    ax2.annotate('', xy=(55, 30), xytext=(72, 30),
                arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=2,
                               connectionstyle='arc3,rad=-0.2'))
    ax2.text(63, 33, 'Learn', fontsize=8, ha='center', color='#4ECDC4')

    # Advantages
    advantages = [
        '✅ Native state management',
        '✅ Declarative cognition',
        '✅ Unified architecture',
        '✅ Self-documenting'
    ]
    for i, adv in enumerate(advantages):
        ax2.text(50, 18 - i*5, adv, fontsize=10, ha='center', color='#27AE60')

    # File icon
    file_box = FancyBboxPatch((75, 85), 20, 10,
                             boxstyle="round,pad=0.1",
                             facecolor='#F8F9FA', edgecolor='#666', linewidth=1)
    ax2.add_patch(file_box)
    ax2.text(85, 90, '.zai', fontsize=11, ha='center', va='center',
            family='monospace', fontweight='bold', color='#2980B9')
    ax2.text(85, 82, 'One file = Complete Mind', fontsize=8, ha='center', color='#666')

    plt.tight_layout()
    plt.savefig('/Users/riven/Github/zai-lang/docs/comparison_en.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Saved: docs/comparison_en.png")

if __name__ == '__main__':
    draw_brain_analogy()
    draw_comparison()
    print("\nAll diagrams generated successfully!")
