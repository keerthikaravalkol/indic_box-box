import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Indic box-box Admin", layout="wide")
st.title("📊 F1 Submissions Dashboard")

conn = sqlite3.connect("f1_data.db")
df = pd.read_sql_query("SELECT * FROM submissions ORDER BY timestamp DESC", conn)
conn.close()

if df.empty:
    st.warning("No submissions yet.")
    st.stop()

# Summary
st.markdown(f"✅ Total Submissions: **{len(df)}**")

with st.expander("🔤 Submissions by Language"):
    st.write(df['language'].value_counts())

with st.expander("🏷️ Submissions by Category"):
    st.write(df['category'].value_counts())

# Display Table
st.dataframe(df, use_container_width=True)

# CSV Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name="f1_submissions.csv", mime="text/csv")

# Audio Playback
if "audio_path" in df.columns:
    st.subheader("🎧 Audio Previews")
    for i, row in df.iterrows():
        if row['audio_path'] and os.path.exists(row['audio_path']):
            st.write(f"🧑 {row['name']} | 🏁 {row['category']} | 🕒 {row['timestamp']}")
            audio_bytes = open(row['audio_path'], "rb").read()
            st.audio(audio_bytes)
