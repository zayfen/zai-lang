# AIOps 智能运维告警处理系统

基于 zai-lang 构建的智能运维自动化系统，展示 AI 与自动化工具的深度集成。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AIOpsOrchestrator                        │
│                     (主协调器)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ ReceiveAlert │→│CollectDiagnostics│→│AnalyzeWithAI│       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                              ↓              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │GenerateReport│←│DecideAndRemediate│←│  AI 分析结果 │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      工具层                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │check_metrics│  │query_logs│  │knowledge_base│  │simulate_fix│
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 特性

- **智能诊断**: AI 分析系统指标和日志，自动定位根因
- **知识库支持**: 历史故障匹配，提供修复建议
- **分级响应**: 根据告警级别 (critical/warning/info) 执行不同策略
- **人机协作**: 高风险操作需人工确认
- **完整追踪**: 全流程日志和报告生成

## 文件结构

```
examples/aiops/
├── orchestrator.zai          # 主程序 - 5阶段处理流程
├── README.md                 # 本文档
└── tools/
    ├── check_metrics.py      # 查询系统指标
    ├── query_logs.py         # 查询服务日志
    ├── knowledge_base.py     # 历史故障知识库
    └── simulate_fix.py       # 模拟修复操作
```

## 使用方法

```bash
# 进入示例目录
cd examples/aiops

# 运行主程序
zai orchestrator.zai
```

## 交互流程

1. **接收告警** - 输入告警信息（服务、级别、类型）
2. **收集诊断** - 自动查询指标、日志、知识库
3. **AI 分析** - LLM 分析根因，给出修复建议
4. **决策处置** - 根据置信度和级别决定自动修复或人工确认
5. **生成报告** - 输出完整处理报告

## 决策逻辑

| 告警级别 | AI 置信度 | 处理方式 |
|---------|----------|---------|
| Critical | ≥ 0.8 | 自动修复 |
| Critical | < 0.8 | 人工介入 |
| Warning | ≥ 0.8 | 人工确认后修复 |
| Warning | < 0.8 | 建议人工诊断 |
| Info | 任意 | 仅生成报告 |

## 配置

通过环境变量或配置文件设置 AI 模型：

```bash
# Shell 环境变量
export ZAI_MODEL="claude-3-5-sonnet"
export ZAI_TEMPERATURE=0.3

# 或当前目录 .zai/config.json
echo '{"ZAI_MODEL": "gpt-4", "ZAI_TEMPERATURE": 0.5}' > .zai/config.json
```

配置优先级：
1. Shell 环境变量
2. 当前目录 `.zai/config.json`
3. 用户目录 `~/.config/zai/config.json`

## 工具说明

### check_metrics.py
模拟查询服务指标，返回 JSON 格式：
```json
{
  "cpu_percent": 40,
  "memory_percent": 62,
  "response_time_ms": 1327,
  "error_rate": 0.07,
  "active_connections": 411
}
```

### query_logs.py
模拟查询服务日志，支持指定行数。
根据服务类型调整日志级别分布。

### knowledge_base.py
模拟历史故障知识库查询，返回匹配的问题类型和修复方案。

### simulate_fix.py
模拟执行修复操作，根据操作类型返回不同成功率。

## 扩展建议

1. **接入真实监控系统**: 替换模拟工具为 Prometheus/Grafana API
2. **增强知识库**: 接入向量数据库存储历史故障 (如 Milvus/Pinecone)
3. **多 Agent 协作**: 不同服务由专门 Agent 处理，通过 `notify`/`wait` 协调
4. **告警抑制**: 添加关联分析减少告警风暴
5. **持久化**: 将处理记录写入数据库，支持历史查询

## zai-lang 特性展示

本示例展示了 zai-lang 的核心能力：

- **Context 上下文**: 跨 skill 状态共享
- **Persona 人格**: 定义 AI 专家角色
- **Process AI 处理**: AI 分析并提取结构化数据
- **Exec 执行**: 调用外部工具
- **Ask 交互**: 人机协作输入
- **Skill 编排**: 模块化业务流程
- **模板渲染**: `{{variable}}` 动态插值（自动从 context 或局部变量获取）
