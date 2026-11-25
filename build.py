"""Cut pg_catalog.csv down to compact JSON for the browser."""
import csv, json, re, sys

src = sys.argv[1] if len(sys.argv) > 1 else "pg_catalog.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "catalog.json"

def author(a):
    # "Austen, Jane, 1775-1817; Smith, John [Editor]" -> "Jane Austen; John Smith"
    names = []
    for part in a.split(";"):
        part = re.sub(r"\[.*?\]", "", part).strip()
        part = re.sub(r",\s*(?:\d{3,4}\??|BCE?|-|\?)[\d\s?\-BCE]*$", "", part).strip(" ,")
        bits = [b.strip() for b in part.split(",")]
        if len(bits) >= 2 and bits[1]:
            part = f"{bits[1]} {bits[0]}"
        if part:
            names.append(part)
    return "; ".join(names)

rows = []
with open(src, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["Type"] != "Text":
            continue
        subj = r["Subjects"].replace(" -- ", ", ")
        shelves = "; ".join(s.replace("Category: ", "") for s in r["Bookshelves"].split("; ") if s)
        rows.append([int(r["Text#"]), " ".join(r["Title"].split()), author(r["Authors"]),
                     r["Language"], subj, shelves, r["Issued"][:4]])

rows.sort(key=lambda x: x[0])
subjects, shelves, authors, books = {}, {}, {}, []
def ref(table, text):
    return [table.setdefault(s, len(table)) for s in text.split("; ") if s]
for i, t, a, lang, subj, shelf, year in rows:
    books.append([i, t, ref(authors, a), lang, ref(subjects, subj), ref(shelves, shelf)])
with open(out, "w", encoding="utf-8") as f:
    json.dump({"authors": list(authors), "subjects": list(subjects), "shelves": list(shelves), "books": books},
              f, ensure_ascii=False, separators=(",", ":"))
print(f"{len(rows)} books -> {out}")
