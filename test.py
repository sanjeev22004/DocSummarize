import streamlit as st
import os
from utils import *
def main():
    st.set_page_config(page_title="pdf summarizer")
    st.title("pdf_summarizer_app.")
    st.write("summarize your pdf here")
    st.divider()
    pdf=st.file_uploader('upload your document here',type='pdf')
    submit=st.button("generate summary")

    os.environ['api_key']=""

    if submit:
        response=summarizer(pdf)
        st.subheader('summary of file:')
        st.write(response)
if __name__ == '__main__':
   main() 