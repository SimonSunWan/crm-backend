#!/usr/bin/env python3
"""代码格式化脚本"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"正在执行: {description}")
    print(f"命令: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def main():
    """主函数"""
    print("🚀 开始代码格式化...")
    
    # 检查是否安装了必要的工具
    tools = ['black', 'isort', 'flake8']
    missing_tools = []
    
    for tool in tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ 缺少以下工具: {', '.join(missing_tools)}")
        print("请先安装这些工具:")
        print("pip install black isort flake8")
        return False
    
    # 定义要格式化的目录
    directories = ['app', 'scripts']
    
    success = True
    
    # 1. 使用 isort 排序导入
    for directory in directories:
        if os.path.exists(directory):
            cmd = f"isort {directory} --profile black"
            if not run_command(cmd, f"排序 {directory} 目录的导入"):
                success = False
    
    # 2. 使用 black 格式化代码
    for directory in directories:
        if os.path.exists(directory):
            cmd = f"black {directory} --line-length 88"
            if not run_command(cmd, f"格式化 {directory} 目录的代码"):
                success = False
    
    # 3. 使用 flake8 检查代码
    for directory in directories:
        if os.path.exists(directory):
            if directory == "scripts":
                # scripts目录忽略E402错误（导入顺序问题）
                cmd = f"flake8 {directory} --max-line-length 88 --ignore E203,W503,E402"
            else:
                cmd = f"flake8 {directory} --max-line-length 88 --ignore E203,W503"
            if not run_command(cmd, f"检查 {directory} 目录的代码"):
                success = False
    
    if success:
        print("\n✅ 代码格式化完成!")
    else:
        print("\n❌ 代码格式化过程中出现错误")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
