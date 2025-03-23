import json
import os
import streamlit as st

data_file = 'library.txt'

# Load Library Data
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save Library Data
def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

# Streamlit UI
st.title("📚 Library Management System")

library = load_library()

# 📖 Add Book
st.sidebar.header("➕ Add a New Book")
title = st.sidebar.text_input("📕 Title")
author = st.sidebar.text_input("✍️ Author")
year = st.sidebar.text_input("📅 Year")
genre = st.sidebar.text_input("🎭 Genre")
read = st.sidebar.checkbox("✅ Mark as Read")

if st.sidebar.button("📌 Add Book"):
    if title and author and year and genre:
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        library.append(new_book)
        save_library(library)
        st.sidebar.success(f'✅ Book "{title}" added successfully!')
        st.rerun()

# 🗑 Remove a Book
st.sidebar.header("🗑 Remove a Book")
remove_title = st.sidebar.text_input("🔍 Enter Title to Remove")
if st.sidebar.button("❌ Remove Book"):
    updated_library = [book for book in library if book["title"] != remove_title]
    if len(updated_library) < len(library):
        save_library(updated_library)
        st.sidebar.success(f'✅ Book "{remove_title}" removed successfully!')
        st.rerun()
    else:
        st.sidebar.error(f'⚠️ Book "{remove_title}" not found!')

# 🔎 Search a Book
st.sidebar.header("🔍 Search for a Book")
search_by = st.sidebar.radio("📌 Search By", ["Title", "Author"])
search_term = st.sidebar.text_input(f"🔎 Enter {search_by.lower()}")

if st.sidebar.button("🔍 Search"):
    results = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]
    if results:
        st.write("### 📖 Search Results")
        for book in results:
            st.write(f'📕 **{book["title"]}** by ✍️ *{book["author"]}* ({book["year"]}) - {"✅ Read" if book["read"] else "❌ Not read"}')
    else:
        st.warning("⚠️ No Book Found!")

# 📚 Display Library Collection
st.write("## 📚 Library Collection")
if library:
    for book in library:
        st.write(f'📖 **{book["title"]}** by ✍️ *{book["author"]}* ({book["year"]}) - {"✅ Read" if book["read"] else "❌ Not read"}')
else:
    st.info("ℹ️ The Library is Empty")

# 📊 Display Statistics
st.write("## 📊 Library Statistics")
total_books = len(library)
read_books = sum(1 for book in library if book["read"])
perc_read = (read_books / total_books) * 100 if total_books > 0 else 0

st.metric("📚 Total Books", total_books)
st.metric("📘 Books Read", read_books)
st.metric("📖 Percentage Read", f"{perc_read:.2f}%")

st.markdown(""" 
    <footer>
            Made with 🧡 by Maham Zafar | Powered by Python & Streamlit
    </footer>
 """, unsafe_allow_html=True)
