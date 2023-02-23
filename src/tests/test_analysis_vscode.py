import pytest


@pytest.mark.parametrize(
    "migration_path",
    ["weblogic_to_eap7", "thorntail_to_eapxp2", "springboot_to_quarkus", "eap to azure-appservice"],
)
def test_apalysis(setup_vscode, migration_path):
    """Analysis tests for VScode using various migration paths"""
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    if migration_path == "weblogic_to_eap7":
        project = config["project_paths"]["eap7_generic"]
        migration_target = "eap7"
    elif migration_path == "thorntail_to_eapxp2":
        project = config["project_paths"]["eapxp_ruleset"]
        migration_target = "eapxp"
    elif migration_path == "springboot_to_quarkus":
        project = config["project_paths"]["quarkus_ruleset"]
        migration_target = "quarkus"
    else:
        project = config["project_paths"]["azure_ruleset"]
        migration_target = "azure-appservice"
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(migration_target)
