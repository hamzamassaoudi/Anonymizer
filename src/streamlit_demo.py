import streamlit as st
from annotated_text import annotated_text
import spacy
from util import LOGO

@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_spacy_model():
    return spacy.load("fr_core_news_md")

colors = {"Person":"#faa",
          "Location":"#fda",
          "Organization":"#afa"}

def process_text(doc, selected_entities, anonymize=False):
    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append((token.text, "Person", colors["Person"]))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append((token.text, "Location", colors["Location"]))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append((token.text, "Organization", colors["Organization"]))
        else:
            tokens.append(" " + token.text + " ")

    if anonymize:
        anonmized_tokens = []
        for token in tokens:
            if type(token) == tuple:
                anonmized_tokens.append(("X" * len(token[0]), token[1], token[2]))
            else:
                anonmized_tokens.append(token)
        return anonmized_tokens

    return tokens



nlp_fr_lg = load_spacy_model()

st.title("DILA Anonymizer")
st.sidebar.markdown(LOGO, unsafe_allow_html=True)
st.header('Input text')
user_input = st.text_area("Type a text to anonymize", "", height=250)
selected_entities = st.sidebar.multiselect(
    "Select the entities you want to detect",
    options=["LOC", "PER", "ORG"],
    default=["LOC", "PER", "ORG"],
)

anonymize = st.checkbox("Anonymize")
doc = nlp_fr_lg(user_input)
tokens = process_text(doc, selected_entities, anonymize=anonymize)
annotated_text(*tokens)
