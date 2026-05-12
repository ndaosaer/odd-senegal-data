"""
Script de build des données au format exact attendu par Open SDG.
Génère tous les fichiers JSON requis par le thème open-sdg/open-sdg.

Structure générée dans _site/ :
  en/meta/all.json          ← liste de tous les indicateurs
  en/meta/1-1-1.json        ← métadonnées par indicateur
  en/data/1-1-1.json        ← données par indicateur
  en/stats/reporting.json   ← statut de reporting
  fr/meta/all.json          ← idem en français
  fr/meta/1-1-1.json
  fr/data/1-1-1.json
  fr/stats/reporting.json
"""

import os
import json
import csv
import yaml
from pathlib import Path

SITE_DIR = Path("_site")
LANGUAGES = ["fr", "en"]

# ─── Données historiques et projections ──────────────────────────────────────
HIST = {
    "1": [0.136,0.259,0.187,0.233,0.291,0.293,0.243,0.270,0.747,0.818,
          0.286,0.426,0.466,0.587,0.522,0.440,0.425,0.403,0.443,0.393,
          0.392,0.376,0.369,0.369,0.378],
    "2": [0.226,0.258,0.250,0.284,0.326,0.309,0.357,0.408,0.522,0.522,
          0.524,0.496,0.529,0.507,0.540,0.547,0.592,0.591,0.640,0.654,
          0.706,0.705,0.739,0.723,0.750],
    "3": [0.119,0.157,0.206,0.260,0.325,0.350,0.442,0.482,0.518,0.555,
          0.577,0.610,0.637,0.657,0.633,0.637,0.660,0.669,0.706,0.739,
          0.760,0.759,0.799,0.789,0.791],
    "4": [0.102,0.144,0.180,0.275,0.266,0.273,0.302,0.426,0.460,0.504,
          0.534,0.657,0.674,0.655,0.684,0.693,0.721,0.773,0.756,0.777,
          0.855,0.883,0.881,0.908,0.963],
    "5": [0.000,0.039,0.079,0.092,0.103,0.111,0.127,0.147,0.162,0.180,
          0.188,0.206,0.327,0.401,0.413,0.418,0.426,0.429,0.441,0.454,
          0.490,0.573,0.981,0.965,0.966],
    "6": [0.132,0.252,0.211,0.233,0.267,0.291,0.304,0.337,0.358,0.373,
          0.393,0.407,0.420,0.447,0.484,0.490,0.491,0.539,0.658,0.657,
          0.658,0.668,0.685,0.760,0.763],
    "7": [0.297,0.302,0.268,0.329,0.257,0.355,0.413,0.345,0.355,0.498,
          0.500,0.479,0.483,0.429,0.434,0.411,0.523,0.455,0.499,0.580,
          0.568,0.584,0.617,0.651,0.651],
    "8": [0.333,0.359,0.212,0.429,0.417,0.433,0.379,0.414,0.494,0.465,
          0.533,0.435,0.506,0.421,0.549,0.548,0.524,0.733,0.686,0.716,
          0.566,0.795,0.694,0.720,0.808],
    "9": [0.357,0.363,0.391,0.385,0.289,0.288,0.318,0.304,0.312,0.298,
          0.308,0.364,0.369,0.379,0.298,0.321,0.320,0.372,0.426,0.538,
          0.504,0.452,0.643,0.632,0.754],
    "10":[0.342,0.318,0.350,0.335,0.355,0.393,0.434,0.457,0.449,0.465,
          0.401,0.470,0.527,0.440,0.497,0.404,0.507,0.601,0.526,0.444,
          0.448,0.440,0.402,0.463,0.449],
    "11":[0.469,0.475,0.482,0.484,0.484,0.488,0.549,0.544,0.361,0.396,
          0.655,0.653,0.539,0.525,0.631,0.580,0.640,0.609,0.650,0.691,
          0.701,0.709,0.718,0.724,0.638],
    "12":[0.110,0.235,0.233,0.256,0.267,0.073,0.081,0.108,0.034,0.064,
          0.118,0.142,0.090,0.122,0.311,0.337,0.194,0.282,0.350,0.621,
          0.441,0.479,0.491,0.485,0.606],
    "13":[0.633,0.765,0.776,0.811,0.725,0.741,0.724,0.763,0.662,0.624,
          0.617,0.581,0.620,0.575,0.564,0.547,0.486,0.408,0.432,0.350,
          0.309,0.306,0.267,0.264,0.264],
    "14":[0.000,0.033,0.033,0.033,0.260,0.260,0.260,0.260,0.260,0.260,
          0.259,0.259,0.260,0.260,0.347,0.346,0.346,0.863,0.773,0.819,
          0.845,0.803,1.000,1.000,1.000],
    "15":[0.446,0.436,0.386,0.389,0.401,0.448,0.361,0.343,0.428,0.403,
          0.376,0.326,0.344,0.352,0.348,0.410,0.389,0.363,0.382,0.363,
          0.362,0.561,0.464,0.496,0.460],
    "16":[0.541,0.543,0.546,0.549,0.551,0.554,0.551,0.548,0.546,0.543,
          0.540,0.326,0.311,0.297,0.282,0.136,0.500,0.500,0.139,0.139,
          0.144,0.130,0.130,0.100,0.100],
    "17":[0.338,0.318,0.319,0.320,0.366,0.322,0.328,0.334,0.356,0.341,
          0.317,0.317,0.364,0.343,0.399,0.360,0.366,0.323,0.362,0.462,
          0.478,0.536,0.524,0.623,0.592],
}

