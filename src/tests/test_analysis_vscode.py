def test_analysis_eap(setup_vscode):
    """
    Test to run analysis for migration path Anything to EAP 7 in VSCode IDE
    """
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["eap7_generic"], migration_target="eap7",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eap7")


def test_analysis_eapxp(setup_vscode):
    """
    Test to run analysis on ruleset thorntail to eapxp2 in VSCode IDE
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["eapxp_ruleset"], migration_target="eapxp",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="eapxp")
    """

def test_analysis_quarkus(setup_vscode):
    """
    Test to run analysis on ruleset quarkus1 in VSCode IDE
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(
        project=config["project_paths"]["quarkus1_ruleset"], migration_target="quarkus1",
    )
    assert vscode.is_analysis_complete()
    vscode.open_report_page()
    assert vscode.verify_story_points(target="quarkus1")
    """
