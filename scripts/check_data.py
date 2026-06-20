"""
Script de verification des donnees et metadonnees, sans generer
la sortie complete. Utilise par le workflow test-pull-requests.yml
pour valider une pull request avant fusion.
"""
import sdg


def main():
    if sdg.open_sdg_check(config='config_data.yml'):
        print("VERIFICATION REUSSIE")
    else:
        print("ECHEC DE VERIFICATION - voir les erreurs ci-dessus")
        exit(1)


if __name__ == '__main__':
    main()
