from enum import Enum


class VSCodeCommandEnum(Enum):
    CLEAR_ALL_NOTIFICATIONS = "Notifications: Clear All Notifications"
    FOCUS_NOTIFICATIONS = "notifications: Show Notifications"
    FOCUS_ON_OUTPUT_VIEW = "Output: Focus on Output View"
    FOCUS_ON_EXPLORER_VIEW = "MTA: focus on explorer view"
    REFRESH_CONFIGURATIONS = "MTA: Refresh Configurations"
    DELETE_CONFIGURATIONS = "MTA: Delete"
    FOCUS_ON_PROBLEMS_VIEW = "Problems: Focus on Problems View"
    RUN_ANALYSIS = "MTA: Run"
