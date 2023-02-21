import pytest

from src.lib.config import config_data


@pytest.mark.parametrize('migration_path', ['eap7-genereic to eap7', 'thorntail to eapxp', 'springboot to quarkus',
        'openjdk17'])
def test_analysis(setup_vscode, migration_path):
    """
    Test to run an analysis on migration from weblogic to EAP 7 in VSCode IDE
    source : windup-rulesets/target/classes/eap7/weblogic/tests/data
    target : eap7
    """
    vscode = setup_vscode
    vscode.open_mta_perspective()
    if migration_path == 'eap7-genereic to eap7':
        source=config["project_paths"]["eap7_generic"],
        target="eap7"
    elif migration_path == 'thorntail to eapxp':
        source=config["project_paths"]["eapxp_ruleset"],
        target="eapxp"
    elif migration_path == 'springboot to quarkus':
        source=config["project_paths"]["quarkus_ruleset"],
        target="quarkus"
    elif migration_path == 'openjdk17':
        source=config["project_paths"]["openjdk17"],
        target="openjdk17"
    vscode.run_simple_analysis(
        project=source,
        migration_target=target,
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eap7")
    