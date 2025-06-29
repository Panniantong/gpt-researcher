import aiofiles
import urllib
import mistune

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)

    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')

    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)

async def write_text_to_md(text: str, filename: str = "") -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.

    Returns:
        str: The file path of the generated Markdown file.
    """
    # 检查内容是否为错误报告
    error_keywords = ["报告生成失败", "响应生成失败", "Error in generate_report", "API连接中断"]
    is_error_report = any(keyword in text for keyword in error_keywords)
    
    # 检查输入内容是否为空或太短（小于100字符可能是错误）
    if not text or text.strip() == "" or len(text.strip()) < 100 or is_error_report:
        print(f"Report content is empty or appears to be an error report (length: {len(text.strip())}). Not generating MD file.")
        # 不生成文件，返回空路径
        return ""

    file_path = f"outputs/{filename[:60]}.md"
    await write_to_file(file_path, text)
    return urllib.parse.quote(file_path)

async def write_md_to_pdf(text: str, filename: str = "") -> str:
    """Converts Markdown text to a PDF file and returns the file path.
    If PDF generation is disabled or fails, falls back to creating a Markdown file.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated PDF or Markdown file.
    """
    import os

    # 检查内容是否为错误报告
    error_keywords = ["报告生成失败", "响应生成失败", "Error in generate_report", "API连接中断"]
    is_error_report = any(keyword in text for keyword in error_keywords)
    
    # 检查输入内容是否为空或太短（小于100字符可能是错误）
    if not text or text.strip() == "" or len(text.strip()) < 100 or is_error_report:
        print(f"Report content is empty or appears to be an error report (length: {len(text.strip())}). Not generating PDF file.")
        # 不生成文件，返回空路径
        return ""

    file_path = f"outputs/{filename[:60]}.pdf"
    fallback_path = f"outputs/{filename[:60]}.md"

    # Check if PDF generation is enabled
    enable_pdf = os.getenv('ENABLE_PDF_GENERATION', 'true').lower() == 'true'

    if not enable_pdf:
        print("PDF generation is disabled. Creating Markdown file instead...")
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Report written to {fallback_path}")
            encoded_file_path = urllib.parse.quote(fallback_path)
            return encoded_file_path
        except Exception as fallback_error:
            print(f"Error in creating Markdown file: {fallback_error}")
            return ""

    try:
        from md2pdf.core import md2pdf
        md2pdf(file_path,
               md_content=text,
               # md_file_path=f"{file_path}.md",
               css_file_path="./frontend/pdf_styles.css",
               base_url=None)
        print(f"Report written to {file_path}")
        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        print(f"Falling back to Markdown format...")

        # Fallback: save as Markdown file
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Report written to {fallback_path}")
            encoded_file_path = urllib.parse.quote(fallback_path)
            return encoded_file_path
        except Exception as fallback_error:
            print(f"Error in creating Markdown file: {fallback_error}")
            return ""

async def write_md_to_word(text: str, filename: str = "") -> str:
    """Converts Markdown text to a DOCX file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated DOCX.
    """
    # 检查内容是否为错误报告
    error_keywords = ["报告生成失败", "响应生成失败", "Error in generate_report", "API连接中断"]
    is_error_report = any(keyword in text for keyword in error_keywords)
    
    # 检查输入内容是否为空或太短（小于100字符可能是错误）
    if not text or text.strip() == "" or len(text.strip()) < 100 or is_error_report:
        print(f"Report content is empty or appears to be an error report (length: {len(text.strip())}). Not generating DOCX file.")
        # 不生成文件，返回空路径
        return ""
    
    file_path = f"outputs/{filename[:60]}.docx"

    try:
        from docx import Document
        from htmldocx import HtmlToDocx
        # Convert report markdown to HTML
        html = mistune.html(text)
        # Create a document object
        doc = Document()
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)

        # Saving the docx document to file_path
        doc.save(file_path)

        print(f"Report written to {file_path}")

        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path

    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""