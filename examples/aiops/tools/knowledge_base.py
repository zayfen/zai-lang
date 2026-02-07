#!/usr/bin/env python3
"""模拟知识库查询工具 - 返回历史类似问题的解决方案"""

import sys
import json

# 模拟知识库
KB = {
    "connection_timeout": {
        "symptoms": ["Connection timeout", "Slow response", "Connection pool exhausted"],
        "solutions": ["restart", "scale_up", "clear_cache"],
        "success_rate": 0.85,
        "avg_fix_time": "5m"
    },
    "memory_issue": {
        "symptoms": ["OutOfMemoryError", "High memory usage", "GC overhead"],
        "solutions": ["restart", "scale_up"],
        "success_rate": 0.90,
        "avg_fix_time": "3m"
    },
    "database_deadlock": {
        "symptoms": ["Deadlock detected", "Transaction rollback", "Lock wait timeout"],
        "solutions": ["clear_cache", "switch_db", "restart"],
        "success_rate": 0.75,
        "avg_fix_time": "8m"
    },
    "high_error_rate": {
        "symptoms": ["502 Bad Gateway", "500 Internal Error", "NullPointerException"],
        "solutions": ["rollback", "restart", "clear_cache"],
        "success_rate": 0.80,
        "avg_fix_time": "10m"
    },
    "slow_query": {
        "symptoms": ["Slow query", "Query timeout", "High CPU"],
        "solutions": ["clear_cache", "scale_up"],
        "success_rate": 0.70,
        "avg_fix_time": "4m"
    }
}

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""

    # 模糊匹配
    results = []
    keyword_lower = keyword.lower()

    for issue_type, data in KB.items():
        # 检查症状是否匹配
        for symptom in data["symptoms"]:
            if keyword_lower in symptom.lower() or symptom.lower() in keyword_lower:
                results.append({
                    "issue_type": issue_type,
                    **data
                })
                break

    if not results:
        # 返回默认结果
        results = [{
            "issue_type": "unknown",
            "symptoms": ["Unknown issue"],
            "solutions": ["restart", "scale_up"],
            "success_rate": 0.60,
            "avg_fix_time": "15m"
        }]

    print(json.dumps(results[:3], indent=2))

if __name__ == "__main__":
    main()
