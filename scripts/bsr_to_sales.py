#!/usr/bin/env python3
"""Fetch public Amazon.com Best Sellers Rank (BSR) for our books and ESTIMATE sales.

No sign-in: reads public product pages only. Config: scripts/bsr_asins.tsv.
Appends one dated row per ASIN to marketing/bsr-history.csv.

ALL SALES NUMBERS ARE ESTIMATES. BSR is relative and recency-weighted; a single
sale can push a no-rank book to ~#300k-#1M for a day or two, then it decays.

Curves (US Amazon, approximate, interpolated log-log between points):
 * Print books: Kindlepreneur "Amazon Book Sales Calculator" / BSR guide
   https://kindlepreneur.com/amazon-kdp-sales-rank-calculator/ and
   TCK Publishing "Amazon Sales Rank Calculator"
   https://www.tckpublishing.com/amazon-book-sales-calculator/
 * Kindle Store: same Kindlepreneur calculator (Kindle mode) and
   Publisher Rocket's published BSR table https://publisherrocket.com/
Rough anchor points (rank -> sales/day), consistent with those tables.
sale_detected: rank appeared (none -> rank) or improved by >=40% vs last row.
"""
import csv, datetime, math, os, re, sys, time, random, urllib.request, gzip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "scripts", "bsr_asins.tsv")
OUT = os.path.join(ROOT, "marketing", "bsr-history.csv")

PRINT = [(1, 3000), (10, 1000), (100, 300), (1000, 60), (5000, 20), (10000, 12),
         (50000, 3), (100000, 1), (200000, 0.5), (500000, 0.2), (1000000, 0.07), (3000000, 0.02)]
KINDLE = [(1, 5000), (10, 2000), (100, 400), (1000, 100), (5000, 25), (10000, 15),
          (50000, 3), (100000, 1), (200000, 0.5), (500000, 0.15), (1000000, 0.05), (3000000, 0.01)]

def est_per_day(rank, fmt):
    if not rank: return 0.0
    pts = KINDLE if fmt == "kindle" else PRINT
    if rank <= pts[0][0]: return pts[0][1]
    for (r1, s1), (r2, s2) in zip(pts, pts[1:]):
        if rank <= r2:
            t = (math.log(rank) - math.log(r1)) / (math.log(r2) - math.log(r1))
            return math.exp(math.log(s1) + t * (math.log(s2) - math.log(s1)))
    return pts[-1][1]

UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"]

def fetch(asin, tries=4):
    for i in range(tries):
        req = urllib.request.Request(f"https://www.amazon.com/dp/{asin}", headers={
            "User-Agent": UAS[i % len(UAS)], "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml", "Accept-Encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                b = r.read()
                if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
                h = b.decode("utf-8", "replace")
            if "captcha" not in h.lower() and "productTitle" in h: return h
        except Exception as e:
            pass
        time.sleep(3 + random.random() * 4)
    return None

def clean(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def parse(h):
    d = {}
    m = re.search(r'id="productTitle"[^>]*>(.*?)</span>', h, re.S); d["page_title"] = clean(m.group(1)) if m else ""
    m = re.search(r"Best Sellers Rank.*?</ul>|Best Sellers Rank.*?</td>", h, re.S)
    blk = clean(m.group(0)) if m else ""
    ranks = re.findall(r"#([\d,]+) in ([^#(]+?)(?: \(|$|#)", blk + " #")
    d["bsr"] = ""; d["cat_ranks"] = []
    for n, cat in ranks:
        n = int(n.replace(",", "")); cat = cat.strip()
        if not d["bsr"] and re.match(r"(Books|Kindle Store)", cat): d["bsr"], d["bsr_cat"] = n, cat
        else: d["cat_ranks"].append(f"#{n} {cat}")
    m = re.search(r'id="acrCustomerReviewText"[^>]*>([\d,]+)', h); d["reviews"] = m.group(1).replace(",", "") if m else "0"
    m = re.search(r'class="a-offscreen">\$([\d.]+)', h); d["price"] = m.group(1) if m else ""
    d["kindle"] = "Kindle Store" in blk or "Kindle Edition" in h[:200000] and "ebooks" in h[:5000]
    return d

def last_ranks():
    res = {}
    if os.path.exists(OUT):
        for r in csv.DictReader(open(OUT)): res[r["asin"]] = r["bsr"]
    return res

def main():
    rows = list(csv.DictReader(open(CFG), delimiter="\t"))
    prev = last_ranks(); today = datetime.date.today().isoformat()
    new = not os.path.exists(OUT)
    f = open(OUT, "a", newline=""); w = csv.writer(f)
    if new: w.writerow(["date", "asin", "title", "format", "price", "bsr", "category_ranks", "reviews",
                        "est_sales_day", "est_sales_month", "sale_detected", "status"])
    for c in rows:
        h = fetch(c["asin"])
        if not h:
            w.writerow([today, c["asin"], c["title"], c["format"], "", "", "", "", "", "", "", "blocked_or_missing"])
            print(f'{c["asin"]}\tBLOCKED'); continue
        d = parse(h); fmt = c["format"]
        if fmt == "auto": fmt = "kindle" if d.get("bsr_cat") == "Kindle Store" else "print"
        title = d["page_title"] if c["title"].startswith("(") else c["title"]
        day = est_per_day(d["bsr"], fmt)
        p = prev.get(c["asin"], ""); sale = ""
        if d["bsr"] and (not p or int(d["bsr"]) <= 0.6 * int(p)): sale = "sale_detected"
        if not p and c["asin"] not in prev: sale = sale and "sale_detected(first_row_has_rank)"
        w.writerow([today, c["asin"], title, fmt, d["price"], d["bsr"], "; ".join(d["cat_ranks"]), d["reviews"],
                    f"{day:.2f}", f"{day*30:.1f}", sale, "ok"])
        print(f'{c["asin"]}\t{title[:50]}\t{fmt}\tBSR {d["bsr"] or "none"}\t~{day*30:.1f}/mo\t{sale}')
        time.sleep(2)
    f.close()

if __name__ == "__main__": main()
