python cli.py --keywords "game theory" LLM RL \
    --venues cs.CL cs.LG cs.AI \
    --max 50 \
    --out_csv nlp_arxiv.csv \
    --out_json nlp_arxiv.json \
    --download_pdf \
    --pdf_dir downloaded_pdfs

<div align="center">

# 🛰️ Arxiv-Searcher

**Search, filter & download arXiv papers from the comfort of your terminal _or_ a sleek Streamlit web UI.**

[![Streamlit App](https://img.shields.io/badge/Live-Demo-Open-▶️-brightgreen)](#) <!-- replace # with deployed URL -->
[![Licence](https://img.shields.io/github/license/yourname/Arxiv-Searcher)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/python-arxiv)](https://pypi.org/project/python-arxiv/)

</div>

---

## ✨ Features

| CLI / API                                | Streamlit GUI                       |
|------------------------------------------|-------------------------------------|
| 🔎 Keyword AND/OR search (title, abstr.) | 🖱️ Point-&-click sidebar controls   |
| 🗂️ Category & year filters               | 📊 Progressive results accordion    |
| 📄 BibTeX & PDF downloader               | ⬇ One-click ZIP of all assets       |
| 🛑 Respectful rate-limiting              | 🚦 Inline spinners & status badges   |
| 🦾 Typed, documented Python API          | ☁️ Ready for **Streamlit Cloud**     |

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/YOURNAME/Arxiv-Searcher.git
cd Arxiv-Searcher
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
