#!/usr/bin/env python3
"""
Download Wikimedia Commons photos for each Hengdian attraction polygon
and emit attraction_photos.csv that joins on osm_id with the shapefile.
"""
import csv
import json
import re
import time
import urllib.parse
from pathlib import Path
import requests

OUT = Path("/Users/pleiadesm./Documents/GitHub/MovieMap/from-scratch/data/hengdian")
PHOTOS = OUT / "attraction_photos"
PHOTOS.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "MovieMap-academic/0.1 (daocheng@iastate.edu)"}

# osm_id → (name_en, commons_filename or None, match_quality, license_note)
# match_quality: "direct" (Commons caption names the attraction) | "inferred"
# (educated guess based on what the photo depicts) | "none"
PHOTOS_MAP = {
    "317231689":  ("Palace of Ming and Qing Dynasties",
                   "20240111 Replica of the Taihe Hall in the Hengdian World Studios.jpg", "direct"),
    "419188975":  ("Hengdian Ming-Qing Folk Residence Expo Town", None, "none"),
    "630397698":  ("Huaxia Cultural Park",
                   "Hengdian- Three Religious Temple-China - panoramio.jpg", "inferred"),
    "630397701":  ("Along the River During the Qingming Festival",
                   "Hengdian World Studios 001.jpg", "direct"),
    "630397705":  ("Qin Dynasty Palace",
                   "Unification Hall, Palace of Emperor Qin, Hengdian World Studios (20250131150447).jpg", "direct"),
    "974859367":  ("Hengdian New Yuanmingyuan - Garden of Eternal Spring",
                   "20240112 Xieqiqu, Hengdian Yingshicheng.jpg", "inferred"),
    "974859368":  ("Hengdian New Yuanmingyuan - Garden of Beautiful Spring (Autumn Garden)",
                   "20240112 Haiyan Tang, Hengdian Yingshicheng.jpg", "inferred"),
    "974859369":  ("Hengdian New Yuanmingyuan",
                   "20240112 Yuanming Xinyuan (093439).jpg", "direct"),
    "974860832":  ("The Dream Valley",
                   "Jinniu Bridge at Dream Valley, Hengdian World Studios (20250131164136).jpg", "direct"),
    "1007605005": ("Hengdian Film and Television Industry Park",
                   "Drama filming at Hengdian World Studios.jpg", "direct"),
    "1007605015": ("Canton Street. Hongkong Street.",
                   "Hengdian World Studios 007.jpg", "direct"),
    "1007605023": ("Tang-Song Mansion · Period Sets", None, "none"),
    "1007605026": ("Dream Bund Film and Television Theme Park",
                   "Entrance of Legend of Bund, Hengdian World Studios (20250130180600).jpg", "direct"),
    "1491747837": ("Hengdian New Yuanmingyuan - Garden of Joyful Spring (Winter Garden)",
                   "20240112 Chunhua Men, Hengdian Yingshicheng.jpg", "inferred"),
    "1491758023": ("Hengdian National Defense Science and Technology Education Park", None, "none"),
    "1491758024": ("Dream Spring Valley Hot Spring Resort", None, "none"),
    "1491758025": ("Hengdian Red Army Long March Expo Town", None, "none"),
}


def safe_filename(name: str) -> str:
    name = name.replace("/", "_").replace(":", "_")
    return re.sub(r"[^a-zA-Z0-9._\-()]+", "_", name).strip("_")


def get_commons_image_url(filename: str) -> tuple[str, dict] | None:
    """Return (direct image URL, extmetadata dict) for a Commons file."""
    r = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "titles": f"File:{filename}",
            "format": "json",
        },
        headers=UA, timeout=20,
    )
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    for _, page in pages.items():
        ii = page.get("imageinfo")
        if ii:
            return ii[0]["url"], ii[0].get("extmetadata", {})
    return None


def main():
    rows = []
    for osm_id, (name_en, filename, quality) in PHOTOS_MAP.items():
        if filename is None:
            rows.append({
                "osm_id": osm_id, "name_en": name_en,
                "match_quality": "none", "image_local": "",
                "image_url": "", "commons_page": "", "license": "", "credit": "",
            })
            print(f"  ·· {osm_id} {name_en}: (no photo)")
            continue

        info = get_commons_image_url(filename)
        if not info:
            print(f"  !! {osm_id} {name_en}: lookup failed for {filename}")
            continue
        url, meta = info
        local_name = f"{osm_id}__{safe_filename(filename)}"
        local_path = PHOTOS / local_name
        if not local_path.exists():
            r = requests.get(url, headers=UA, timeout=30)
            r.raise_for_status()
            local_path.write_bytes(r.content)
            print(f"  ↓ {osm_id} {name_en} ({len(r.content)//1024} KB)")
        else:
            print(f"  = {osm_id} {name_en} (cached)")

        # Pull license + author from extmetadata
        lic = meta.get("LicenseShortName", {}).get("value", "") or \
              meta.get("UsageTerms", {}).get("value", "")
        author = meta.get("Artist", {}).get("value", "")
        author = re.sub(r"<[^>]+>", "", author).strip()
        commons_page = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(filename)}"

        rows.append({
            "osm_id": osm_id,
            "name_en": name_en,
            "match_quality": quality,
            "image_local": f"attraction_photos/{local_name}",
            "image_url": url,
            "commons_page": commons_page,
            "license": lic,
            "credit": author[:80],
        })
        time.sleep(0.4)

    out_csv = OUT / "attraction_photos.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "osm_id", "name_en", "match_quality",
            "image_local", "image_url", "commons_page", "license", "credit",
        ])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    matched = sum(1 for r in rows if r["image_local"])
    print(f"\nwrote {out_csv}: {len(rows)} rows ({matched} with photos)")


if __name__ == "__main__":
    main()
