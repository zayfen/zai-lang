#!/usr/bin/env python3
"""模拟查询日志的工具"""

import sys
import random

LOG_LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]

def generate_log_line(service, level):
    templates = {
        "INFO": [
            f"[{level}] {service}: Request processed successfully",
            f"[{level}] {service}: User authenticated",
            f"[{level}] {service}: Database connection established",
            f"[{level}] {service}: Cache hit for key user:12345",
        ],
        "WARN": [
            f"[{level}] {service}: High memory usage detected: 85%",
            f"[{level}] {service}: Slow query detected (duration: 2.5s)",
            f"[{level}] {service}: Connection pool nearing limit (18/20)",
            f"[{level}] {service}: Retry attempt 2/3 for request abc123",
        ],
        "ERROR": [
            f"[{level}] {service}: Connection timeout after 30s",
            f"[{level}] {service}: Database query failed: deadlock detected",
            f"[{level}] {service}: OutOfMemoryError: Java heap space",
            f"[{level}] {service}: NullPointerException at UserService.java:156",
            f"[{level}] {service}: 502 Bad Gateway from upstream",
        ],
        "DEBUG": [
            f"[{level}] {service}: Entering method processRequest",
            f"[{level}] {service}: Cache miss for key config:v1",
        ]
    }

    return random.choice(templates[level])

def main():
    service = sys.argv[1] if len(sys.argv) > 1 else "app"
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    # 根据服务类型调整日志级别分布
    if service in ["database", "api-gateway"]:
        weights = [30, 25, 35, 10]  # 更多错误
    else:
        weights = [50, 25, 15, 10]

    for _ in range(lines):
        level = random.choices(LOG_LEVELS, weights=weights)[0]
        print(generate_log_line(service, level))

if __name__ == "__main__":
    main()