PROJ = {
    "1":0.199,"2":0.826,"3":0.797,"4":0.983,"5":0.966,
    "6":0.916,"7":0.729,"8":0.889,"9":0.911,"10":0.384,
    "11":0.794,"12":0.861,"13":0.070,"14":0.987,"15":0.566,
    "16":0.044,"17":0.807,
}

FEU = {
    "1":"Rouge","2":"Vert","3":"Vert","4":"Vert","5":"Orange",
    "6":"Vert","7":"Orange","8":"Vert","9":"Vert","10":"Rouge",
    "11":"Vert","12":"Vert","13":"Rouge","14":"Orange","15":"Orange foncé",
    "16":"Rouge","17":"Vert",
}

N_IND = {
    "1":5,"2":39,"3":43,"4":18,"5":5,"6":12,"7":11,"8":14,
    "9":10,"10":10,"11":8,"12":4,"13":13,"14":2,"15":22,"16":5,"17":20,
}

LABELS = {
    "1":"Pas de pauvreté","2":"Faim zéro","3":"Bonne santé et bien-être",
    "4":"Éducation de qualité","5":"Égalité des genres",
    "6":"Eau propre et assainissement","7":"Énergie propre et abordable",
    "8":"Travail décent et croissance économique",
    "9":"Industrie, innovation et infrastructure",
    "10":"Inégalités réduites","11":"Villes et communautés durables",
    "12":"Consommation et production responsables",
    "13":"Mesures relatives à la lutte contre les changements climatiques",
    "14":"Vie aquatique","15":"Vie terrestre",
    "16":"Paix, justice et institutions efficaces",
    "17":"Partenariats pour la réalisation des objectifs",
}

