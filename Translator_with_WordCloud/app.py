import streamlit as st
from gtts import gTTS
import os
from langdetect import detect, lang_detect_exception
from deep_translator import GoogleTranslator
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data
nltk.download("punkt")
nltk.download("words")

# -------------------------------
# Read Aloud Function
# -------------------------------
def read_aloud(text, language="en"):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("temp.mp3")
        os.system("start temp.mp3")
    except Exception as e:
        st.error(f"Speech Error: {e}")

# -------------------------------
# WordCloud Function
# -------------------------------
def generate_wordcloud(text):

    english_words = set(nltk.corpus.words.words())

    words = word_tokenize(text)

    english_words_in_text = [
        word for word in words if word.lower() in english_words
    ]

    english_text = " ".join(english_words_in_text)

    if english_text.strip() == "":
        english_text = text

    wordcloud = WordCloud(
        width=900,
        height=500,
        background_color="white"
    ).generate(english_text)

    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Globalize",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Globalize - Language Translator with Word Cloud")

# -------------------------------
# Background CSS (Optional)
# -------------------------------
if os.path.exists("back.jpg"):
    st.markdown(
        """
        <style>
        .stApp{
            background-image:url("back.jpg");
            background-size:cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    paragraph = st.text_area(
        "Enter Paragraph",
        height=250
    )

with col2:

    all_languages = sorted(
        [
            lang.name
            for lang in pycountry.languages
            if hasattr(lang, "alpha_2")
        ]
    )

    target_languages_input = st.multiselect(
        "Select Languages",
        all_languages
    )

# -------------------------------
# Read Aloud
# -------------------------------
if st.button("🔊 Read Aloud"):

    if paragraph.strip():

        try:
            detected = detect(paragraph)
        except:
            detected = "en"

        read_aloud(paragraph, detected)

# -------------------------------
# Detect Language
# -------------------------------
paragraph_language = "en"

translated_paragraph = paragraph

if paragraph.strip():

    try:

        paragraph_language = detect(paragraph)

        language_name = pycountry.languages.get(
            alpha_2=paragraph_language
        )

        if language_name:
            st.success(f"Detected Language : {language_name.name}")
        else:
            st.success(f"Detected Language Code : {paragraph_language}")

    except lang_detect_exception.LangDetectException:
        st.error("Unable to detect language.")

# -------------------------------
# Translate to English
# -------------------------------
if paragraph.strip():

    try:

        if paragraph_language != "en":

            translated_paragraph = GoogleTranslator(
                source="auto",
                target="en"
            ).translate(paragraph)

            st.subheader("Universal Language (English)")

            st.write(translated_paragraph)

        else:

            translated_paragraph = paragraph

    except Exception as e:

        st.error(f"Translation Error : {e}")

# -------------------------------
# Word Cloud
# -------------------------------
if translated_paragraph.strip():

    try:

        fig = generate_wordcloud(translated_paragraph)

        st.sidebar.header("Word Cloud")

        st.sidebar.pyplot(fig)

    except Exception as e:

        st.error(e)

# -------------------------------
# Translate to Multiple Languages
# -------------------------------
if st.button("🌍 Translate & Read Aloud"):

    if paragraph.strip() == "":

        st.warning("Please enter some text.")

    else:

        for language in target_languages_input:

            try:

                lang = pycountry.languages.lookup(language)

                code = lang.alpha_2

                translated = GoogleTranslator(
                    source="auto",
                    target=code
                ).translate(paragraph)

                st.subheader(language)

                st.write(translated)

                read_aloud(translated, code)

            except Exception as e:

                st.error(f"{language}: {e}")