import time


def test_run_analysis(setup_intellij):
    configuration_name = "test_configuration"
    intellij = setup_intellij
    time.sleep(5)
    intellij.open_mta_perspective()
    time.sleep(3)
    intellij.run_simple_analysis(configuration_name)
    intellij.is_analysis_complete()
# region old tests
# def test_analysis_eap(setup_intellij):
#     """
#     Test to run analysis for migration path Anything to EAP 7 in IntelliJ IDE
#     """
#     intellij = setup_intellij
#     time.sleep(5)
#     intellij.open_mta_perspective()
#     # Intellij freezes without this sleep
#     time.sleep(3)
#     # todo: set the projects selection to be done dynamically instead of manually adding to config
#     intellij.run_simple_analysis(
#         project=config_data["project_paths"]["eap7_generic"],
#         migration_target="eap7",
#     )
#     assert intellij.is_analysis_complete()
#     assert intellij.verify_story_points(target="eap7")
#
#
# def test_analysis_eapxp(setup_intellij):
#     """
#     Test to run analysis on ruleset thorntail to eapxp2 in IntelliJ IDE
#     """
#     intellij = setup_intellij
#     time.sleep(5)
#     intellij.open_mta_perspective()
#     # Intellij freezes without this sleep
#     time.sleep(3)
#     intellij.run_simple_analysis(
#         project=config_data["project_paths"]["eapxp_ruleset"],
#         migration_target="eapxp",
#     )
#     assert intellij.is_analysis_complete()
#     assert intellij.verify_story_points(target="eapxp")
#
#
# def test_analysis_quarkus(setup_intellij):
#     """
#     Test to run analysis on ruleset quarkus1 in IntelliJ IDE
#     """
#     intellij = setup_intellij
#     time.sleep(5)
#     intellij.open_mta_perspective()
#     # Intellij freezes without this sleep
#     time.sleep(3)
#     intellij.run_simple_analysis(
#         project=config_data["project_paths"]["quarkus_ruleset"],
#         migration_target="quarkus",
#     )
#     assert intellij.is_analysis_complete()
#     assert intellij.verify_story_points(target="quarkus")
#
#
# def test_install_plugin(setup_intellij):
#     """
#     Test if plugin is installed
#     """
#     intellij = setup_intellij
#     time.sleep(5)
#     intellij.open_mta_perspective()
# endregion
