#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

import streamlit as st


QUESTIONS = [
    {
        "country": "Danmark",
        "answer": "København",
        "choices": ["København", "Aarhus", "Odense", "Stockholm"],
    },
    {
        "country": "Frankrig",
        "answer": "Paris",
        "choices": ["Lyon", "Marseille", "Paris", "Nice"],
    },
    {
        "country": "Tyskland",
        "answer": "Berlin",
        "choices": ["Hamborg", "Berlin", "München", "Bonn"],
    },
    {
        "country": "Spanien",
        "answer": "Madrid",
        "choices": ["Barcelona", "Valencia", "Madrid", "Sevilla"],
    },
    {
        "country": "Italien",
        "answer": "Rom",
        "choices": ["Milano", "Napoli", "Rom", "Torino"],
    },
    {
        "country": "Norge",
        "answer": "Oslo",
        "choices": ["Bergen", "Oslo", "Trondheim", "Stavanger"],
    },
    {
        "country": "Sverige",
        "answer": "Stockholm",
        "choices": ["Göteborg", "Malmö", "Uppsala", "Stockholm"],
    },
    {
        "country": "Japan",
        "answer": "Tokyo",
        "choices": ["Kyoto", "Osaka", "Tokyo", "Hiroshima"],
    },
    {
        "country": "Canada",
        "answer": "Ottawa",
        "choices": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
    },
    {
        "country": "Brasilien",
        "answer": "Brasília",
        "choices": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
    },
]


def new_question():
    st.session_state.question = random.choice(QUESTIONS)
    st.session_state.answered = False
    st.session_state.selected = None


st.set_page_config(page_title="Hovedstadsquiz", page_icon="🌍")

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    new_question()

st.title("Hovedstadsquiz")
st.write("Vælg den rigtige hovedstad.")

question = st.session_state.question

st.subheader(f"Hvad er hovedstaden i {question['country']}?")

selected = st.radio(
    "Svarmuligheder",
    question["choices"],
    index=None,
    key=f"choice_{st.session_state.total}",
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Svar", type="primary", disabled=selected is None):
        st.session_state.selected = selected
        st.session_state.answered = True
        st.session_state.total += 1

        if selected == question["answer"]:
            st.session_state.score += 1

with col2:
    if st.button("Næste spørgsmål"):
        new_question()
        st.rerun()

if st.session_state.answered:
    if st.session_state.selected == question["answer"]:
        st.success("Korrekt!")
    else:
        st.error(f"Forkert. Det rigtige svar er {question['answer']}.")

st.divider()
st.metric("Score", f"{st.session_state.score} / {st.session_state.total}")

if st.button("Nulstil quiz"):
    st.session_state.score = 0
    st.session_state.total = 0
    new_question()
    st.rerun()
