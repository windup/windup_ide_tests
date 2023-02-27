import pytest


@pytest.mark.parametrize(
    "migration_path",
    ["weblogic_to_eap7", "thorntail_to_eapxp", "springboot_to_quarkus", "eap_to_azure-appservice"],
)
def test_analysis(setup_vscode, migration_path):
    """Analysis tests for VScode using various migration paths"""
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    project = config["project_path"][migration_path]["path"]
    migration_target = config["project_path"][migration_path]["targets"]
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(migration_target)
