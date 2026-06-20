"""
Build script officiel pour le depot de donnees Open SDG.
Utilise la bibliotheque sdg-build (module Python "sdg") pour generer
les fichiers JSON attendus par le plugin jekyll-open-sdg-plugins.
"""
import sdg


def main():
    if sdg.open_sdg_check(config='config_data.yml'):
        sdg.open_sdg_build(config='config_data.yml')
        print("BUILD TERMINE - fichiers generes dans _site/")
    else:
        print("ECHEC DE VALIDATION - voir les erreurs ci-dessus")
        exit(1)


if __name__ == '__main__':
    main()
