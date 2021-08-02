def test_analysis_eap(setup_codereadystudio):
    """
    Test to run analysis for migration path Anything to EAP 7 in CodeReadyStudio IDE
    """
    codereadystudio = setup_codereadystudio
    codereadystudio.open_mta_perspective()
    codereadystudio.run_simple_analysis(project="acme", migration_target="eap7")
    assert codereadystudio.is_analysis_complete()
    assert codereadystudio.verify_story_points(target="eap7")


def test_analysis_eapxp(setup_codereadystudio):
    """
    Test to run analysis on ruleset thorntail to eapxp2 in CodeReadyStudio IDE
    """
    codereadystudio = setup_codereadystudio
    codereadystudio.open_mta_perspective()
    codereadystudio.run_simple_analysis(project="data_thorntail", migration_target="eapxp")
    assert codereadystudio.is_analysis_complete()
    assert codereadystudio.verify_story_points(target="eapxp")


def test_analysis_quarkus(setup_codereadystudio):
    """
    Test to run analysis on ruleset quarkus1 in CodeReadyStudio IDE
    """
    codereadystudio = setup_codereadystudio
    codereadystudio.open_mta_perspective()
    codereadystudio.run_simple_analysis(project="data_quarkus1", migration_target="quarkus1")
    assert codereadystudio.is_analysis_complete()
    assert codereadystudio.verify_story_points(target="quarkus1")
