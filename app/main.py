"""Streamlit UI Script
This script is the entrypoint for the streamlit text summarization app.

This file can be run inside of Docker or run locally
"""

import logging

import streamlit as st
from transformers import pipeline

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@st.cache(allow_output_mutation=True)
def load_summarizer():
    """loads the Hugging Face model"""
    # need to name the mode directly as best practice
    model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return model


def generate_chunks(inp_str: str) -> list:
    """Chunks text of input string into a list for easier processing

    Args:
        inp_str (str): text from user input

    Returns:
        list: a list of text
    """
    max_chunk = 500
    inp_str = inp_str.replace(".", ".<eos>")
    inp_str = inp_str.replace("?", "?<eos>")
    inp_str = inp_str.replace("!", "!<eos>")

    sentences = inp_str.split("<eos>")
    current_chunk = 0
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(" ")) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(" "))
            else:
                current_chunk += 1
                chunks.append(sentence.split(" "))
        else:
            chunks.append(sentence.split(" "))

    for chunk_id, _ in enumerate(chunks):
        chunks[chunk_id] = " ".join(chunks[chunk_id])
    return chunks


# Main interface code
summarizer = load_summarizer()
st.title("Text Summarization Demo")


# Side bar code
with st.sidebar:
    st.write("Maximum Number of Words")
max_len = st.sidebar.slider(
    "These are the maximum number of words to use in summary.",
    50,
    500,
    step=10,
    value=150,
)

with st.sidebar:
    st.write("Minimum Number of Words")
min_len = st.sidebar.slider(
    "These are the minimum number of words to use in summary.",
    10,
    450,
    step=10,
    value=50,
)

with st.sidebar:
    st.write("")
    st.write("The average number of words in an English sentence is 15 to 20.")
do_sample = st.sidebar.checkbox("Do sample", value=False)


# Copy and paste part
st.subheader("Paste in text")
sentence = st.text_area(
    label="",
    #    value="text inside here...",
    height=30,
    max_chars=2000,
)
button = st.button("Summarize Text")
st.caption("2000 character limit")

with st.spinner("Generating Summary..."):
    if button and sentence:
        chunks = generate_chunks(sentence)
        res = summarizer(
            chunks,
            max_length=max_len,
            min_length=min_len,
            do_sample=do_sample,
        )
        text = " ".join([summary["summary_text"] for summary in res])
        st.write(text)
