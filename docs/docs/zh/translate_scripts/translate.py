import re
import os
import requests
from tqdm import tqdm
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor

from bs4 import BeautifulSoup

import logging
from logging.handlers import RotatingFileHandler


def setup_logger(
    name, log_file, level=logging.INFO, max_size=5 * 1024 * 1024, backup_count=3
):
    """
    设置一个日志记录器，打印到终端和固定大小的循环滚动日志文件。

    参数:
    name (str): 日志记录器的名称
    log_file (str): 日志文件的路径
    level (int): 日志级别，默认为 INFO
    max_size (int): 每个日志文件的最大大小（字节），默认为 5MB
    backup_count (int): 保留的日志文件数量，默认为 3

    返回:
    logging.Logger: 配置好的日志记录器
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 创建终端处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_size, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


class TqdmToLogger:
    def __init__(self, logger, level=20):  # level 20 是 INFO
        self.logger = logger
        self.level = level
        self.last_printed_len = 0

    def write(self, buf):
        if buf.strip():  # 避免空行
            self.logger.log(self.level, buf.strip())

    def flush(self):
        pass

logger = setup_logger("translator", "translator.log")
tqdm_out = TqdmToLogger(logger)


@dataclass
class TextBlock:
    """用于存储待翻译的文本块信息"""

    content: str
    original_position: int


class MarkdownTranslator:
    def __init__(self):
        """
        初始化翻译器
        """

        # 分别定义不同类型的保护模式
        self.block_protected_patterns = [
            # 代码块 - 使用非贪婪匹配
            {"name": "code_block", "pattern": r"```[\s\S]*?```"},
            # 表格 - 使用非捕获组 TODO: 优化匹配两侧不存在竖线的情况
            {
                "name": "table",
                "pattern": r"\n([^\n]*\|[^\n]*)\n([-|\s]*)\n((.*\|.*\n)*)",
            },
            # Front Matter - 匹配文件开头的YAML块
            {"name": "front_matter", "pattern": r"\A---\r?\n[\s\S]*?\r?\n---"},
            # HTML注释 - 使用非贪婪匹配
            {"name": "html_comment", "pattern": r"<!--[\s\S]*?-->"},
            # Tip和hfoption标签行
            {
                "name": "special_tags",
                "pattern": r"^(?:</?Tip|</?hfoption|</?frameworkcontent|</?jax|</?pt)[^\n]*$",
            },
        ]
        self.system_message = """Role：技术文档翻译专家

Background：你是一位资深的技术文档翻译专家，专注于网页文本和 AI 领域的英译汉翻译。

Skills & Goals：
- 准确理解并翻译技术术语和专业名词
- 提供准确、流畅的翻译，保持原文的专业性和清晰度
- 确保翻译符合技术文档的专业标准和行业规范
- 保持翻译的忠实性、准确性和连贯性
- 严格保持原文的格式结构和层级关系

Workflow：
1. 接收英文内容
2. 分析并记录原文的格式特征（包括但不限于标题层级、列表缩进、代码块等）
3. 进行翻译，确保准确性
4. 对照原文格式进行校对，确保格式完全一致
5. 审核校对翻译，确保流畅性和连贯性
6. 输出最终翻译，符合要求

