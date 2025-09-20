#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证配置和基本功能
"""

import os
from pathlib import Path

# 从主脚本导入配置
from pdf_mineru import (
    ALIBABA_API_KEY, ALIBABA_API_BASE_URL,
    RETRY_INTERVAL, FILE_PROCESSING_INTERVAL, MAX_RETRIES,
    OUTPUT_DIR, LOG_FILE
)

def test_config():
    """测试配置文件"""
    print("=== 配置测试 ===")
    print(f"API密钥: {ALIBABA_API_KEY[:10]}...{ALIBABA_API_KEY[-10:]}")
    print(f"API基础URL: {ALIBABA_API_BASE_URL}")
    print(f"重试间隔: {RETRY_INTERVAL}秒")
    print(f"文件处理间隔: {FILE_PROCESSING_INTERVAL}秒")
    print(f"最大重试次数: {MAX_RETRIES}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"日志文件: {LOG_FILE}")

def test_pdf_files():
    """测试PDF文件检测"""
    print("\n=== PDF文件检测测试 ===")
    current_dir = Path('.')
    pdf_files = list(current_dir.glob('*.pdf'))
    
    if pdf_files:
        print(f"找到 {len(pdf_files)} 个PDF文件:")
        for i, file in enumerate(pdf_files, 1):
            print(f"  {i}. {file.name} ({file.stat().st_size / 1024 / 1024:.1f} MB)")
    else:
        print("未找到PDF文件")

def test_output_directory():
    """测试输出目录创建"""
    print("\n=== 输出目录测试 ===")
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"输出目录 '{OUTPUT_DIR}' 创建成功")
        
        # 检查目录权限
        test_file = os.path.join(OUTPUT_DIR, 'test.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('测试文件')
        os.remove(test_file)
        print("目录写入权限正常")
        
    except Exception as e:
        print(f"输出目录测试失败: {e}")

def main():
    """主测试函数"""
    print("PDF处理工具配置测试")
    print("=" * 50)
    
    test_config()
    test_pdf_files()
    test_output_directory()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n如果所有测试都通过，您可以运行 'python pdf_mineru.py' 开始处理PDF文件。")
    print("请确保在运行前更新 pdf_mineru.py 中的 ALIBABA_API_KEY。")

if __name__ == "__main__":
    main() 