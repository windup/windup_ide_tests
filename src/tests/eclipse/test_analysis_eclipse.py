def test_analysis_eap(setup_eclipse):
    """
    Test to run analysis for migration path Anything to EAP 7 in Eclipse IDE
    """
    eclipse = setup_eclipse
    eclipse.open_mta_perspective()
    eclipse.run_simple_analysis(project="acme", migration_target="eap7")
    assert eclipse.is_analysis_complete()
    assert eclipse.verify_story_points(target="eap7")


def test_analysis_eapxp(setup_eclipse):
    """
    Test to run analysis on ruleset thorntail to eapxp2 in Eclipse IDE
    """
    eclipse = setup_eclipse
    eclipse.open_mta_perspective()
    eclipse.run_simple_analysis(project="data_thorntail", migration_target="eapxp")
    assert eclipse.is_analysis_complete()
    assert eclipse.verify_story_points(target="eapxp")


def test_analysis_quarkus(setup_eclipse):
    """
    Test to run analysis on ruleset quarkus1 in Eclipse IDE
    """
    eclipse = setup_eclipse
    eclipse.open_mta_perspective()
    eclipse.run_simple_analysis(project="data_quarkus1", migration_target="quarkus1")
    assert eclipse.is_analysis_complete()
    assert eclipse.verify_story_points(target="quarkus1")
