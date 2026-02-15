#!/usr/bin/env python3
"""
Zai 多Agent交互测试脚本

这个脚本演示了两个Agent之间如何通过 notify/wait 机制进行协作。
使用多进程模拟真实的多Agent环境。

运行方式:
    python examples/multi_agent/test_restaurant.py
"""

import os
import sys
import time
import shutil
import multiprocessing

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zai.core.parser import get_parser
from zai.core.interpreter import Interpreter


# 厨师Agent代码 - 接收订单并处理
CHEF_CODE = """
agent ChefAgent

context KitchenContext {
    dish_name: "",
    status: ""
}

skill Main() {
    say "==========================================="
    say "        厨房系统启动 - ChefAgent"
    say "==========================================="
    say "等待服务员提交订单..."
    say ""

    var order_count = 0

    while order_count < 3 {
        [order_status, order_data] = wait WaiterAgent

        say ""
        say "-------------------------------------------"
        say "收到新订单!"

        if order_status == "NEW_ORDER" {
            context.dish_name = order_data
            context.status = "preparing"

            say "订单详情: 菜品={{dish_name}}"
            say "开始烹饪..."

            exec "bash -c 'sleep 1'"

            say "{{dish_name}} 制作完成!"
            say "通知服务员取餐..."

            notify WaiterAgent "ORDER_READY" "{{dish_name}}"
            say "已通知服务员"

            order_count = order_count + 1
        }
    }

    say ""
    say "==========================================="
    say "厨房任务完成，准备收工..."
    say "==========================================="

    success 0 "厨房关闭"
}
"""


# 服务员Agent代码 - 接待顾客并发送订单
WAITER_CODE = """
agent WaiterAgent

context ServiceContext {
    customer_name: "",
    order_list: "",
    current_order: "",
    order_count: 0,
    total_served: 0
}

skill Main() {
    say "==========================================="
    say "        服务系统启动 - WaiterAgent"
    say "==========================================="
    say ""

    context.customer_name = "测试顾客"

    say "欢迎，{{customer_name}}!"

    var i = 0

    while i < 3 {
        if i == 0 {
            context.current_order = "宫保鸡丁"
        } else {
            if i == 1 {
                context.current_order = "麻婆豆腐"
            } else {
                context.current_order = "红烧肉"
            }
        }

        say ""
        say "----------- 点餐 -----------"
        say "顾客点单: {{current_order}}"

        if context.order_list == "" {
            context.order_list = context.current_order
        } else {
            context.order_list = "{{order_list}}, {{current_order}}"
        }

        say "正在将订单发送到厨房..."
        notify ChefAgent "NEW_ORDER" "{{current_order}}"
        say "订单已发送"

        context.order_count = context.order_count + 1

        say ""
        say "等待厨房出餐..."

        [chef_code, chef_msg] = wait ChefAgent

        if chef_code == "ORDER_READY" {
            say ""
            say "厨房通知: {{chef_msg}} 已准备好!"
            say "正在上菜..."

            context.total_served = context.total_served + 1

            say "已上菜: {{chef_msg}}"
            say "已上: {{total_served}} / {{order_count}}"
        }

        i = i + 1
    }

    say ""
    say "==========================================="
    say "所有餐品已上齐!"
    say "顾客: {{customer_name}}"
    say "上菜数: {{total_served}}"
    say "感谢光临!"
    say "==========================================="

    success 0 "服务完成"
}
"""


def run_chef():
    """运行厨师Agent"""
    parser = get_parser()
    tree = parser.parse(CHEF_CODE, start='agent')
    interpreter = Interpreter(tree, wait_timeout=30)
    interpreter.run()


def run_waiter():
    """运行服务员Agent"""
    # 稍微延迟启动，让厨师先准备好
    time.sleep(1)

    parser = get_parser()
    tree = parser.parse(WAITER_CODE, start='agent')
    interpreter = Interpreter(tree, wait_timeout=30)
    interpreter.run()


def cleanup_ipc():
    """清理IPC目录"""
    ipc_dirs = [".zai_ipc", "/tmp/zai_ipc"]
    for ipc_dir in ipc_dirs:
        if os.path.exists(ipc_dir):
            try:
                shutil.rmtree(ipc_dir)
                print(f"[系统] 清理IPC目录: {ipc_dir}")
            except Exception as e:
                print(f"[系统] 清理失败: {e}")


def main():
    print("=" * 50)
    print("    Zai 多Agent交互演示 - 智能餐厅系统")
    print("=" * 50)
    print()
    print("场景说明:")
    print("  - ChefAgent (厨师): 接收订单，烹饪，通知完成")
    print("  - WaiterAgent (服务员): 点餐，发送订单，等待出餐")
    print()
    print("通信机制:")
    print("  - notify: 发送消息给目标Agent")
    print("  - wait: 等待来自特定Agent的消息")
    print()
    print("-" * 50)
    print()

    # 清理旧的IPC文件
    cleanup_ipc()

    # 启动厨师进程
    print("[系统] 启动厨师Agent...")
    chef_process = multiprocessing.Process(target=run_chef, name="ChefAgent")
    chef_process.start()

    # 启动服务员进程
    print("[系统] 启动服务员Agent...")
    waiter_process = multiprocessing.Process(target=run_waiter, name="WaiterAgent")
    waiter_process.start()

    print()
    print("-" * 50)
    print()

    # 等待进程完成
    waiter_process.join(timeout=60)
    chef_process.join(timeout=5)  # 给厨师一些时间完成收尾

    # 检查结果
    print()
    print("-" * 50)

    if waiter_process.exitcode == 0:
        print("[系统] 服务员Agent正常退出")
    else:
        print(f"[系统] 服务员Agent异常退出 (exitcode: {waiter_process.exitcode})")

    if chef_process.exitcode == 0:
        print("[系统] 厨师Agent正常退出")
    else:
        print(f"[系统] 厨师Agent异常退出 (exitcode: {chef_process.exitcode})")

    # 强制终止仍在运行的进程
    if chef_process.is_alive():
        chef_process.terminate()
    if waiter_process.is_alive():
        waiter_process.terminate()

    print()
    print("=" * 50)
    print("    多Agent交互演示完成!")
    print("=" * 50)

    # 清理
    cleanup_ipc()


if __name__ == "__main__":
    main()
