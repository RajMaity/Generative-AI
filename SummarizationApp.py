## Generating the summary of the large documents(pdfs) using LLM.
## Modules used: PyPDF2 to extract contents of pdf
##               gemini-pro: LLM Model
##               Gradio for the basic UI

#Importing necessary libraries
import google.generativeai as genai
from dotenv import dotenv_values
from PyPDF2 import PdfReader
import gradio as gr

#Loading environment values
config = dotenv_values('.env')

#API Configuration
genai.configure(api_key=config['GEMINI_API_KEY'])

#Creating instance of genai
model = genai.GenerativeModel('gemini-pro')

#Extracting text-content from pdf
def textExtractor(file):
    file_path = file.name
    data_obj = open(file_path,'rb')
    pdf_reader = PdfReader(data_obj)
    num_pages = len(pdf_reader.pages)
    text = ' '
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        temp = page.extract_text()
        text = text+temp
    data_obj.close()
    return text

#Summary function
def generateSummary(file):
    text = textExtractor(file)
    #Prompt
    #You can modify and design other prompts which can generate more accurate results
    prompt = f'''Generate concise summary of the following provided text delimited by '##',\
                highlighting the important details.
                ## {text} ##
            '''
    #Getting response
    response = model.generate_content(prompt)
    return response.text   


#Gradio UI
with gr.Blocks(title="Summarization app") as demo:
    with gr.Row():
        inputFile = gr.File(label='Upload your pdf file:')
        summaryOutput = gr.Textbox(label='Generated summary:')
    with gr.Column():
        generateSummaryBtn = gr.Button(value='Generate Summary')
        clearBtn = gr.ClearButton([inputFile,summaryOutput])

    generateSummaryBtn.click(fn=generateSummary,inputs=inputFile,outputs=summaryOutput)

if __name__ == '__main__':
    demo.launch()
