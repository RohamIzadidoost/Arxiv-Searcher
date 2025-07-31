import arxiv, requests, time, os, csv

class ArxivSearcher:
    def __init__(self, delay=3.0, page_size=50):
        self.client = arxiv.Client(page_size=page_size, delay_seconds=delay)

    def build_query(self, keywords):
        return " AND ".join([f'all:"{k}"' for k in keywords])

    def search(self, keywords, venues=None, year_from=None, year_to=None, max_results=200):
        q = self.build_query(keywords)
        s = arxiv.Search(query=q, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        out = []
        for r in self.client.results(s):
            if venues and not any(v.lower() in c.lower() for c in r.categories for v in venues):
                continue
            y = r.published.year
            if (year_from and y < year_from) or (year_to and y > year_to):
                continue
            out.append(
                {
                    "paper_id": r.entry_id.split("/")[-1],
                    "title": r.title.strip().replace("\n", " "),
                    "authors": ", ".join(a.name for a in r.authors),
                    "abstract": r.summary.strip().replace("\n", " "),
                    "published": r.published.strftime("%Y-%m-%d"),
                    "year": y,
                    "pdf_url": r.pdf_url,
                    "categories": ",".join(r.categories),
                    "keywords": ", ".join(keywords),
                }
            )
            if len(out) >= max_results:
                break
        return out

    def download_pdfs(self, papers, save_dir="pdfs"):
        os.makedirs(save_dir, exist_ok=True)
        for p in papers:
            pid = p["paper_id"]
            try:
                r = next(self.client.results(arxiv.Search(id_list=[pid])))
                fn = os.path.join(save_dir, f"{pid}.pdf")
                r.download_pdf(dirpath=save_dir, filename=os.path.basename(fn))
                p["pdf_file"] = fn
            except Exception:
                p["pdf_file"] = ""
            time.sleep(self.client.delay_seconds)

    def _bib(self, pid):
        return requests.get(
            f"https://arxiv.org/bibtex/{pid}",
            headers={"User-Agent": "ArxivSearcher"},
            timeout=15,
        ).text.strip()

    def download_bibtex(self, papers, save_dir="bibs"):
        os.makedirs(save_dir, exist_ok=True)
        for p in papers:
            pid = p["paper_id"]
            try:
                bib = self._bib(pid)
                fn = os.path.join(save_dir, f"{pid}.bib")
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(bib + "\n")
                p["bib_file"] = fn
                p["bibtex"] = bib
            except Exception:
                p["bib_file"] = ""
                p["bibtex"] = ""
            time.sleep(self.client.delay_seconds)

    def save_csv(self, papers, fname="papers.csv"):
        if not papers:
            return
        cols = [
            "paper_id",
            "title",
            "authors",
            "abstract",
            "published",
            "year",
            "pdf_url",
            "categories",
            "keywords",
            "bibtex",
        ]
        with open(fname, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for p in papers:
                w.writerow({k: p.get(k, "") for k in cols})


if __name__ == "__main__":
    s = ArxivSearcher()
    papers = s.search(["transformer", "speech"], year_from=2023)
    s.download_pdfs(papers)
    s.download_bibtex(papers)
    s.save_csv(papers)
