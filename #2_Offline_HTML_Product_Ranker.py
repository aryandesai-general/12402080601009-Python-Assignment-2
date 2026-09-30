"""Q2: Extract products from saved HTML pages and rank the top K.

Expected markup should contain product cards with a name, price and rating.
The parser supports common class/id names and data-* attributes; adjust selectors
in ProductParser if your supplied HTML uses a different structure.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


def number(text):
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    return float(cleaned) if cleaned else None


class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.products = []
        self.stack = []
        self.current = None
        self.capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").lower()
        ident = attrs.get("id", "").lower()
        marker = f"{classes} {ident}"
        if any(word in marker for word in ("product", "item-card", "listing")) and self.current is None:
            self.current = {"name": "", "price": None, "rating": None}
        if self.current is not None:
            if "name" in marker or "title" in marker or attrs.get("itemprop") == "name":
                self.capture = "name"
            elif "price" in marker or attrs.get("itemprop") == "price":
                value = attrs.get("content") or attrs.get("data-price")
                if value:
                    self.current["price"] = number(value)
                self.capture = "price"
            elif "rating" in marker or attrs.get("itemprop") == "ratingValue":
                value = attrs.get("content") or attrs.get("data-rating")
                if value:
                    self.current["rating"] = number(value)
                self.capture = "rating"
            if tag in {"br", "img", "meta", "input"}:
                self.capture = None

    def handle_data(self, data):
        if self.current is None or self.capture is None:
            return
        value = data.strip()
        if not value:
            return
        if self.capture == "name":
            self.current["name"] = (self.current["name"] + " " + value).strip()
        elif self.capture == "price" and self.current["price"] is None:
            self.current["price"] = number(value)
        elif self.capture == "rating" and self.current["rating"] is None:
            self.current["rating"] = number(value)

    def handle_endtag(self, tag):
        if self.current is not None and self.capture:
            self.capture = None
        # Close a product card when a likely card container closes.
        if self.current is not None and tag in {"article", "li", "div"}:
            if self.current["name"] and self.current["price"] is not None and self.current["rating"] is not None:
                self.products.append(self.current)
                self.current = None
                self.capture = None


def parse_file(path):
    parser = ProductParser()
    parser.feed(Path(path).read_text(encoding="utf-8", errors="replace"))
    if parser.current and parser.current["name"] and parser.current["price"] is not None and parser.current["rating"] is not None:
        parser.products.append(parser.current)
    return parser.products


def main():
    try:
        p, k = map(int, input().split())
        if not 1 <= p <= 5000 or not 1 <= k <= 1000:
            raise ValueError
        paths = [input().strip() for _ in range(p)]
    except ValueError:
        print("Invalid input.")
        return

    unique = {}
    for path in paths:
        try:
            products = parse_file(path)
        except OSError as exc:
            print(f"Warning: {path}: {exc}", file=sys.stderr)
            continue
        for product in products:
            name = product["name"].strip()
            if not name:
                continue
            old = unique.get(name)
            if old is None or product["rating"] > old["rating"] or (
                product["rating"] == old["rating"] and product["price"] < old["price"]
            ):
                unique[name] = product

    ranked = sorted(unique.values(), key=lambda x: (-x["rating"], x["price"], x["name"]))[:k]
    for product in ranked:
        price = int(product["price"]) if product["price"].is_integer() else product["price"]
        print(product["name"], price, product["rating"])


if __name__ == "__main__":
    main()
