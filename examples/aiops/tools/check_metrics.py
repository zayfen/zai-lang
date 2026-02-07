#!/usr/bin/env python3
"""模拟查询系统指标的工具"""

import sys
import random
import json

def main():
    service = sys.argv[1] if len(sys.argv) > 1 else "unknown"

    # 模拟不同服务的指标数据
    metrics = {
        "cpu_percent": random.randint(20, 95),
        "memory_percent": random.randint(30, 90),
        "disk_usage": random.randint(40, 85),
        "response_time_ms": random.randint(50, 2000),
        "error_rate": round(random.uniform(0, 0.15), 3),
        "active_connections": random.randint(10, 500),
    }

    # 根据服务类型调整指标
    if service == "api-gateway":
        metrics["response_time_ms"] = random.randint(100, 3000)
        metrics["error_rate"] = round(random.uniform(0, 0.2), 3)
    elif service == "database":
        metrics["active_connections"] = random.randint(50, 1000)
        metrics["cpu_percent"] = random.randint(30, 98)
    elif service == "web-frontend":
        metrics["memory_percent"] = random.randint(40, 95)

    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