YEARS_HIST = list(range(2000, 2025))
YEARS_PROJ = list(range(2025, 2031))
SOURCES = {
    "1":"ONU SDGAPI, Banque Mondiale WDI, ANSD",
    "2":"FAO FAOSTAT, ONU SDGAPI","3":"OMS GHO, Banque Mondiale WDI, PNUD HDR",
    "4":"ONU SDGAPI, Banque Mondiale WDI","5":"ONU SDGAPI, PNUD HDR",
    "6":"ONU SDGAPI, Banque Mondiale WDI","7":"ONU SDGAPI, Banque Mondiale WDI",
    "8":"ONU SDGAPI, Banque Mondiale WDI","9":"ONU SDGAPI, Banque Mondiale WDI",
    "10":"ONU SDGAPI, Banque Mondiale WDI","11":"ONU SDGAPI, Banque Mondiale WDI",
    "12":"ONU SDGAPI, Banque Mondiale WDI","13":"FAO FAOSTAT, Banque Mondiale WDI",
    "14":"ONU SDGAPI","15":"FAO FAOSTAT, Banque Mondiale WDI",
    "16":"ONU SDGAPI, Banque Mondiale WDI","17":"ONU SDGAPI, Banque Mondiale WDI",
}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_indicator_meta(num):
    """Construit le dict de métadonnées d'un indicateur."""
    ind_id = f"{num}-1-1"
    return {
        "indicator":          f"{num}.1.1",
        "indicator_number":   f"{num}.1.1",
        "indicator_name":     f"Score composite normalisé — ODD {num} : {LABELS[num]}",
        "goal":               str(num),
        "target":             f"{num}.1",
        "target_name":        LABELS[num],
        "published":          True,
        "reporting_status":   "complete",
        "national_indicator_description": (
            f"Score composite normalisé de l'ODD {num} calculé à partir de "
            f"{N_IND[num]} indicateurs internationaux pour le Sénégal (2000-2024). "
            f"Méthode : normalisation min-max (OCDE, 2008). "
            f"Score 2024 : {HIST[num][-1]:.3f}. "
            f"Projection 2030 : {PROJ[num]:.3f}."
        ),
        "computation_units":  "Score normalisé [0 – 1]",
        "national_geographical_coverage": "Sénégal",
        "source_organisation_1": SOURCES[num],
        "contact_organisation": "ANSD / DMCI — Dakar, Sénégal",
        "periodicity":        "Annuelle",
        "status":             FEU[num],
        "score_2024":         round(HIST[num][-1], 3),
        "projection_2030":    PROJ[num],
        "n_indicateurs":      N_IND[num],
        "data_start_values":  [],
        "graph_type":         "line",
        "graph_title":        f"ODD {num} — {LABELS[num]}",
        "graph_annotations": [
            {
                "value": 0.75,
                "label": "Cible 2030",
                "mode":  "horizontal",
                "preset": "target",
            }
        ],
    }


def build_indicator_data(num):
    """Construit les données au format attendu par Open SDG."""
    rows = []
    for yr, val in zip(YEARS_HIST, HIST[num]):
        rows.append({"Year": yr, "Value": round(val, 4)})
    # Ajouter les projections
    slope = (HIST[num][-1] - HIST[num][-3]) / 2
    for i, yr in enumerate(YEARS_PROJ, 1):
        proj_val = round(min(1.0, max(0.0, HIST[num][-1] + slope * i)), 4)
        rows.append({"Year": yr, "Value": proj_val, "Type": "Projection"})
    return rows


def build_reporting_status(all_meta):
    """Construit le fichier de statut de reporting."""
    statuses = {}
    for ind_id, meta in all_meta.items():
        goal = meta["goal"]
        if goal not in statuses:
            statuses[goal] = {"goal": int(goal), "statuses": {}}
        status = meta["reporting_status"]
        if status not in statuses[goal]["statuses"]:
            statuses[goal]["statuses"][status] = 0
        statuses[goal]["statuses"][status] += 1

    return {
        "statuses":   list(statuses.values()),
        "totals":     {"total": len(all_meta), "complete": len(all_meta)},
        "extra_fields": {"status": {
            "Vert":         [k for k,v in FEU.items() if v == "Vert"],
            "Orange":       [k for k,v in FEU.items() if v == "Orange"],
            "Orange foncé": [k for k,v in FEU.items() if v == "Orange foncé"],
            "Rouge":        [k for k,v in FEU.items() if v == "Rouge"],
        }},
    }


