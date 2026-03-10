import json
import csv
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

BASE_URL = "https://www.metacritic.com"

DATA_FILE = os.path.join(os.path.dirname(__file__), "games_data.json")
CSV_FILE  = os.path.join(os.path.dirname(__file__), "games_data.csv")


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def get_soup(driver, url, wait_selector=None, wait_time=12):
    driver.get(url)
    if wait_selector:
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
            )
        except Exception:
            pass
    time.sleep(4)
    return BeautifulSoup(driver.page_source, "lxml")


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
                        if isinstance(img, list):
                            img = img[0]
                        if isinstance(img, dict):
                            img = img.get("url", "Not Available")
                        data["image_url"] = img
                    for role in ["author", "creator", "developer"]:
                        val = obj.get(role)
                        if val:
                            if isinstance(val, list):
                                val = val[0]
                            if isinstance(val, dict):
                                val = val.get("name", "Not Available")
                            data["developer"] = str(val)
                            break
                    pub = obj.get("publisher")
                    if pub:
                        if isinstance(pub, list):
                            pub = pub[0]
                        if isinstance(pub, dict):
                            pub = pub.get("name", "Not Available")
                        data["publisher"] = str(pub)
                    genre = obj.get("genre")
                    if genre:
                        if isinstance(genre, list):
                            genre = ", ".join(genre)
                        data["genre"] = str(genre)
                    platform = obj.get("gamePlatform") or obj.get("operatingSystem")
                    if platform:
                        if isinstance(platform, list):
                            platform = ", ".join(platform)
                        data["platforms"] = str(platform)
                    agg = obj.get("aggregateRating")
                    if agg and isinstance(agg, dict):
                        rv = agg.get("ratingValue")
                        if rv:
                            data["score"] = str(int(float(rv)))
            except Exception:
                continue
    except Exception:
        pass
    return data


def _text(soup, selector, attr=None):
    el = soup.select_one(selector)
    if el is None:
        return "Not Available"
    if attr:
        return el.get(attr, "Not Available").strip() or "Not Available"
    return el.get_text(separator=" ", strip=True) or "Not Available"


def _find_meta(soup, label_text):
    # Method 1 - new card layout
    for li in soup.select("li.c-gameDetails_listItem"):
        text = li.get_text(separator="|", strip=True)
        parts = text.split("|")
        for idx, part in enumerate(parts):
            if label_text.lower() in part.lower():
                remaining = "|".join(parts[idx+1:]).strip()
                if remaining:
                    return remaining

    # Method 2 - definition list
    for dt in soup.select("dt"):
        if label_text.lower() in dt.get_text(strip=True).lower():
            dd = dt.find_next_sibling("dd")
            if dd:
                return dd.get_text(separator=", ", strip=True)

    # Method 3 - legacy layout
    for li in soup.select("li.summary_detail"):
        lbl = li.select_one("span.label")
        val_el = li.select_one("span.data")
        if lbl and label_text.lower() in lbl.get_text(strip=True).lower() and val_el:
            return val_el.get_text(separator=", ", strip=True)

    # Method 4 - scan entire page text line by line
    full_text = soup.get_text(separator="\n", strip=True)
    lines = full_text.split("\n")
    for idx, line in enumerate(lines):
        if line.strip().lower() == label_text.lower():
            for next_line in lines[idx+1:]:
                val = next_line.strip()
                if val and len(val) < 150:
                    return val

    # Method 5 - span/div pairs anywhere on page
    for el in soup.find_all(["span", "div", "p"]):
        if el.get_text(strip=True).lower() == label_text.lower():
            sibling = el.find_next_sibling()
            if sibling:
                val = sibling.get_text(separator=", ", strip=True)
                if val and len(val) < 150:
                    return val
            parent = el.parent
            if parent:
                siblings = list(parent.children)
                for i, child in enumerate(siblings):
                    if hasattr(child, 'get_text') and child.get_text(strip=True).lower() == label_text.lower():
                        remaining = [c for c in siblings[i+1:] if hasattr(c, 'get_text') and c.get_text(strip=True)]
                        if remaining:
                            return remaining[0].get_text(separator=", ", strip=True)

    return "Not Available"


def scrape_game_detail(driver, game_url):
    print("[scraper] Scraping: " + game_url)
    soup = get_soup(driver, game_url, wait_selector="h1")
    raw_html = driver.page_source

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

    # JSON-LD first - most reliable
    ld_data = extract_from_json_ld(raw_html)
    game.update({k: v for k, v in ld_data.items() if v})

    # Title fallback
    if game["title"] == "Not Available":
        for sel in ["h1.c-productHero_title", "h1[class*='title']", "h1"]:
            val = _text(soup, sel)
            if val != "Not Available" and len(val) < 200:
                game["title"] = val
                break

    # Score fallback
    if game["score"] == "Not Available":
        for sel in ["div.c-siteReviewScore span", "span.metascore_w", "div.c-ScoreCard span"]:
            val = _text(soup, sel)
            if val != "Not Available" and val.strip().isdigit():
                game["score"] = val.strip()
                break

    # Image fallback
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

    # HTML fallbacks for details
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

    # Key features fallback
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

    print("[scraper] Got: " + game["title"] + " | Dev: " + game["developer"] + " | Pub: " + game["publisher"])
    return game


def scrape_games_list(base_url, limit=15):
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
    driver = get_driver()
    games = []
    seen_titles = set()

    try:
        for link in game_links:
            if len(games) >= limit:
                break
            data = scrape_game_detail(driver, link)
            if not data:
                continue
            title = data.get("title", "Not Available")
            if title == "Not Available" or title in seen_titles:
                continue
            seen_titles.add(title)
            games.append(data)
            time.sleep(1)
    finally:
        driver.quit()

    return games


def save_to_json(games, filepath=DATA_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
    print("[scraper] Saved " + str(len(games)) + " games to JSON")


def save_to_csv(games, filepath=CSV_FILE):
    if not games:
        return
    fieldnames = ["title", "release_date", "platforms", "developer",
                  "publisher", "genre", "score", "key_features", "url", "image_url"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(games)
    print("[scraper] Saved " + str(len(games)) + " games to CSV")


def load_games():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def run_scraper(base_url=BASE_URL, limit=15):
    print("[scraper] Starting scrape of " + base_url)
    games = scrape_games_list(base_url, limit=limit)
    if games:
        save_to_json(games)
        save_to_csv(games)
    else:
        print("[scraper] No games scraped.")
    return games