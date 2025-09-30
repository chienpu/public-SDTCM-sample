import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/"
TOC_URL = urljoin(BASE, "toc.html")

# === 行為開關 ===
LIMIT = 0                 # 0=全部；測試可設 20/50
ONLY_ENTITY = True        # 只輸出 ENTITY；若要全類型設為 False
SLEEP_BETWEEN = 0.10      # 請求間隔，避免觸發限制
MAX_RETRIES = 3

# 一些常見的表頭別名（統一為 name/type/desc）
HDR_ALIASES = {
    "name": {"name", "attribute", "attr", "parameter"},
    "type": {"type", "data type", "datatype"},
    "desc": {"description", "desc", "definition", "remarks", "note"}
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (IFC4x3 schema extractor; +https://buildingsmart.org)"
}

def get_url(url, ok_status=(200,), retries=MAX_RETRIES):
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code in ok_status:
                return r
            else:
                print(f"  ⚠️ HTTP {r.status_code} for {url}")
        except Exception as e:
            print(f"  ⚠️ Error {e} for {url}")
        time.sleep(0.5 + i*0.5)
    raise RuntimeError(f"Failed to fetch after {retries} retries: {url}")

def classify_page(soup):
    """
    依據 EXPRESS 區塊內容判定頁面類別：ENTITY / TYPE / ENUM / SELECT / UNKNOWN
    """
    # 常見：在 <pre> 或 <code> 中會出現 'ENTITY IfcX' / 'TYPE IfcX = SELECT/ENUMERATION OF/…'
    text_blobs = []
    for tag in soup.find_all(["pre", "code"]):
        text_blobs.append(tag.get_text(" ", strip=True))
    blob = " ".join(text_blobs).upper()

    if " ENTITY " in blob:
        return "ENTITY"
    if " TYPE " in blob:
        if " ENUMERATION OF " in blob:
            return "ENUM"
        if " SELECT " in blob:
            return "SELECT"
        return "TYPE"

    # 備援：找頁面段落
    page_txt = soup.get_text(" ", strip=True).upper()
    if "ENTITY" in page_txt:
        return "ENTITY"  # 假設
    return "UNKNOWN"

def normalize_header(h):
    h = h.strip().lower()
    for k, aliases in HDR_ALIASES.items():
        if h in aliases:
            return k
    return h

def parse_attributes_from_tables(soup):
    """
    嘗試從各種表格樣式抽出屬性列
    回傳 list(dict(name,type,desc))
    """
    out = []
    for tbl in soup.find_all("table"):
        # 擷取表頭
        headers = [normalize_header(th.get_text(" ", strip=True)) for th in tbl.find_all("th")]
        if not headers:
            continue
        # 至少要包含 name 與 type 其一
        if not (("name" in headers) or ("type" in headers)):
            continue

        # 找出欄位索引
        try:
            idx_name = headers.index("name")
        except ValueError:
            idx_name = None
        try:
            idx_type = headers.index("type")
        except ValueError:
            idx_type = None
        # 描述欄可能叫不同名字，挑一個最像的
        idx_desc = None
        for key in ("desc", "description", "definition", "remarks", "note"):
            if key in headers:
                idx_desc = headers.index(key)
                break

        # 逐列取值
        for tr in tbl.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            if len(cells) < 2:
                continue
            name_val = cells[idx_name] if idx_name is not None and idx_name < len(cells) else ""
            type_val = cells[idx_type] if idx_type is not None and idx_type < len(cells) else ""
            desc_val = cells[idx_desc] if idx_desc is not None and idx_desc < len(cells) else ""
            # 過濾掉表頭或空白列
            if name_val and name_val.lower() not in {"name", "attribute", "attr"}:
                out.append({"name": name_val, "type": type_val, "desc": desc_val})
    return out

def parse_definition(soup):
    # 優先抓 .definition；否則抓第一個段落備援
    def_div = soup.find("div", {"class": "definition"})
    if def_div:
        return def_div.get_text(" ", strip=True)
    p = soup.find("p")
    return p.get_text(" ", strip=True) if p else ""

def main():
    print(f"📑 Scanning TOC: {TOC_URL}")
    toc = get_url(TOC_URL)
    toc_soup = BeautifulSoup(toc.text, "lxml")

    # 1) 找所有 content.html 模組頁
    module_pages = []
    for a in toc_soup.select("a[href]"):
        href = a["href"]
        if href.endswith("content.html"):
            full = urljoin(BASE, href)
            if full not in module_pages:
                module_pages.append(full)
    print("📑 Found schema modules:", len(module_pages))
    print("👉 First 5 modules:", module_pages[:5])

    # 2) 在每個模組頁找 lexical/Ifc*.htm 連結
    entity_links = []
    for page in module_pages:
        print(f"🔎 Scanning {page}")
        try:
            mod = get_url(page)
        except Exception as e:
            print(f"  ⚠️ Skip module {page}: {e}")
            continue
        soup = BeautifulSoup(mod.text, "lxml")

        # 關鍵：不限定在 <td>，直接抓任何含 lexical/Ifc 的連結
        for a in soup.select('a[href*="lexical/Ifc"]'):
            text = a.get_text(" ", strip=True)
            href = a.get("href")
            if not text:
                # 有些頁面連結的文字不是名稱，從 href 取
                m = re.search(r"lexical/(ifc[^./]+)\.htm", href, re.I)
                text = m.group(1) if m else ""
            if text and text.startswith("Ifc"):
                full = urljoin(BASE, href)
                entity_links.append((text, full))
        time.sleep(SLEEP_BETWEEN)

    # 去重
    seen = set()
    entity_links = [(n, u) for (n, u) in entity_links if (n, u) not in seen and not seen.add((n, u))]
    print("🔢 Found total lexical pages:", len(entity_links))
    print("👉 First 10:", entity_links[:10])

    # 可先限制數量測試
    links_to_fetch = entity_links if LIMIT == 0 else entity_links[:LIMIT]

    # 3) 逐頁解析
    rows = []
    kept = 0
    for name, url in links_to_fetch:
        try:
            r = get_url(url)
            soup = BeautifulSoup(r.text, "lxml")
            kind = classify_page(soup)
            if ONLY_ENTITY and kind != "ENTITY":
                # 略過 TYPE/ENUM/SELECT
                continue

            definition = parse_definition(soup)
            attrs = parse_attributes_from_tables(soup)
            kept += 1
            print(f"✅ [{kind}] {name} — {len(attrs)} attributes")

            if attrs:
                for a in attrs:
                    rows.append({
                        "Entity": name,
                        "Kind": kind,
                        "Definition": definition,
                        "Attr_Name": a["name"],
                        "Attr_Type": a["type"],
                        "Attr_Desc": a["desc"],
                        "Source": url
                    })
            else:
                # 沒有屬性也保留一列（Definition 仍然有用）
                rows.append({
                    "Entity": name,
                    "Kind": kind,
                    "Definition": definition,
                    "Attr_Name": "",
                    "Attr_Type": "",
                    "Attr_Desc": "",
                    "Source": url
                })
        except Exception as e:
            print(f"  ❌ Error parsing {name} -> {e}")
        time.sleep(SLEEP_BETWEEN)

    # 4) 輸出 CSV
    out = "IFC4x3_full_schema.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Entity", "Kind", "Definition", "Attr_Name", "Attr_Type", "Attr_Desc", "Source"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"🎉 Exported {len(rows)} rows from {kept} pages to {out}")

if __name__ == "__main__":
    main()
