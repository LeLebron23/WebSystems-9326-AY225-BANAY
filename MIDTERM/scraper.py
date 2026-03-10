import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import time
import re

BASE_URL = "https://www.metacritic.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.metacritic.com/",
}

DATA_FILE = os.path.join(os.path.dirname(__file__), "games_data.json")
CSV_FILE  = os.path.join(os.path.dirname(__file__), "games_data.csv")


def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "lxml"), resp.text
            print("[scraper] HTTP " + str(resp.status_code) + " for " + url)
        except requests.RequestException as exc:
            print("[scraper] Request error (attempt " + str(attempt + 1) + "): " + str(exc))
        time.sleep(2 ** attempt)
    return None, None


def _text(soup, selector, attr=None):
    el = soup.select_one(selector)
    if el is None:
        return "Not Available"
    if attr:
        return el.get(attr, "Not Available").strip() or "Not Available"
    return el.get_text(separator=" ", strip=True) or "Not Available"


def extract_from_json_ld(raw_html):
    data = {}
    try:
        matches = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            raw_html, re.DOTALL
        )
        for match in matches:
            try:
                obj = json.loads(match.strip())
                if isinstance(obj, list):
                    obj = obj[0]
                t = obj.get("@type", "")
                if "VideoGame" in t or "Game" in t or "SoftwareApplication" in t:
                    if obj.get("name"):
                        data["title"] = obj["name"]
                    if obj.get("datePublished"):
                        data["release_date"] = obj["datePublished"]
                    if obj.get("description"):
                        data["key_features"] = obj["description"][:500]
                    if obj.get("image"):
                        img = obj["image"]
                        if isinstance(img, list): img = img[0]
                        if isinstance(img, dict): img = img.get("url", "Not Available")
                        data["image_url"] = img
                    for role in ["author", "creator", "developer"]:
                        val = obj.get(role)
                        if val:
                            if isinstance(val, list): val = val[0]
                            if isinstance(val, dict): val = val.get("name", "Not Available")
                            data["developer"] = str(val)
                            break
                    pub = obj.get("publisher")
                    if pub:
                        if isinstance(pub, list): pub = pub[0]
                        if isinstance(pub, dict): pub = pub.get("name", "Not Available")
                        data["publisher"] = str(pub)
                    genre = obj.get("genre")
                    if genre:
                        if isinstance(genre, list): genre = ", ".join(genre)
                        data["genre"] = str(genre)
                    platform = obj.get("gamePlatform") or obj.get("operatingSystem")
                    if platform:
                        if isinstance(platform, list): platform = ", ".join(platform)
                        data["platforms"] = str(platform)
                    agg = obj.get("aggregateRating")
                    if agg and isinstance(agg, dict):
                        rv = agg.get("ratingValue")
                        if rv: data["score"] = str(int(float(rv)))
            except Exception:
                continue
    except Exception:
        pass
    return data


def _find_meta(soup, label_text):
    for li in soup.select("li.c-gameDetails_listItem"):
        text = li.get_text(separator="|", strip=True)
        parts = text.split("|")
        for idx, part in enumerate(parts):
            if label_text.lower() in part.lower():
                remaining = "|".join(parts[idx+1:]).strip()
                if remaining:
                    return remaining
    for dt in soup.select("dt"):
        if label_text.lower() in dt.get_text(strip=True).lower():
            dd = dt.find_next_sibling("dd")
            if dd:
                return dd.get_text(separator=", ", strip=True)
    for li in soup.select("li.summary_detail"):
        lbl = li.select_one("span.label")
        val_el = li.select_one("span.data")
        if lbl and label_text.lower() in lbl.get_text(strip=True).lower() and val_el:
            return val_el.get_text(separator=", ", strip=True)
    return "Not Available"


