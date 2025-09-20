#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT文件转JSON格式切分工具
将extracted_texts目录下的TXT文件转换为JSON格式，并按照指定参数进行切分
"""

import json
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any
import re


def split_text_file(file_path: Path, chunk_size: int = 30, chunk_overlap: int = 5) -> List[Dict[str, Any]]:
    """
    切分单个文本文件
    
    Args:
        file_path: 文本文件路径
        chunk_size: 每个块的最大行数
        chunk_overlap: 块之间的重叠行数
    
    Returns:
        包含切分块的列表
    """
    chunks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # 按行切分
        start_line = 1
        while start_line <= total_lines:
            end_line = min(start_line + chunk_size - 1, total_lines)
            
            # 提取当前块的行
            chunk_lines = lines[start_line - 1:end_line]
            chunk_text = ''.join(chunk_lines)
            
            # 创建块对象
            chunk = {
                "lines": [start_line, end_line],
                "text": chunk_text
            }
            
            chunks.append(chunk)
            
            # 计算下一个块的起始行（考虑重叠）
            start_line = end_line - chunk_overlap + 1
            
            # 避免无限循环
            if start_line > total_lines:
                break
    
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return []
    
    return chunks


def generate_sha1(file_path: Path) -> str:
    """生成文件的SHA1哈希值"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return hashlib.sha1(content).hexdigest()
    except:
        return f"file_{file_path.stem}"


def extract_company_name(file_name: str) -> str:
    """从文件名中提取公司/机构名称"""
    # 移除文件扩展名
    name = file_name.replace('_extracted.txt', '')
    
    # 尝试提取机构名称
    patterns = [
        r'^(.+?)(?:报告|展望|分析)',
        r'^(.+?)(?:\d{4}年)',
        r'^(.+?)(?:202[0-9])',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            return match.group(1).strip()
    
    return name


def convert_txt_to_json(input_dir: Path, output_dir: Path, chunk_size: int = 30, chunk_overlap: int = 5):
    """
    批量转换TXT文件为JSON格式
    
    Args:
        input_dir: 输入目录（包含TXT文件）
        output_dir: 输出目录（保存JSON文件）
        chunk_size: 每个块的最大行数
        chunk_overlap: 块之间的重叠行数
    """
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有TXT文件
    txt_files = list(input_dir.glob("*.txt"))
    
    if not txt_files:
        print(f"在 {input_dir} 中未找到TXT文件")
        return
    
    print(f"找到 {len(txt_files)} 个TXT文件，开始转换...")
    
    for txt_file in txt_files:
        print(f"\n处理文件: {txt_file.name}")
        
        # 生成SHA1
        sha1 = generate_sha1(txt_file)
        
        # 提取公司名称
        company_name = extract_company_name(txt_file.name)
        
        # 切分文件
        chunks = split_text_file(txt_file, chunk_size, chunk_overlap)
        
        if not chunks:
            print(f"  警告: 文件 {txt_file.name} 切分失败")
            continue
        
        # 构建JSON结构
        json_data = {
            "metainfo": {
                "sha1": sha1,
                "company_name": company_name,
                "file_name": txt_file.name
            },
            "content": {
                "chunks": chunks
            }
        }
        
        # 生成输出文件名
        output_file = output_dir / f"{txt_file.stem}.json"
        
        # 保存JSON文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"  成功: 生成 {output_file.name} ({len(chunks)} 个块)")
            
        except Exception as e:
            print(f"  错误: 保存 {output_file.name} 失败: {e}")
    
    print(f"\n转换完成！共处理 {len(txt_files)} 个文件")


def main():
    """主函数"""
    # 设置路径
    current_dir = Path(".")
    input_dir = current_dir / "data" / "extracted_texts"
    output_dir = current_dir / "data" / "json_segments"
    
    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"错误: 输入目录 {input_dir} 不存在")
        return
    
    print("=== TXT文件转JSON格式切分工具 ===")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"切分参数: chunk_size=30, chunk_overlap=5")
    print("=" * 50)
    
    # 执行转换
    convert_txt_to_json(input_dir, output_dir)
    
    print(f"\n✅ 转换完成！")
    print(f"📁 输出目录: {output_dir}")
    print(f"📊 可以在输出目录中查看生成的JSON文件")


if __name__ == "__main__":
    main() 