注意事项：
- 将"you"统一翻译为"你"
- 严格保持标题层级，如一级标题(#)必须保持为一级标题，不得改变层级
- 保持列表的缩进层级和符号类型（有序/无序）与原文完全一致
- 保持表格或行列格式与原文一致
- 保持代码块的格式和语言标记
- 保持原文的空行和段落间距
- 只输出译文，不输出额外说明
- 不破坏原文的格式，保持原文的图片链接、超链接和行内代码不翻译，原样保留
- 对于 HTML 标签（如 <hfoptions>、<Tip>、<div> 等）：
  * 保持原样不翻译
  * 保持原有的所有属性和值不变
  * 保持标签的开闭状态，如果原文缺少闭合标签则保持不闭合
  * 不对标签进行任何格式调整或补充

任务：将英文内容翻译成中文，确保翻译符合大部分中文读者的阅读习惯和理解能力。"""

    def batch_translate(self, text_blocks: list[TextBlock]) -> list[str]:
        """
        批量翻译文本块
        Args:
            text_blocks: 待翻译的文本块列表
        Returns:
            list[str]: 翻译后的文本列表
        """
        translations = []

        for block in tqdm(
            text_blocks, total=len(text_blocks), desc="翻译", file=tqdm_out
        ):
            translated_text = self.translate_text(block.content)
            translations.append(translated_text)

        return translations

    def translate_markdown(self, input_file: str, output_file: str):
        """
        翻译整个Markdown文件
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
        """
        try:
            # 读取输入文件
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 分割内容
            parts = self.split_content(content)

            # 收集需要翻译的文本块
            text_blocks = []
            non_translatable_parts = []
            current_position = 0

            for text, needs_translation in parts:
                if needs_translation and text.strip():
                    text_blocks.append(
                        TextBlock(
                            content=text.strip(),
                            original_position=current_position,
                        )
                    )
                    non_translatable_parts.append(None)
                else:
                    text_blocks.append(None)
                    non_translatable_parts.append(text)
                current_position += 1

            translatable_blocks = [block for block in text_blocks if block is not None]

            # 批量翻译
            translations = self.batch_translate(translatable_blocks)

            for i, block in enumerate(translatable_blocks):

                assert (
                    non_translatable_parts[block.original_position] is None
                ), "待填充翻译部分不为None"

                non_translatable_parts[block.original_position] = translations[i]

            # 合并所有部分
            final_content = "\n\n".join(non_translatable_parts)

            # 写入输出文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_content)

            logger.info(f"翻译完成！输出文件: {output_file}")

        except Exception as e:
            logger.info(f"处理文件时出错: {e}")

    def translate_text(self, text: str) -> str:
        """
        使用OpenAI API翻译文本，对超长文本进行分割处理
        Args:
            text: 需要翻译的文本
        Returns:
            str: 翻译后的文本
        """
        MAX_TEXT_LENGTH = 2048

        def split_by_headers(text: str) -> list[str]:
            """按照markdown标题分割文本"""
            # 匹配各级标题的正则表达式
            header_pattern = r"^#{1,6}\s+[^\n]+$"

            if len(text) <= MAX_TEXT_LENGTH:
                return [text]

            parts = []
            current_part = []
            current_length = 0

            for line in text.split("\n"):
                line_length = len(line) + 1  # +1 为换行符

                # 如果当前行是标题且当前部分不为空，则开始新的部分
                if re.match(header_pattern, line, re.MULTILINE) and current_part:
                    if current_length > MAX_TEXT_LENGTH:
                        # 如果当前部分过长，进一步按段落分割
                        sub_parts = "\n".join(current_part).split("\n\n")
                        temp_part = []
                        temp_length = 0

                        for sub_part in sub_parts:
                            if temp_length + len(sub_part) > MAX_TEXT_LENGTH:
                                parts.append("\n\n".join(temp_part))
                                temp_part = [sub_part]
                                temp_length = len(sub_part)
                            else:
                                temp_part.append(sub_part)
                                temp_length += len(sub_part) + 2  # +2 为段落间的双换行

                        if temp_part:
                            parts.append("\n\n".join(temp_part))
                    else:
                        parts.append("\n".join(current_part))

                    current_part = [line]
                    current_length = line_length
                else:
                    current_part.append(line)
                    current_length += line_length

            # 处理最后一部分
            if current_part:
                if current_length > MAX_TEXT_LENGTH:
                    # 同样按段落分割最后一部分
                    sub_parts = "\n".join(current_part).split("\n\n")
                    temp_part = []
                    temp_length = 0

                    for sub_part in sub_parts:
                        if temp_length + len(sub_part) > MAX_TEXT_LENGTH:
                            parts.append("\n\n".join(temp_part))
                            temp_part = [sub_part]
                            temp_length = len(sub_part)
                        else:
                            temp_part.append(sub_part)
                            temp_length += len(sub_part) + 2

                    if temp_part:
                        parts.append("\n\n".join(temp_part))
                else:
                    parts.append("\n".join(current_part))

            return parts

        # 分割文本
        text_parts = split_by_headers(text)
        translated_parts = []
        url = "http://10.136.0.65:7008/v1/chat/completions"

        # 翻译每个部分
        for part in tqdm(
            text_parts, total=len(text_parts), desc="分割翻译", file=tqdm_out
        ):
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer EMPTY",
            }
            payload = {
                "model": "Qwen2.5-72B-Instruct",
                "messages": [
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": part},
                ],
                "temperature": 0.0,
            }

            max_retries = 5
            for attempt in range(max_retries):
                if attempt != 0:
                    logger.info(f"尝试第{attempt + 1}次翻译")
                try:
                    raw_response = requests.post(url, headers=headers, json=payload)
                    raw_response.raise_for_status()
                    translated_parts.append(
                        raw_response.json()["choices"][0]["message"]["content"].strip()
                    )
                    break
                except Exception as e:
                    logger.info(f"翻译出错: {e}")
                    if attempt == max_retries - 1:
                        raise RuntimeError("翻译失败")
                    continue

        # 合并翻译后的文本
        return "\n\n".join(translated_parts)

    def get_combined_pattern(self) -> str:
        """
        获取组合后的正则表达式模式
        Returns:
            str: 组合后的正则表达式模式
        """
        # 使用命名捕获组来组合模式
        patterns = [
            f'(?P<{pattern["name"]}>{pattern["pattern"]})'
            for pattern in self.block_protected_patterns
        ]
        return "|".join(patterns)

    def split_html_content(self, content: str) -> list[tuple[str, bool]]:
        """
        处理包含HTML的内容块
        """
        # 定义需要保护的Markdown字符及其HTML实体
        md_entities = {
            "&gt;": ">",  # 引用块
            "&lt;": "<",  # HTML标签
            "&amp;": "&",  # &符号
            "&quot;": '"',  # 引号
            "&apos;": "'",  # 单引号
            "&#96;": "`",  # 代码块
            "&ast;": "*",  # 强调
            "&plus;": "+",  # 列表
            "&minus;": "-",  # 列表和分隔线
            "&equals;": "=",  # 标题
            "&num;": "#",  # 标题
            "&vert;": "|",  # 表格
        }

        parts = []
        soup = BeautifulSoup(content, "html.parser")

        # 将内容转换为字符串,保持原始格式
        content_str = str(soup)

        # 还原所有被转义的Markdown字符
        for entity, char in md_entities.items():
            content_str = content_str.replace(entity, char)

        last_end = 0

        # 查找所有顶层标签
        for tag in soup.find_all(recursive=False):
            if not isinstance(tag, str) and tag.name not in {
                "tip",
                "Tip",
                "hfoption",
                "hfoptions",
                "request",
                "call",
                "response",
                "submit",
            }:
                # 将tag转换为字符串并还原Markdown字符
                tag_str = str(tag)
                for entity, char in md_entities.items():
                    tag_str = tag_str.replace(entity, char)

                start = content_str.find(tag_str, last_end)
                if start > last_end:
                    # 添加标签之前的文本(需要翻译)
                    parts.append((content_str[last_end:start], True))

                # 添加HTML标签(不需要翻译)
                parts.append((tag_str, False))
                last_end = start + len(tag_str)

        # 添加剩余的文本
        if last_end < len(content_str):
            parts.append((content_str[last_end:], True))

        return parts

    def split_content(self, content: str) -> list[tuple[str, bool]]:
        """
        将Markdown内容分割成需要翻译和不需要翻译的部分
        """
        # 首先使用正则表达式处理非HTML的部分
        pattern = self.get_combined_pattern()
        parts = []
        last_end = 0

        for match in re.finditer(pattern, content, re.MULTILINE):
            start, end = match.span()
            if start > last_end:
                # 处理这段文本中的HTML标签
                text_part = content[last_end:start]
                html_parts = self.split_html_content(text_part)
                parts.extend(html_parts)

            # 添加匹配的非HTML文本（不需要翻译）
            matched_text = match.group(0)
            parts.append((matched_text, False))
            last_end = end

        # 处理剩余的文本
        if last_end < len(content):
            remaining_text = content[last_end:]
            html_parts = self.split_html_content(remaining_text)
            parts.extend(html_parts)

        return parts

    def translate_markdown_directory(
        self, input_dir: str, output_dir: str, max_workers: int = 4
    ):
        """
        并行处理目录下的markdown文件翻译
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            max_workers: 最大进程数
        """

        os.makedirs(output_dir, exist_ok=True)

        # 获取所有 md 和 mdx 文件的列表
        md_files = []
        for ext in ["*.md", "*.mdx"]:
            md_files.extend(list(Path(input_dir).glob(f"**/{ext}")))

        # 过滤掉已存在的文件
        files_to_translate = []
        for md_file in md_files:
            rel_path = md_file.relative_to(input_dir)
            output_path = Path(output_dir) / rel_path

            if output_path.exists():
                logger.info(f"跳过已存在的文件: {rel_path}")
                continue

            os.makedirs(output_path.parent, exist_ok=True)
            # 将翻译器实例也加入到参数中
            files_to_translate.append((self, str(md_file), str(output_path)))

        # 使用进程池并行处理翻译
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            list(
                tqdm(
                    executor.map(_translate_file, files_to_translate),
                    total=len(files_to_translate),
                    desc="翻译文件",
                    file=tqdm_out,
                )
            )


def _translate_file(args):
    """辅助函数用于处理单个文件的翻译"""
    translator, input_file, output_file = args
    return translator.translate_markdown(input_file, output_file)


def main():
    # 创建翻译器实例，设置最大块大小为1024字符
    translator = MarkdownTranslator()

    # 翻译单个文件
    translator.translate_markdown(
        "README.md",
        # "diffusers/docs/source/zh/quicktour.md",
        # "assets/example.md",
        "README_ZH.md",
    )

    # 翻译整个目录
    # translator.translate_markdown_directory(
    #     "docs",
    #     "docs-zh",
    # )


if __name__ == "__main__":
    main()