def scrape_game_detail(game_url):
    soup, raw_html = fetch_page(game_url)
    if soup is None:
        return {}

    game = {
        "title":        "Not Available",
        "release_date": "Not Available",
        "key_features": "Not Available",
        "platforms":    "Not Available",
        "developer":    "Not Available",
        "publisher":    "Not Available",
        "url":          game_url,
        "score":        "Not Available",
        "genre":        "Not Available",
        "image_url":    "Not Available",
    }

    if raw_html:
        ld_data = extract_from_json_ld(raw_html)
        game.update({k: v for k, v in ld_data.items() if v})

    if game["title"] == "Not Available":
        for sel in ["h1.c-productHero_title", "h1[class*='title']", "h1"]:
            val = _text(soup, sel)
            if val != "Not Available" and len(val) < 200:
                game["title"] = val
                break

    if game["score"] == "Not Available":
        for sel in ["div.c-siteReviewScore span", "span.metascore_w", "div.c-ScoreCard span"]:
            val = _text(soup, sel)
            if val != "Not Available" and val.strip().isdigit():
                game["score"] = val.strip()
                break

    if game["image_url"] == "Not Available":
        for sel in ["img.c-productHero_imageSimple", "img.c-gameHero_image", "picture img"]:
            val = _text(soup, sel, attr="src")
            if val != "Not Available" and val.startswith("http"):
                game["image_url"] = val
                break
    if game["image_url"] == "Not Available":
        og = soup.select_one("meta[property='og:image']")
        if og:
            game["image_url"] = og.get("content", "Not Available")

    if game["key_features"] == "Not Available":
        for sel in ["span.c-productDetails_description", "div.c-productDetails_description", "div.summary_deck"]:
            val = _text(soup, sel)
            if val != "Not Available" and len(val) > 20:
                game["key_features"] = val[:500]
                break
    if game["key_features"] == "Not Available":
        og_desc = soup.select_one("meta[name='description'], meta[property='og:description']")
        if og_desc:
            content = og_desc.get("content", "")
            if content and len(content) > 20:
                game["key_features"] = content[:500]

    if game["release_date"] == "Not Available":
        game["release_date"] = _find_meta(soup, "Release Date")
    if game["developer"] == "Not Available":
        game["developer"] = _find_meta(soup, "Developer")
    if game["publisher"] == "Not Available":
        game["publisher"] = _find_meta(soup, "Publisher")
    if game["genre"] == "Not Available":
        game["genre"] = _find_meta(soup, "Genre")
    if game["platforms"] == "Not Available":
        game["platforms"] = _find_meta(soup, "Platform")
    if game["platforms"] == "Not Available":
        game["platforms"] = _find_meta(soup, "Platforms")

    if game["developer"] == "Not Available" and game["publisher"] != "Not Available":
        game["developer"] = game["publisher"]

    print("[scraper] Got: " + game["title"] + " | Dev: " + game["developer"] + " | Pub: " + game["publisher"])
    return game


def run_scraper(base_url=BASE_URL, limit=15):
    all_slugs = [
        "/game/elden-ring/",
        "/game/baldurs-gate-3/",
        "/game/the-legend-of-zelda-breath-of-the-wild/",
        "/game/red-dead-redemption-2/",
        "/game/grand-theft-auto-v/",
        "/game/the-witcher-3-wild-hunt/",
        "/game/god-of-war/",
        "/game/hades/",
        "/game/disco-elysium/",
        "/game/the-last-of-us/",
        "/game/cyberpunk-2077/",
        "/game/hollow-knight/",
        "/game/sekiro-shadows-die-twice/",
        "/game/death-stranding/",
        "/game/monster-hunter-world/",
        "/game/persona-5-royal/",
        "/game/batman-arkham-city/",
        "/game/portal-2/",
        "/game/bioshock/",
        "/game/dark-souls/",
        "/game/mass-effect-2/",
        "/game/the-elder-scrolls-v-skyrim/",
        "/game/god-of-war-ragnarok/",
        "/game/resident-evil-4/",
        "/game/super-mario-odyssey/",
        "/game/the-legend-of-zelda-tears-of-the-kingdom/",
        "/game/astro-bot/",
        "/game/final-fantasy-xvi/",
        "/game/spider-man-2/",
        "/game/horizon-forbidden-west/",
    ]

    game_links = [base_url.rstrip("/") + s for s in all_slugs]
    games = []
    seen_titles = set()

    for link in game_links:
        if len(games) >= limit:
            break
        data = scrape_game_detail(link)
        if not data:
            continue
        title = data.get("title", "Not Available")
        if title == "Not Available" or title in seen_titles:
            continue
        seen_titles.add(title)
        games.append(data)
        time.sleep(1.5)

    if games:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(games, f, indent=2, ensure_ascii=False)
        fieldnames = ["title", "release_date", "platforms", "developer",
                      "publisher", "genre", "score", "key_features", "url", "image_url"]
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(games)
        print("[scraper] Done. Saved " + str(len(games)) + " games.")
    return games


def load_games():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []