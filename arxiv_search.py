import arxiv
import time
import os

class ArxivSearcher:
    def __init__(self, delay=3.0):
        self.client = arxiv.Client(page_size=50, delay_seconds=delay)

    def build_query(self, keywords):
        terms = [f'all:"{kw}"' for kw in keywords]
        return " AND ".join(terms)

    def search(self, keywords, venues=None, max_results=100):
        query = self.build_query(keywords)
        search = arxiv.Search(query=query, max_results=max_results,
                              sort_by=arxiv.SortCriterion.Relevance)
        results = []
        for r in self.client.results(search):
            cats = r.categories
            if venues and not any(v.lower() in cat.lower() for cat in cats for v in venues):
                continue
            papers = {
                "paper_id": r.entry_id.split("/")[-1],
                "title": r.title.strip().replace("\n", " "),
                "authors": ", ".join(a.name for a in r.authors),
                "abstract": r.summary.strip().replace("\n", " ")[:500],
                "published": r.published.strftime("%Y-%m-%d"),
                "pdf_url": r.pdf_url
            }
            results.append(papers)
            if len(results) >= max_results:
                break
        return results

    def download_pdfs(self, papers, save_dir="pdfs"):
        os.makedirs(save_dir, exist_ok=True)
        for p in papers:
            paper_id = p["paper_id"] 
            try:
                result = next(self.client.results(arxiv.Search(id_list=[paper_id])))
                fname = os.path.join(save_dir, f"{paper_id}.pdf")
                result.download_pdf(dirpath=save_dir, filename=os.path.basename(fname))
                p["downloaded_pdf"] = fname
            except Exception as e:
                p["downloaded_pdf"] = ""
                print("Download Error:", paper_id, e)
            time.sleep(self.client.delay_seconds)