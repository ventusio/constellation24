import streamlit as st
from chatbot import chatbot
from map import map


def main():
    st.title("Feather")

    with st.sidebar:
        chatbot()

    map()


if __name__ == "__main__":
    main()
