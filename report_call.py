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

if __name__ == "__main__":
    # User input for query
    query = input("Enter your research query: ")
    
    # Selection for report type
    report_type = input("Select report type (research_report, summary, detailed_analysis): ")
    
    # Run the main function asynchronously and generate the report
    report = asyncio.run(generate_report(query, report_type))
    print('Report generated successfully!')
    
    # Convert the report to PDF
    pdf_filename = "research_report.pdf"
    markdown_to_pdf(report, pdf_filename)
    
    # Display the report in the console
    print('Research Report:')
    print(report)
    
    # Inform the user that the report is saved as a PDF
    print(f'Research report saved as {pdf_filename}.')

