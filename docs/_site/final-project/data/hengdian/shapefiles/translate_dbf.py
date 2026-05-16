#!/usr/bin/env python3
"""
Fill in missing name_en values in the Hengdian shapefile attribute table.
Preserves the existing 5 English names and adds 12 new ones using the same
descriptive style. Geometry is untouched.
"""
import shapefile
import shutil
from pathlib import Path

SRC = Path("/Users/pleiadesm./Documents/GitHub/MovieMap/from-scratch/data/hengdian/shapefiles/HengdianStudio")
TMP = Path("/tmp/HengdianStudio_translated")

# osm_id -> English name. Using osm_id (stable) instead of row index so the
# join is robust to reordering.
TRANSLATIONS = {
    "419188975":  "Hengdian Ming-Qing Folk Residence Expo Town",
    "630397698":  "Huaxia Cultural Park",
    "974859367":  "Hengdian New Yuanmingyuan - Garden of Eternal Spring",
    "974859368":  "Hengdian New Yuanmingyuan - Garden of Beautiful Spring (Autumn Garden)",
    "974859369":  "Hengdian New Yuanmingyuan",
    "1007605005": "Hengdian Film and Television Industry Park",
    "1007605023": "Tang-Song Mansion · Period Sets",
    "1007605026": "Dream Bund Film and Television Theme Park",
    "1491747837": "Hengdian New Yuanmingyuan - Garden of Joyful Spring (Winter Garden)",
    "1491758023": "Hengdian National Defense Science and Technology Education Park",
    "1491758024": "Dream Spring Valley Hot Spring Resort",
    "1491758025": "Hengdian Red Army Long March Expo Town",
}


def main():
    reader = shapefile.Reader(str(SRC), encoding="utf-8")
    writer = shapefile.Writer(str(TMP), shapeType=reader.shapeType)
    writer.encoding = "utf-8"

    # Copy field schema (drop the implicit DeletionFlag at index 0)
    for f in reader.fields:
        if f[0] == "DeletionFlag":
            continue
        writer.field(*f)

    updated = 0
    already = 0
    for shape_rec in reader.iterShapeRecords():
        rec = shape_rec.record.as_dict()
        oid = rec["osm_id"]
        if not rec.get("name_en"):
            if oid in TRANSLATIONS:
                rec["name_en"] = TRANSLATIONS[oid]
                updated += 1
        else:
            already += 1
        writer.shape(shape_rec.shape)
        writer.record(**rec)

    writer.close()
    reader.close()

    # Replace original sidecar files
    for ext in ("shp", "shx", "dbf"):
        shutil.copy(f"{TMP}.{ext}", f"{SRC}.{ext}")

    print(f"  pre-existing English names: {already}")
    print(f"  newly added:                {updated}")
    print(f"  written back to: {SRC}.dbf (and .shp/.shx)")


if __name__ == "__main__":
    main()
