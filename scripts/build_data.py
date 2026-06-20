"""
Build script officiel pour le depot de donnees Open SDG.
Utilise la bibliotheque sdg-build pour generer les fichiers JSON
attendus par le plugin jekyll-open-sdg-plugins.

Ce script remplace l'ancien script "maison" qui generait les
fichiers JSON a la main et causait des incompatibilites avec
le plugin Jekyll cote site.
"""
import sdg


def main():
    if sdg.open_sdg_check_from_config('config_data.yml'):
        sdg.open_sdg_build_from_config('config_data.yml')
        print("BUILD TERMINE - fichiers generes dans _site/")
    else:
        print("ECHEC DE VALIDATION - voir les erreurs ci-dessus")
        exit(1)


if __name__ == '__main__':
    main()
