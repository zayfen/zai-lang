#!/usr/bin/env python3
"""
生成 zai-lang 认知哲学架构图
使用 matplotlib 绘制人脑类比图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def draw_brain_analogy():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 标题
    ax.text(50, 97, 'zai-lang 认知计算模型：人脑类比',
            fontsize=20, fontweight='bold', ha='center', va='top')

    # ===== 左侧：人脑结构 =====
    brain_x = 25

    # 大脑轮廓
    brain_outline = Circle((brain_x, 50), 20, fill=True,
                          facecolor='#FFE4B5', edgecolor='#8B4513', linewidth=3, alpha=0.3)
    ax.add_patch(brain_outline)

    # 大脑皮层 (Context)
    cortex = FancyBboxPatch((brain_x-12, 65), 24, 12,
                           boxstyle="round,pad=0.1",
                           facecolor='#87CEEB', edgecolor='#4682B4', linewidth=2)
    ax.add_patch(cortex)
    ax.text(brain_x, 71, '大脑皮层\n(Context)', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 67, '长期记忆', fontsize=8, ha='center', va='center', style='italic')

    # 前额叶 (Persona)
    prefrontal = FancyBboxPatch((brain_x-8, 48), 16, 12,
                               boxstyle="round,pad=0.1",
                               facecolor='#DDA0DD', edgecolor='#8B008B', linewidth=2)
    ax.add_patch(prefrontal)
    ax.text(brain_x, 54, '前额叶\n(Persona)', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 50, '认知框架', fontsize=8, ha='center', va='center', style='italic')

    # 基底神经节 (Skill)
    basal = FancyBboxPatch((brain_x-8, 30), 16, 12,
                          boxstyle="round,pad=0.1",
                          facecolor='#98FB98', edgecolor='#228B22', linewidth=2)
    ax.add_patch(basal)
    ax.text(brain_x, 36, '神经节\n(Skill)', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(brain_x, 32, '程序执行', fontsize=8, ha='center', va='center', style='italic')

    # 人脑标签
    ax.text(brain_x, 18, '人类大脑', fontsize=14, ha='center', fontweight='bold', color='#8B4513')

    # ===== 中间：循环箭头 =====
    arrow_x = 50

    # 循环箭头
    ax.annotate('', xy=(arrow_x, 65), xytext=(arrow_x+8, 71),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+10, 68, '记忆\n检索', fontsize=8, ha='center', color='#FF6B6B')

    ax.annotate('', xy=(arrow_x, 54), xytext=(arrow_x+8, 60),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+10, 57, '框架\n激活', fontsize=8, ha='center', color='#FF6B6B')

    ax.annotate('', xy=(arrow_x, 36), xytext=(arrow_x+8, 48),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2))
    ax.text(arrow_x+10, 42, '行动\n执行', fontsize=8, ha='center', color='#FF6B6B')

    # 反馈循环
    ax.annotate('', xy=(arrow_x+3, 30), xytext=(arrow_x+3, 25),
                arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=2, connectionstyle='arc3,rad=0.3'))
    ax.text(arrow_x+8, 27, '学习\n反馈', fontsize=8, ha='center', color='#4ECDC4')

    # ===== 右侧：zai-lang 实现 =====
    zai_x = 75

    # Agent 容器
    agent_box = FancyBboxPatch((zai_x-20, 20), 40, 70,
                              boxstyle="round,pad=0.5",
                              facecolor='#F0F8FF', edgecolor='#4169E1', linewidth=3)
    ax.add_patch(agent_box)

    # Context 层
    ctx_box = FancyBboxPatch((zai_x-15, 65), 30, 18,
                            boxstyle="round,pad=0.1",
                            facecolor='#E1F5FF', edgecolor='#01579B', linewidth=2)
    ax.add_patch(ctx_box)
    ax.text(zai_x, 76, 'Context', fontsize=12, ha='center', va='center', fontweight='bold', color='#01579B')
    ax.text(zai_x, 72, '持久化状态', fontsize=9, ha='center', va='center', color='#01579B')
    ax.text(zai_x, 68, '{ user_profile, history, state }', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # Persona 层
    per_box = FancyBboxPatch((zai_x-15, 45), 30, 16,
                            boxstyle="round,pad=0.1",
                            facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2)
    ax.add_patch(per_box)
    ax.text(zai_x, 55, 'Persona', fontsize=12, ha='center', va='center', fontweight='bold', color='#E65100')
    ax.text(zai_x, 51, '情境化认知框架', fontsize=9, ha='center', va='center', color='#E65100')
    ax.text(zai_x, 47, 'if/else + system prompt', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # Skill 层
    skill_box = FancyBboxPatch((zai_x-15, 25), 30, 16,
                              boxstyle="round,pad=0.1",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(skill_box)
    ax.text(zai_x, 35, 'Skill', fontsize=12, ha='center', va='center', fontweight='bold', color='#2E7D32')
    ax.text(zai_x, 31, '认知-行动循环', fontsize=9, ha='center', va='center', color='#2E7D32')
    ax.text(zai_x, 27, 'ask → process → exec', fontsize=7, ha='center', va='center',
            family='monospace', color='#555')

    # zai 标签
    ax.text(zai_x, 18, 'zai Agent', fontsize=14, ha='center', fontweight='bold', color='#4169E1')

    # ===== 底部：循环说明 =====
    cycle_y = 8

    # 认知循环流程
    cycle_steps = ['感知\nSense', '整合\nIntegrate', '认知\nCognize', '决策\nDecide', '执行\nAct', '学习\nLearn']
    cycle_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

    step_width = 12
    start_x = 20

    for i, (step, color) in enumerate(zip(cycle_steps, cycle_colors)):
        x = start_x + i * step_width
        circle = Circle((x, cycle_y), 4, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, cycle_y, step, fontsize=7, ha='center', va='center', fontweight='bold', color='white')

        if i < len(cycle_steps) - 1:
            ax.annotate('', xy=(x+8, cycle_y), xytext=(x+4, cycle_y),
                       arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    # 闭环箭头
    ax.annotate('', xy=(start_x, cycle_y+5), xytext=(start_x + 5*step_width, cycle_y+5),
               arrowprops=dict(arrowstyle='->', color='#666', lw=1.5,
                              connectionstyle='arc3,rad=0.3'))

    ax.text(50, 2, '认知循环 (Cognitive Loop)', fontsize=11, ha='center', style='italic', color='#666')

    plt.tight_layout()
    plt.savefig('/Users/riven/Github/zai-lang/docs/cognitive_model.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ 认知模型图已生成: docs/cognitive_model.png")

def draw_comparison():
    """生成传统 vs zai 对比图"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))

    # 左侧：传统开发
    ax1 = axes[0]
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title('传统 Agent 开发', fontsize=16, fontweight='bold', pad=20, color='#C0392B')

    # 散落的组件
    components = [
        ('代码\nCode', 20, 80, '#E8F8F5'),
        ('提示词\nPrompt', 50, 80, '#E8F8F5'),
        ('状态管理\nState DB', 80, 80, '#E8F8F5'),
        ('API 调用\nAPI Call', 20, 50, '#FEF9E7'),
        ('字符串拼接\nString Concat', 50, 50, '#FEF9E7'),
        ('结果解析\nParsing', 80, 50, '#FEF9E7'),
    ]

    for name, x, y, color in components:
        box = FancyBboxPatch((x-12, y-8), 24, 16,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='#7F8C8D', linewidth=2)
        ax1.add_patch(box)
        ax1.text(x, y, name, fontsize=9, ha='center', va='center')

    # 混乱的箭头
    for i, (x1, y1) in enumerate([(20, 72), (50, 72), (80, 72), (20, 42), (50, 42)]):
        for j, (x2, y2) in enumerate([(50, 50), (80, 50), (50, 80), (20, 50)]):
            if i != j and np.random.random() > 0.5:
                ax1.plot([x1, x2], [y1, y2], 'k-', alpha=0.2, linewidth=0.5)

    # 问题标注
    problems = ['❌ 胶水代码多', '❌ 状态易丢失', '❌ 提示难维护', '❌ 上下文断裂']
    for i, prob in enumerate(problems):
        ax1.text(50, 25 - i*6, prob, fontsize=10, ha='center', color='#C0392B')

    # 右侧：zai-lang
    ax2 = axes[1]
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title('zai-lang 开发', fontsize=16, fontweight='bold', pad=20, color='#27AE60')

    # 统一容器
    container = FancyBboxPatch((20, 25), 60, 60,
                              boxstyle="round,pad=0.5",
                              facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=3)
    ax2.add_patch(container)

    # 有机整合的组件
    zai_components = [
        ('Context\n(记忆)', 50, 75, '#E1F5FF', '#01579B'),
        ('Persona\n(认知)', 50, 58, '#FFF3E0', '#E65100'),
        ('Skill\n(行动)', 50, 41, '#E8F5E9', '#2E7D32'),
    ]

    for name, x, y, bg_color, text_color in zai_components:
        box = FancyBboxPatch((x-18, y-8), 36, 16,
                            boxstyle="round,pad=0.1",
                            facecolor=bg_color, edgecolor=text_color, linewidth=2)
        ax2.add_patch(box)
        ax2.text(x, y, name, fontsize=11, ha='center', va='center',
                fontweight='bold', color=text_color)

    # 清晰的循环箭头
    ax2.annotate('', xy=(70, 58), xytext=(70, 75),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    ax2.annotate('', xy=(70, 41), xytext=(70, 58),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    ax2.annotate('', xy=(50, 30), xytext=(70, 30),
                arrowprops=dict(arrowstyle='->', color='#666', lw=2,
                              connectionstyle='arc3,rad=-0.3'))
    ax2.text(60, 33, '学习反馈', fontsize=8, ha='center', color='#666')

    # 优势标注
    advantages = ['✅ 原生状态管理', '✅ 声明式认知', '✅ 统一架构', '✅ 自我描述']
    for i, adv in enumerate(advantages):
        ax2.text(50, 18 - i*5, adv, fontsize=10, ha='center', color='#27AE60')

    # 文件图标
    file_box = FancyBboxPatch((75, 85), 20, 10,
                             boxstyle="round,pad=0.1",
                             facecolor='#F8F9FA', edgecolor='#666', linewidth=1)
    ax2.add_patch(file_box)
    ax2.text(85, 90, '.zai', fontsize=11, ha='center', va='center',
            family='monospace', fontweight='bold', color='#2980B9')
    ax2.text(85, 82, '单一文件 = 完整心智', fontsize=8, ha='center', color='#666')

    plt.tight_layout()
    plt.savefig('/Users/riven/Github/zai-lang/docs/comparison.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ 对比图已生成: docs/comparison.png")

if __name__ == '__main__':
    draw_brain_analogy()
    draw_comparison()
    print("\n所有图片已生成到 docs/ 目录")
