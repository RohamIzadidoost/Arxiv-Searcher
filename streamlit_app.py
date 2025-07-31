"""
Run with:  streamlit run streamlit_app.py
"""
from datetime import datetime
import io
import os
import zipfile
import streamlit as st
from arxiv_search import ArxivSearcher   

st.sidebar.title("🔍 Arxiv Searcher")
keywords = st.sidebar.text_input(
    "Keywords (comma-separated)",
    placeholder="e.g. LLm, RL"
)
venues   = st.sidebar.text_input(
    "arXiv categories / venues (comma-separated)",
    placeholder="e.g. cs.LG, stat.ML"
)

col1, col2 = st.sidebar.columns(2)
year_from = col1.number_input("Year from", value=2022, min_value=1992)
year_to   = col2.number_input("Year to",   value=datetime.now().year)

max_results = st.sidebar.slider("Max results", min_value=1, max_value=50, value=10)
pdf_dl      = st.sidebar.checkbox("⬇ Download PDFs", value=False)
bib_dl      = st.sidebar.checkbox("⬇ Download BibTeX", value=True)

search_btn  = st.sidebar.button("Search arXiv")
st.title("📚 arXiv Explorer")

if search_btn:
    if not keywords.strip():
        st.warning("Please enter at least one keyword.")
        st.stop()

    searcher = ArxivSearcher(delay=2.0) 

    kw_list   = [k.strip() for k in keywords.split(",") if k.strip()]
    venue_lst = [v.strip() for v in venues.split(",") if v.strip()] or None

    with st.spinner("Querying arXiv …"):
        papers = searcher.search(
            keywords=kw_list,
            venues=venue_lst,
            year_from=year_from,
            year_to=year_to,
            max_results=max_results
        )
        searcher.save_csv(papers, "arxiv_results.csv")

    if not papers:
        st.info("No papers matched your query.")
        st.stop()

    st.success(f"Found {len(papers)} papers")

    if pdf_dl:
        with st.spinner("Downloading PDFs …"):
            searcher.download_pdfs(papers)

    if bib_dl:
        with st.spinner("Downloading BibTeX …"):
            searcher.download_bibtex(papers)

    for p in papers:
        with st.expander(f"**{p['title']}**"):
            st.write(f"**Authors:** {p['authors']}")
            st.write(f"**Published:** {p['published']}")
            st.write("**Abstract:**")
            st.write(p["abstract"])
            colA, colB = st.columns(2)
            colA.markdown(f"[PDF]({p['pdf_url']})")
            if p.get("bibtex_file"):
                with open(p["bibtex_file"], "r", encoding="utf-8") as f:
                    colB.download_button(
                        label="Download BibTeX",
                        data=f.read(),
                        file_name=os.path.basename(p["bibtex_file"]),
                        mime="text/plain"
                    )

    if pdf_dl or bib_dl:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as z:
            for p in papers:
                for k in ("downloaded_pdf", "bibtex_file"):
                    fpath = p.get(k, "")
                    if fpath and os.path.exists(fpath):
                        z.write(fpath, arcname=os.path.basename(fpath))
        if zip_buffer.getbuffer().nbytes:
            st.download_button(
                label="Download all (zip)",
                data=zip_buffer.getvalue(),
                file_name="arxiv_results.zip",
                mime="application/zip"
            )
