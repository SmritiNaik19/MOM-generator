import google.generativeai as genai
import os
import streamlit as st


from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image

# Configure the model
key = 'AIzaSyDKCSwh-y55gWT4aTSw4aZY-xzmAORJaQM'
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')
user_text = None
st.sidebar.title(':green[Upload your MoM notes here]')
st.sidebar.subheader('Only Image,PDFs and Docx files are allowed to upload')

user_file = st.sidebar.file_uploader("Upload your file", type=['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ['image/png','image/jpg','image/jpeg']:
        user_text = extract_text_image(user_file)
    else:
        st.sidebar.write("Please upload a correctp file type")



st.title(':blue[Minutes of Meeting] : [AI assited MOM generator in a standardized format for meeting notes]')
tips = '''
* Upload your meeting notes in the form of images, PDFs or Docx files .
* Click on generate MOM button and get the minutes of meeting in a standardized format.'''
st.write(tips)

if st.button('Generate MoM'):
    if user_text is None :
        st.error('Text is not generated')

    else:
        with st.spinner('Processing your Data......'):
            prompt = ''' Assume you are an expert in creating minutes of meeting .
              User has provided you the notes of the meeting in text format. Using this data you need to create a 
              standardized minutes of meeting for the user. The data provided by user is as follows{user_text}.
              
              Keep the format strictly as mentioned below :
              title : Title of the Meeting
              Heading : Meeting Agenda
              subheading : Name of attendees ( If attendees name are not provided then keep it as Not available)
              subheading : Date and Place of the meeting(place means name of conference/meeting room ,if not provided then keep it online)
              Body : The body must follow the following sequence of points
              * Key points discussed
              * Highlight any decisions that has been finalised
              * Mention actionable items
              * Any additional notes
              * Any deadlines that has been discussed
              * Any next meeting date if discussed
              * 2 to 3 lines summary of the meeting
              * Use bullet points and highlights or bold important keywords such as  CONTEXT IS CLEAR 
              * Generate the output in such a way that it can be directly copy and pasted in a word document
              
              The data provided by user is as follows : {user_text}'''
            response = model.generate_content(prompt)
            st.write(response.text)
        
            st.download_button(label = 'Click to download',
                               data = response.text,
                               file_name = 'MoM.txt',
                               mime = 'text/plain')