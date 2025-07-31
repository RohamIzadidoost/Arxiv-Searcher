import argparse
from arxiv_search import ArxivSearcher
import csv
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", nargs="+", required=True)
    parser.add_argument("--venues", nargs="*", help="e.g. cs.CL, cs.LG")
    parser.add_argument("--max", type=int, default=50)
    parser.add_argument("--out_csv", type=str, default="results.csv")
    parser.add_argument("--out_json", type=str, default=None)
    parser.add_argument("--download_pdf", action="store_true")
    parser.add_argument("--pdf_dir", type=str, default="pdfs")
    args = parser.parse_args()

    searcher = ArxivSearcher()
    papers = searcher.search(args.keywords, args.venues, max_results=args.max)

    if args.download_pdf:
        searcher.download_pdfs(papers, save_dir=args.pdf_dir)

    with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(papers[0].keys()))
        writer.writeheader()
        for p in papers:
            writer.writerow(p)
    print(f"{len(papers)} records saved to {args.out_csv}")

    # ذخیره JSON
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print("JSON saved to", args.out_json)

if __name__ == "__main__":
    main()