import pytest


@pytest.mark.parametrize(
    "migration_path",
    ["weblogic_to_eap7", "thorntail_to_eapxp2", "springboot_to_quarkus", "eap to azure-appservice"],
)
def test_apalysis(setup_vscode, migration_path):
    """
    Test to run an analysis on migration from weblogic to EAP 7 in VSCode IDE
    source : windup-rulesets/target/classes/eap7/weblogic/tests/data
    target : eap7
    """
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


def test_analysis_eapxp(setup_vscode):
    """
    Test to run an analysis on migration from thorntail to eapxp2 in VSCode IDE
    source : windup-rulesets/target/classes/eapxp/thorntail/tests/data
    target : eapxp

    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["eapxp_ruleset"],
        migration_target="eapxp",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eapxp")
    """


def test_analysis_quarkus(setup_vscode):
    """
    Test to run an analysis on migration from quarkus in VSCode IDE. Note that quarkus1 was removed
    as source and target through https://issues.redhat.com/browse/WINDUP-3328 .

    source : windup-rulesets/target/classes/quarkus/springboot/tests/data
    target : quarkus

    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["quarkus_ruleset"],
        migration_target="quarkus",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="quarkus")
    """
