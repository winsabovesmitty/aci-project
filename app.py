import streamlit as st
import pandas as pd

st.title("Approach Count Index (ACI)")

df = pd.read_csv("aci.csv")

min_pitches = st.slider("Minimum Pitches Seen", 50, 1000, 200)

df = df[df["Pitches"] >= min_pitches]

df = df.sort_values("ACI", ascending=False)

st.dataframe(df, use_container_width=True)
