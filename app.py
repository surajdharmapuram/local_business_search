import streamlit as st

import parse_query

def search():
    parse_query.parse(st.session_state.search_query)

def app():
    st.title("Local Spotlight")

    st.text_input(label="Search local stores",
                  placeholder="Search local stores",
                  label_visibility="collapsed",
                  key="search_query",
                  on_change=search)

    st.map()

if __name__ == "__main__":
    app()
