import aiofiles
import urllib
import uuid
import mistune
import os

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')

    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)


async def write_text_to_md(text: str, path: str) -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.

    Returns:
        str: The file path of the generated Markdown file.
    """
    task = uuid.uuid4().hex
    file_path = f"{path}/{task}.md"
    await write_to_file(file_path, text)
    print(f"Report written to {file_path}")
    return file_path


async def write_md_to_pdf(text: str, path: str) -> str:
    """Converts Markdown text to a PDF file and returns the file path.
    If PDF generation is disabled or fails, falls back to creating a Markdown file.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated PDF or Markdown file.
    """
    task = uuid.uuid4().hex
    file_path = f"{path}/{task}.pdf"
    fallback_path = f"{path}/{task}.md"

    # Check if PDF generation is enabled
    enable_pdf = os.getenv('ENABLE_PDF_GENERATION', 'true').lower() == 'true'

    if not enable_pdf:
        print("PDF generation is disabled. Creating Markdown file instead...")
        try:
            await write_to_file(fallback_path, text)
            print(f"Report written to {fallback_path}")
            encoded_file_path = urllib.parse.quote(fallback_path)
            return encoded_file_path
        except Exception as fallback_error:
            print(f"Error in creating Markdown file: {fallback_error}")
            return ""

    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, "pdf_styles.css")

        # Moved imports to inner function to avoid known import errors with gobject-2.0
        from md2pdf.core import md2pdf
        md2pdf(file_path,
               md_content=text,
               css_file_path=css_path,
               base_url=None)
        print(f"Report written to {file_path}")
        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        print(f"Falling back to Markdown format...")

        # Fallback: save as Markdown file
        try:
            await write_to_file(fallback_path, text)
            print(f"Report written to {fallback_path}")
            encoded_file_path = urllib.parse.quote(fallback_path)
            return encoded_file_path
        except Exception as fallback_error:
            print(f"Error in creating Markdown file: {fallback_error}")
            return ""


async def write_md_to_word(text: str, path: str) -> str:
    """Converts Markdown text to a DOCX file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated DOCX.
    """
    task = uuid.uuid4().hex
    file_path = f"{path}/{task}.docx"

    try:
        from htmldocx import HtmlToDocx
        from docx import Document
        # Convert report markdown to HTML
        html = mistune.html(text)
        # Create a document object
        doc = Document()
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)

        # Saving the docx document to file_path
        doc.save(file_path)

        print(f"Report written to {file_path}")

        encoded_file_path = urllib.parse.quote(f"{file_path}.docx")
        return encoded_file_path

    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""
