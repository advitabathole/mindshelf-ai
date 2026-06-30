import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(
    page_title="MindShelf AI",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "books.csv"

# ---------- Helpers ----------
def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "Date Added", "Title", "Author", "Status", "Rating", "Notes"
    ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_book(title, author, status, rating, notes):
    df = load_data()
    new_book = {
        "Date Added": date.today().isoformat(),
        "Title": title,
        "Author": author,
        "Status": status,
        "Rating": rating,
        "Notes": notes
    }
    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    save_data(df)

def generate_reflection(notes):
    if not notes.strip():
        return "Add some notes first. Even AI needs material, sadly."

    return f"""
### AI Reflection

Based on your notes, here are some useful takeaways:

**Main idea:**  
Your notes suggest this book has themes worth connecting to your own goals, decisions, or habits.

**Reflection questions:**
1. What is one idea from this book you could apply this week?
2. Did this book change how you think about discipline, relationships, work, or identity?
3. What quote or idea would you want to remember 6 months from now?

**Action step:**  
Turn one insight from your notes into a small behavior you can actually do. Not a dramatic life transformation montage. One behavior.
"""

# ---------- Styling ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}
.metric-card {
    padding: 20px;
    border-radius: 15px;
    background-color: #f5f5f5;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<p class="main-title">📚 MindShelf AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track your books, notes, ratings, and reflections in one clean dashboard.</p>', unsafe_allow_html=True)

df = load_data()

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Book", "📖 Library", "📊 Dashboard", "🧠 AI Reflection"
])

# ---------- Add Book ----------
with tab1:
    st.header("Add a Book")

    with st.form("book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        status = st.selectbox("Status", ["Want to Read", "Reading", "Finished"])
        rating = st.slider("Rating", 0, 5, 0)
        notes = st.text_area("Notes", height=150)

        submitted = st.form_submit_button("Save Book")

        if submitted:
            if title.strip() == "":
                st.error("Title is required. The book does need a name, tragically.")
            else:
                add_book(title, author, status, rating, notes)
                st.success("Book saved successfully!")
                st.rerun()

# ---------- Library ----------
with tab2:
    st.header("Your Library")

    if df.empty:
        st.info("No books added yet.")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("Delete a Book")
        book_to_delete = st.selectbox("Choose a book to delete", df["Title"].tolist())

        if st.button("Delete Selected Book"):
            df = df[df["Title"] != book_to_delete]
            save_data(df)
            st.success(f"Deleted '{book_to_delete}'")
            st.rerun()

# ---------- Dashboard ----------
with tab3:
    st.header("Reading Dashboard")

    total_books = len(df)
    finished_books = len(df[df["Status"] == "Finished"]) if not df.empty else 0
    currently_reading = len(df[df["Status"] == "Reading"]) if not df.empty else 0

    rated_books = df[df["Rating"] > 0] if not df.empty else pd.DataFrame()
    avg_rating = round(rated_books["Rating"].mean(), 2) if not rated_books.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Books", total_books)
    col2.metric("Finished", finished_books)
    col3.metric("Currently Reading", currently_reading)
    col4.metric("Average Rating", avg_rating)

    if not df.empty:
        st.subheader("Books by Status")
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)

# ---------- AI Reflection ----------
with tab4:
    st.header("AI Reflection Helper")

    st.write("Paste your book notes below and get reflection questions.")

    reflection_notes = st.text_area("Paste notes here", height=200)

    if st.button("Generate Reflection"):
        response = generate_reflection(reflection_notes)
        st.markdown(response)