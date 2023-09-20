import os
import time

from src.utils.ocr import find_all_sentence_occurrences

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


def test_plugin_info(setup_intellij):
    """
    Test if the plugin panel shows the expected information
    """
    intellij = setup_intellij
    # Intellij freezes without this sleep
    time.sleep(3)

    intellij.open_mta_plugin_info()

    # assert all the following sentences are present in the panel
    assert len(find_all_sentence_occurrences(
        "The Migration Toolkit for Applications (MTA) plugin for IntelliJ")) > 0, ("the sentence \"The Migration "
                                                                                   "Toolkit for Applications (MTA) "
                                                                                   "plugin for IntelliJ\" was not "
                                                                                   "found in the plugin info panel")
    assert len(find_all_sentence_occurrences(
        "Platform-based IDEs")) > 0, "the sentence \"Platform-based IDEs\" was not found in the plugin info panel"
    assert len(find_all_sentence_occurrences(
        "Provides tooling to accelerate application migration by marking")) > 0, ("the sentence \"Provides tooling to "
                                                                                  "accelerate application migration "
                                                                                  "by marking\" was not found in the "
                                                                                  "plugin info panel")
    assert len(find_all_sentence_occurrences(
        "migration issues in the source code, provides guidance to fix the")) > 0, ("the sentence \"migration issues "
                                                                                    "in the source code, "
                                                                                    "provides guidance to fix the\" "
                                                                                    "was not found in the plugin info "
                                                                                    "panel")
    assert len(find_all_sentence_occurrences(
        "issues, and offers automatic code replacement when possible")) > 0, ("the sentence \"issues, and offers "
                                                                              "automatic code replacement when "
                                                                              "possible\" was not found in the plugin "
                                                                              "info panel")
    assert len(find_all_sentence_occurrences(
        "Read more about MTA here")) > 0, ("the sentence \"Read more about MTA here\" was not found in the plugin info "
                                           "panel")
