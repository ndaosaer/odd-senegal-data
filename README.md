# ODD Sénégal, Données

Dépôt des données pour la plateforme Open SDG Sénégal.

**Dépôt site :** https://github.com/ndaosaer/odd-senegal-site

## Structure

```
data/
  indicator_1-1-1.csv    Score composite ODD 1 (Pauvreté)
  indicator_2-1-1.csv    Score composite ODD 2 (Alimentation)
  indicator_3-1-1.csv    Score composite ODD 3 (Santé)
  ...                    (17 fichiers au total)

meta/
  1-1-1.yml              Métadonnées ODD 1
  2-1-1.yml              Métadonnées ODD 2
  ...                    (17 fichiers au total)

scripts/
  build.py               Script de compilation des données
```

## Format des fichiers CSV

Chaque fichier CSV contient trois colonnes :

| Year | Value  | Type        |
|------|--------|-------------|
| 2000 | 0.1355 | Historique  |
| 2024 | 0.3777 | Historique  |
| 2025 | 0.3650 | Projection  |
| 2030 | 0.1990 | Projection  |

## Ajouter de nouvelles données (ex : EHCVM 2021)

1. Ouvrir le fichier CSV de l'ODD concerné (ex : `data/indicator_1-1-1.csv`)
2. Mettre à jour les valeurs avec les nouvelles données ANSD
3. Mettre à jour le fichier YAML de métadonnées si nécessaire
4. Committer et pousser :

```bash
git add data/indicator_1-1-1.csv
git commit -m "Mise à jour ODD 1 avec données EHCVM 2021"
git push origin main
```

GitHub Actions recompile automatiquement. Le site se met à jour en 3-5 minutes.

## Sources des données

| ODD | Sources |
|-----|---------|
| 1   | ONU SDGAPI, Banque Mondiale WDI, ANSD (EHCVM) |
| 2   | FAO FAOSTAT, ONU SDGAPI |
| 3   | OMS GHO, Banque Mondiale WDI, PNUD HDR |
| 4   | ONU SDGAPI, Banque Mondiale WDI, ANSD (DPRE) |
| 5   | ONU SDGAPI, PNUD HDR (IIG) |
| 6-17| ONU SDGAPI, Banque Mondiale WDI, FAO, OMS |

## Auteur

ANSD / DMCI — Mémoire Analyste Statisticien, Dakar 2025
Saer Ndao
