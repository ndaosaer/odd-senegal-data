"""
=============================================================================
BUILD DES DONNÉES OPEN SDG — SÉNÉGAL
=============================================================================
Ce script lit les fichiers CSV de données et YAML de métadonnées,
et les compile au format attendu par la plateforme Open SDG.

STRUCTURE ATTENDUE :
  data/
    indicator_1-1-1.csv    (Score composite ODD 1)
    indicator_2-1-1.csv    (Score composite ODD 2)
    ...
  meta/
    1-1-1.yml
    2-1-1.yml
    ...
  scripts/
    build.py               (ce fichier)

MISE À JOUR DES DONNÉES :
  1. Remplacer le CSV de l'indicateur concerné dans data/
  2. git add . && git commit -m "Mise à jour données [ODD X]"
  3. git push origin main
  → GitHub Actions recompile et déploie automatiquement
=============================================================================
"""

import os, json, csv, yaml, shutil
from pathlib import Path

DATA_DIR  = Path("data")
META_DIR  = Path("meta")
SITE_DIR  = Path("_site")
SITE_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("BUILD DONNÉES OPEN SDG — SÉNÉGAL")
print("=" * 60)

# ── Lire tous les CSV de données ──────────────────────────────────────────────
print("\nLecture des fichiers de données...")
indicators = {}
for csv_file in sorted(DATA_DIR.glob("indicator_*.csv")):
    ind_id = csv_file.stem.replace("indicator_", "").replace("-", ".")
    rows = []
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "Year":  int(row["Year"]),
                "Value": float(row["Value"]),
                "Type":  row.get("Type", "Historique"),
            })
    indicators[ind_id] = rows
    print(f"  {ind_id} : {len(rows)} observations")

# ── Lire tous les YAML de métadonnées ─────────────────────────────────────────
print("\nLecture des métadonnées...")
metadata = {}
for yml_file in sorted(META_DIR.glob("*.yml")):
    ind_id = yml_file.stem.replace("-", ".")
    with open(yml_file, encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    metadata[ind_id] = meta
    print(f"  {ind_id} : {meta.get('indicator_name','')[:50]}")

# ── Compiler le JSON de sortie pour Open SDG ──────────────────────────────────
print("\nCompilation des fichiers JSON...")

# Fichier all_indicators.json (liste de tous les indicateurs)
all_indicators = []
for ind_id, rows in indicators.items():
    meta = metadata.get(ind_id, {})
    goal_num = ind_id.split(".")[0]

    # Dernière valeur disponible (hors projection)
    hist_rows = [r for r in rows if r["Type"] == "Historique"]
    last_val  = hist_rows[-1]["Value"] if hist_rows else None
    last_year = hist_rows[-1]["Year"]  if hist_rows else None

    # Score projeté 2030
    proj_rows = [r for r in rows if r["Type"] == "Projection"]
    proj_2030 = next((r["Value"] for r in proj_rows if r["Year"] == 2030), None)

    all_indicators.append({
        "id":           ind_id,
        "goal":         int(goal_num),
        "target":       f"{goal_num}.1",
        "name":         meta.get("indicator_name", f"ODD {goal_num} — Score composite"),
        "description":  meta.get("national_indicator_description", ""),
        "status":       meta.get("reporting_status", "complete"),
        "score_2024":   meta.get("score_2024", last_val),
        "score_2030":   meta.get("projection_2030", proj_2030),
        "feu":          meta.get("status", "").split(" — ")[0],
        "n_ind":        meta.get("n_indicateurs", 0),
        "source":       meta.get("source_organisation_1", ""),
        "published":    meta.get("published", True),
    })

with open(SITE_DIR / "all_indicators.json", "w", encoding="utf-8") as f:
    json.dump(all_indicators, f, ensure_ascii=False, indent=2)
print(f"  all_indicators.json : {len(all_indicators)} indicateurs")

# Fichier individuel par indicateur
ind_dir = SITE_DIR / "data"
ind_dir.mkdir(exist_ok=True)
for ind_id, rows in indicators.items():
    out = {
        "indicator": ind_id,
        "data":      rows,
        "metadata":  metadata.get(ind_id, {}),
    }
    fname = ind_dir / f"{ind_id.replace('.', '-')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

print(f"  Fichiers JSON individuels : {len(indicators)}")

# Fichier de résumé par ODD
goals_summary = {}
for ind in all_indicators:
    g = str(ind["goal"])
    if g not in goals_summary:
        goals_summary[g] = {
            "goal": ind["goal"],
            "indicators": [],
            "score_2024_moy": 0,
            "score_2030_moy": 0,
        }
    goals_summary[g]["indicators"].append(ind["id"])

for g, data in goals_summary.items():
    scores_24 = [ind["score_2024"] for ind in all_indicators
                 if str(ind["goal"]) == g and ind["score_2024"] is not None]
    scores_30 = [ind["score_2030"] for ind in all_indicators
                 if str(ind["goal"]) == g and ind["score_2030"] is not None]
    data["score_2024_moy"] = round(sum(scores_24)/len(scores_24), 4) if scores_24 else None
    data["score_2030_moy"] = round(sum(scores_30)/len(scores_30), 4) if scores_30 else None

with open(SITE_DIR / "goals.json", "w", encoding="utf-8") as f:
    json.dump(list(goals_summary.values()), f, ensure_ascii=False, indent=2)
print("  goals.json créé")

print("\n" + "=" * 60)
print("BUILD TERMINÉ")
print(f"  Fichiers dans : {SITE_DIR.resolve()}/")
print("  all_indicators.json")
print("  goals.json")
print(f"  data/ ({len(indicators)} fichiers JSON)")
print("=" * 60)
print("\nPour mettre à jour les données :")
print("  1. Modifier le CSV dans data/")
print("  2. git add . && git commit -m 'Mise à jour données'")
print("  3. git push → GitHub Actions redéploie automatiquement")
