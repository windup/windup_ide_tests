def test_analysis_eap(setup_vscode):
    """
    Test to run an analysis on migration from weblogic to EAP 7 in VSCode IDE
    source : windup-rulesets/target/classes/eap7/weblogic/tests/data
    target : eap7
    """
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["eap7_generic"],
        migration_target="eap7",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eap7")


def test_analysis_eapxp(setup_vscode):
    """
    Test to run an analysis on migration from thorntail to eapxp2 in VSCode IDE
    source : windup-rulesets/target/classes/eapxp/thorntail/tests/data
    target : eapxp
    """
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["eapxp_ruleset"],
        migration_target="eapxp",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eapxp")


def test_analysis_quarkus(setup_vscode):
    """
    Test to run an analysis on migration from quarkus in VSCode IDE. Note that quarkus1 was removed
    as source and target through https://issues.redhat.com/browse/WINDUP-3328 .

    source : windup-rulesets/target/classes/quarkus/springboot/tests/data
    target : quarkus
    """
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["quarkus_ruleset"],
        migration_target="quarkus",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="quarkus")
