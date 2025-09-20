#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行行业政策知识库 - PDF处理管道
用于处理银行政策报告PDF文件，提取文本内容并进行结构化分析
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_processing.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PDFPipeline:
    """PDF处理管道类"""
    
    def __init__(self, pdf_dir: str = "."):
        """
        初始化PDF处理管道
        
        Args:
            pdf_dir: PDF文件所在目录
        """
        self.pdf_dir = Path(pdf_dir)
        self.pdf_files = []
        self.processed_data = {}
        
    def scan_pdf_files(self) -> List[Path]:
        """
        扫描目录中的PDF文件
        
        Returns:
            PDF文件路径列表
        """
        logger.info(f"扫描目录: {self.pdf_dir}")
        
        if not self.pdf_dir.exists():
            logger.error(f"目录不存在: {self.pdf_dir}")
            return []
            
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        self.pdf_files = pdf_files
        
        logger.info(f"找到 {len(pdf_files)} 个PDF文件")
        for pdf_file in pdf_files:
            logger.info(f"  - {pdf_file.name}")
            
        return pdf_files
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        从PDF文件中提取文本内容
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            提取的文本内容
        """
        try:
            logger.info(f"正在提取文本: {pdf_path.name}")
            
            # 尝试使用PyPDF2提取文本
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    
                    if text.strip():
                        logger.info(f"使用PyPDF2成功提取文本: {pdf_path.name}")
                        return text
                    else:
                        logger.warning(f"PyPDF2提取的文本为空: {pdf_path.name}")
            except ImportError:
                logger.warning("PyPDF2未安装，尝试使用其他方法")
            except Exception as e:
                logger.warning(f"PyPDF2提取失败: {e}")
            
            # 尝试使用pdfplumber提取文本
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    
                    if text.strip():
                        logger.info(f"使用pdfplumber成功提取文本: {pdf_path.name}")
                        return text
                    else:
                        logger.warning(f"pdfplumber提取的文本为空: {pdf_path.name}")
            except ImportError:
                logger.warning("pdfplumber未安装")
            except Exception as e:
                logger.warning(f"pdfplumber提取失败: {e}")
            
            # 如果都失败了，返回占位符
            logger.warning(f"所有PDF提取方法都失败，返回占位符: {pdf_path.name}")
            return f"从 {pdf_path.name} 提取的文本内容（需要安装PDF处理库）"
            
        except Exception as e:
            logger.error(f"提取文本失败 {pdf_path.name}: {e}")
            return ""
    
    def analyze_content(self, text: str, filename: str) -> Dict[str, Any]:
        """
        分析文本内容，提取关键信息
        
        Args:
            text: 文本内容
            filename: 文件名
            
        Returns:
            分析结果字典
        """
        logger.info(f"正在分析内容: {filename}")
        
        # 这里可以添加更复杂的文本分析逻辑
        # 比如关键词提取、主题分类、实体识别等
        
        analysis_result = {
            "filename": filename,
            "content_length": len(text),
            "keywords": [],  # 待实现关键词提取
            "summary": "",   # 待实现摘要生成
            "entities": [],  # 待实现实体识别
            "topics": []     # 待实现主题分类
        }
        
        return analysis_result
    
    def process_all_pdfs(self) -> Dict[str, Any]:
        """
        处理所有PDF文件
        
        Returns:
            处理结果字典
        """
        logger.info("开始处理所有PDF文件")
        
        # 扫描PDF文件
        pdf_files = self.scan_pdf_files()
        
        if not pdf_files:
            logger.warning("没有找到PDF文件")
            return {}
        
        # 处理每个PDF文件
        for pdf_file in pdf_files:
            try:
                # 提取文本
                text_content = self.extract_text_from_pdf(pdf_file)
                
                if text_content:
                    # 分析内容
                    analysis_result = self.analyze_content(text_content, pdf_file.name)
                    self.processed_data[pdf_file.name] = {
                        "text_content": text_content,
                        "analysis": analysis_result
                    }
                    logger.info(f"成功处理: {pdf_file.name}")
                else:
                    logger.warning(f"无法提取文本内容: {pdf_file.name}")
                    
            except Exception as e:
                logger.error(f"处理文件失败 {pdf_file.name}: {e}")
        
        logger.info(f"处理完成，共处理 {len(self.processed_data)} 个文件")
        return self.processed_data
    
    def save_results(self, output_file: str = "analysis_results.json"):
        """
        保存处理结果到文件
        
        Args:
            output_file: 输出文件名
        """
        try:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.processed_data, f, ensure_ascii=False, indent=2)
            logger.info(f"结果已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存结果失败: {e}")


def main():
    """主函数"""
    logger.info("启动银行行业政策知识库PDF处理管道")
    
    # 创建处理管道
    pipeline = PDFPipeline()
    
    # 处理所有PDF文件
    results = pipeline.process_all_pdfs()
    
    # 保存结果
    if results:
        pipeline.save_results()
        logger.info("PDF处理管道执行完成")
    else:
        logger.warning("没有处理任何PDF文件")


if __name__ == "__main__":
    main() 