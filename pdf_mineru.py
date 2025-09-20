#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文本提取工具 - 使用阿里云百炼API
用于从PDF文件中提取文本内容
"""

import requests
import time
import zipfile
import os
import logging
import json
import base64
from pathlib import Path

# ==================== 配置区域 ====================
# 请在此处配置您的API密钥和其他设置
# 
# 重要：请将下面的API密钥替换为您的有效密钥
# 获取API密钥：https://bailian.console.aliyun.com/

# 阿里云百炼API密钥配置
ALIBABA_API_KEY = 'sk-db159bb711df4c46ae4db8100e304516'  # 请替换为您的实际API密钥

# 阿里云百炼API端点
ALIBABA_API_BASE_URL = 'https://dashscope.aliyuncs.com'

# 处理设置
RETRY_INTERVAL = 5  # 重试间隔（秒）
FILE_PROCESSING_INTERVAL = 3  # 文件处理间隔（秒）
MAX_RETRIES = 60  # 最大重试次数（5分钟）

# 输出设置
OUTPUT_DIR = 'extracted_texts'  # 输出目录
LOG_FILE = 'pdf_processing.log'  # 日志文件

# ==================== 配置区域结束 ====================

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_api_key():
    """
    检查API密钥是否有效
    
    Returns:
        bool: API密钥是否有效
    """
    url = f'{ALIBABA_API_BASE_URL}/api/v1/services/aigc/text-generation/generation'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ALIBABA_API_KEY}'
    }
    
    # 简单的测试请求
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": "你好"
                }
            ]
        }
    }
    
    try:
        res = requests.post(url, headers=headers, json=data, timeout=10)
        if res.status_code == 200:
            logger.info("阿里云百炼API密钥验证成功！")
            return True
        elif res.status_code == 401:
            logger.error("API密钥无效或已过期！")
            logger.error(f"请更新pdf_mineru.py中的ALIBABA_API_KEY变量。")
            return False
        else:
            logger.error(f"API密钥验证失败，状态码: {res.status_code}")
            logger.error(f"响应内容: {res.text}")
            return False
    except Exception as e:
        logger.error(f"API密钥验证时出错: {e}")
        return False

def process_pdf_with_python(file_path):
    """
    使用Python库处理PDF文件
    
    Args:
        file_path: PDF文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        logger.info(f"文件大小: {file_size_mb:.1f}MB")
        
        # 尝试使用PyPDF2提取文本
        try:
            import PyPDF2
            logger.info("使用PyPDF2提取文本...")
            
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    logger.info(f"处理第 {page_num + 1}/{len(reader.pages)} 页")
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- 第 {page_num + 1} 页 ---\n"
                        text += page_text
                        text += "\n"
                
                if text.strip():
                    logger.info(f"PDF文本提取成功，长度: {len(text)} 字符")
                    return text
                else:
                    logger.warning("PyPDF2未能提取到文本，尝试其他方法...")
                    
        except ImportError:
            logger.warning("PyPDF2未安装，尝试其他方法...")
        except Exception as e:
            logger.warning(f"PyPDF2提取失败: {e}")
        
        # 如果PyPDF2失败，尝试使用pdfplumber
        try:
            import pdfplumber
            logger.info("使用pdfplumber提取文本...")
            
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    logger.info(f"处理第 {page_num + 1}/{len(pdf.pages)} 页")
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- 第 {page_num + 1} 页 ---\n"
                        text += page_text
                        text += "\n"
            
            if text.strip():
                logger.info(f"PDF文本提取成功，长度: {len(text)} 字符")
                return text
            else:
                logger.warning("pdfplumber也未能提取到文本")
                
        except ImportError:
            logger.warning("pdfplumber未安装")
        except Exception as e:
            logger.warning(f"pdfplumber提取失败: {e}")
        
        # 如果都失败了，返回错误信息
        logger.error("所有PDF提取方法都失败了")
        return "无法提取PDF文本内容。请确保PDF文件包含可提取的文本，或者安装PyPDF2或pdfplumber库。"
            
    except Exception as e:
        logger.error(f"处理PDF文件时出错: {e}")
        return None

def save_extracted_text(file_name, text_content):
    """
    保存提取的文本内容到文件
    
    Args:
        file_name: 原始PDF文件名
        text_content: 提取的文本内容
    """
    try:
        # 创建输出目录
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 生成输出文件名
        base_name = Path(file_name).stem
        output_file = os.path.join(OUTPUT_DIR, f"{base_name}_extracted.txt")
        
        # 保存文本内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        logger.info(f"文本内容已保存到: {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"保存文本内容时出错: {e}")
        return None





def process_pdf_file(file_name):
    """
    处理单个PDF文件的完整流程
    
    Args:
        file_name: PDF文件名
    """
    logger.info(f"开始处理PDF文件: {file_name}")
    
    # 使用Python库处理PDF
    extracted_text = process_pdf_with_python(file_name)
    if extracted_text:
        # 保存提取的文本内容
        output_file = save_extracted_text(file_name, extracted_text)
        if output_file:
            logger.info(f"PDF文件 {file_name} 处理完成")
            return True
        else:
            logger.error(f"保存PDF文件 {file_name} 的提取内容失败")
            return False
    else:
        logger.error(f"PDF文件 {file_name} 处理失败")
        return False

def get_pdf_files():
    """
    自动获取当前目录下的所有PDF文件
    
    Returns:
        list: PDF文件名列表
    """
    pdf_files = []
    current_dir = Path('.')
    
    for file in current_dir.glob('*.pdf'):
        pdf_files.append(file.name)
    
    return sorted(pdf_files)

def main():
    """主函数 - 批量处理所有PDF文件"""
    # 首先验证API密钥
    logger.info("正在验证API密钥...")
    if not check_api_key():
        logger.error("API密钥验证失败，程序退出。")
        return
    
    # 自动获取当前目录下的所有PDF文件
    pdf_files = get_pdf_files()
    
    if not pdf_files:
        logger.error("当前目录下没有找到PDF文件！")
        logger.error("请确保PDF文件位于脚本同一目录下。")
        return
    
    logger.info(f"找到 {len(pdf_files)} 个PDF文件:")
    for i, file_name in enumerate(pdf_files, 1):
        logger.info(f"  {i}. {file_name}")
    
    logger.info(f"开始批量处理 {len(pdf_files)} 个PDF文件...")
    
    # 逐个处理每个PDF文件
    for i, file_name in enumerate(pdf_files, 1):
        logger.info(f"\n{'='*50}")
        logger.info(f"正在处理第 {i}/{len(pdf_files)} 个文件: {file_name}")
        logger.info(f"{'='*50}")
        
        try:
            # 处理PDF文件
            success = process_pdf_file(file_name)
            if success:
                logger.info(f"文件 {file_name} 处理完成")
            else:
                logger.error(f"文件 {file_name} 处理失败")
        except Exception as e:
            logger.error(f"处理文件 {file_name} 时出错: {e}")
            continue
        
        # 在处理下一个文件前稍作等待，避免API限制
        if i < len(pdf_files):
            logger.info(f"等待{FILE_PROCESSING_INTERVAL}秒后处理下一个文件...")
            time.sleep(FILE_PROCESSING_INTERVAL)
    
    logger.info(f"\n{'='*50}")
    logger.info("所有PDF文件处理完成！")
    logger.info(f"{'='*50}")

if __name__ == "__main__":
    main()
