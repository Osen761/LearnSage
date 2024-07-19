from gpt_researcher import GPTResearcher
import asyncio
import markdown
import pdfkit
import os

def markdown_to_pdf(markdown_text, output_filename):
    # Convert Markdown to HTML
    html_text = markdown.markdown(markdown_text)
    
    # Combine HTML with CSS styles
    styled_html = html_text
    
    # Convert styled HTML to PDF
    pdfkit.from_string(styled_html, output_filename)

async def generate_report(query, report_type):
    """
    This is a sample script that shows how to run a research report.
    """
    # Initialize the researcher
    researcher = GPTResearcher(query=query, report_type=report_type, config_path="gpt_researcher/config.json")
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    
    return report