def main():
    print("=" * 60)
    print("BUILD DONNÉES OPEN SDG — SÉNÉGAL")
    print("=" * 60)

    all_meta = {}

    for num in [str(i) for i in range(1, 18)]:
        ind_id = f"{num}-1-1"
        meta   = build_indicator_meta(num)
        data   = build_indicator_data(num)
        all_meta[ind_id] = meta

        for lang in LANGUAGES:
            # Métadonnées individuelles
            write_json(
                SITE_DIR / lang / "meta" / f"{ind_id}.json",
                meta
            )
            # Données individuelles
            write_json(
                SITE_DIR / lang / "data" / f"{ind_id}.json",
                {"indicator": f"{num}.1.1", "data": data}
            )
            # CSV des données (format Open SDG)
            csv_path = SITE_DIR / lang / "data" / f"{ind_id}.csv"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Year", "Value"])
                writer.writeheader()
                for row in [r for r in data if "Type" not in r]:
                    writer.writerow(row)

        print(f"  ODD {num:2s} : meta + data générés "
              f"(score 2024={HIST[num][-1]:.3f}, "
              f"proj 2030={PROJ[num]:.3f}, "
              f"statut={FEU[num]})")

    # all.json pour chaque langue (clé du build Open SDG)
    for lang in LANGUAGES:
        write_json(SITE_DIR / lang / "meta" / "all.json", all_meta)
        write_json(SITE_DIR / lang / "stats" / "reporting.json",
                   build_reporting_status(all_meta))

    # headlines.json ET headline/all.json
    headlines = {}
    for num in [str(i) for i in range(1, 18)]:
        ind_id = f"{num}-1-1"
        headlines[ind_id] = [
            {"Year": yr, "Value": round(val, 4)}
            for yr, val in zip(YEARS_HIST, HIST[num])
        ]
    for lang in LANGUAGES:
        write_json(SITE_DIR / lang / "data" / "headlines.json", headlines)
        # Open SDG cherche aussi en/headline/all.json
        write_json(SITE_DIR / lang / "headline" / "all.json", headlines)
        # Et parfois en/data/all.json
        write_json(SITE_DIR / lang / "data" / "all.json", headlines)
        write_json(SITE_DIR / lang / "headline" / "all.json", headlines)
        write_json(SITE_DIR / lang / "data" / "all.json", headlines)

    # zip.json (liste des indicateurs publiés)
    zip_data = {
        ind_id: {"published": True, "reporting_status": "complete"}
        for ind_id in all_meta
    }
    for lang in LANGUAGES:
        write_json(SITE_DIR / lang / "zip.json", zip_data)

    # Fichier de configuration globale pour le site
    site_config = {
        "remote_data_prefix": "https://ndaosaer.github.io/odd-senegal-data",
        "languages": LANGUAGES,
        "goals": [
            {"number": i, "name": LABELS[str(i)]}
            for i in range(1, 18)
        ],
    }
    write_json(SITE_DIR / "config.json", site_config)

    print("\n" + "=" * 60)
    print("BUILD TERMINÉ")
    print(f"Fichiers générés dans : {SITE_DIR.resolve()}/")
    for lang in LANGUAGES:
        n_files = sum(1 for _ in (SITE_DIR / lang).rglob("*") if _.is_file())
        print(f"  {lang}/ : {n_files} fichiers")
    print("=" * 60)

# schema.json requis par Open SDG
    schema = {
        "fields": [
            {"name": "indicator", "title": "Indicator", "type": "string"},
            {"name": "indicator_name", "title": "Indicator name", "type": "string"},
            {"name": "goal", "title": "Goal", "type": "string"},
            {"name": "target", "title": "Target", "type": "string"},
            {"name": "published", "title": "Published", "type": "boolean"},
            {"name": "reporting_status", "title": "Reporting status", "type": "string"},
            {"name": "computation_units", "title": "Unit of measurement", "type": "string"},
            {"name": "graph_type", "title": "Graph type", "type": "string"},
            {"name": "source_organisation_1", "title": "Organisation", "type": "string"},
        ]
    }
    for lang in LANGUAGES:
        write_json(SITE_DIR / lang / "meta" / "schema.json", schema)

if __name__ == "__main__":
    main()
