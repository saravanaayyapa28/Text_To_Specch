import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# Read language dataset
try:
    df = pd.read_excel(os.path.join('language.xlsx'), sheet_name='wiki')
    df.dropna(inplace=True)
    lang = df['name'].to_list()
    langcode = df['iso'].to_list()
except Exception as e:
    st.error(f"Error reading language dataset: {e}")

# Create dictionary of language and 2-letter langcode
lang_array = {lang[i]: langcode[i] for i in range(len(lang))}

# Layout
st.title("Language-Translation + Text-To-Speech")
st.markdown("In Python 🐍 with Streamlit ! (https://www.streamlit.io/)")
inputtext = st.text_area("INPUT", height=200)

# Sidebar components
with st.sidebar:
    st.subheader('Select Language')
    #selected_lang_index = st.slider('Lang')
    #selected_lang = st.selectbox('SELECT LANGUAGE', lang)

    # Dropdown for additional language selection
    st.subheader('Additional Language Options')
    #additional_lang = st.selectbox('Select Additional Language', lang)
    selected_lang = st.selectbox('SELECT LANGUAGE', lang)

# Function to decode audio file for download
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Submit button
if st.button('Translate and Generate Audio'):
    if len(inputtext) > 0:
        try:
            # Perform translation for selected language
            output = translate(inputtext, lang_array[selected_lang])
            st.text_area("TRANSLATED TEXT", output, height=200)

            # Generate and display audio file if supported
            aud_file = gTTS(text=output, lang=lang_array[selected_lang], slow=False)
            aud_file_path = f"lang_{lang_array[selected_lang]}.mp3"
            aud_file.save(aud_file_path)
            with open(aud_file_path, 'rb') as audio_file_read:
                audio_bytes = audio_file_read.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.markdown(get_binary_file_downloader_html(aud_file_path, 'Audio File'), unsafe_allow_html=True)

        except Exception as e:
            st.error(e)
