import logging
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from src.lib.config import config_data


class WebBrowser:
    """
    Class for handling browser related functionalities using selenium webdriver
    """

    def __init__(self, browser):
        path = self._get_driver_path(browser)
        if browser == "firefox":
            self.driver = webdriver.Firefox(executable_path=path)
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path=path)

    def close_browser(self):
        """
        Closes all the window handles opened by driver
        """
        self.driver.quit()

    def explicit_wait(self, timeout=30):
        """
        Returns explicit wait object

        Args:
            timeout (int): The time to wait for

        Returns:
            (object): Instance of WebDriverWait
        """
        return WebDriverWait(self.driver, timeout)

    def _get_workspace_username(self):
        """
        Returns workspace username

        Args:
            None

        Returns:
            username (str): The username to login into workspace
        """
        username = config_data["workspace_credentials"]["username"]
        return username

    def _get_workspace_password(self):
        """
        Returns workspace password

        Args:
            None

        Returns:
            password (str): The password to login into workspace
        """
        password = config_data["workspace_credentials"]["password"]
        return password

    def _get_driver_path(self, browser):
        """
        Returns path to webdriver executable

        Args:
            browser (str): The browser for which executable paths needs to be returned

        Returns:
            driver_path (str): The path to webdriver executable
        """
        driver_path = config_data["driver_paths"][browser]
        return driver_path

    def open_url(self, url):
        """
        Opens the url using webdriver

        Args:
            url (str): The url to open

        Returns:
            None
        """
        self.driver.get(url)

    def wait_click_element(self, by_locator_strategy, locator, timeout=30):
        """
        Finds the element by waiting for its visibility and clicks it

        Args:
            by_locator_strategy (By class property): By strategy for finding element,
                                                     example - By.XPATH, By.ID, By.NAME etc.
            locator (string): Value of locator to search element
            timeout (int): Time to wait for element visibility in seconds

        Returns:
            None
        """
        ele = self.wait_find_element(by_locator_strategy, locator, timeout)
        ele.click()

    def wait_find_element(self, by_locator_strategy, locator, timeout=30):
        """
        Finds the element by waiting for its visibility

        Args:
            by_locator_strategy (By class property): By strategy for finding element,
                                                     example - By.XPATH, By.ID, By.NAME etc.
            locator (string): Value of locator to search element
            timeout (int): Time to wait for element visibility in seconds

        Returns:
            ele (WebElement): WebElement object corresponding to element found
        """
        wait = self.explicit_wait(timeout=timeout)
        ele = wait.until(
            expected_conditions.visibility_of_element_located((by_locator_strategy, locator)),
        )
        return ele

    def wait_switch_frame(self, by_locator_strategy, locator, timeout=30):
        """
        Finds the iframe element by waiting for its visibility and switches to it

        Args:
            by_locator_strategy (By class property): By strategy for finding iframe,
                                                     example - By.XPATH, By.ID, By.NAME etc.
            locator (string): Value of locator to search iframe
            timeout (int): Time to wait for iframe visibility in seconds

        Returns:
            frame_ele (WebElement): WebElement object corresponding to iframe found
        """
        wait = self.explicit_wait(timeout=timeout)
        frame_ele = wait.until(
            expected_conditions.frame_to_be_available_and_switch_to_it(
                (by_locator_strategy, locator),
            ),
        )
        return frame_ele

    def write_text(self, by_locator_strategy, locator, text, timeout=30):
        """
        Writes text into the writable element (textbox or textarea) after waiting and finding it

        Args:
            by_locator_strategy (By class property): By strategy for finding element,
                                                     example - By.XPATH, By.ID, By.NAME etc.
            locator (string): Value of locator to search element
            text (string): The text to write
            timeout (int): Time to wait for element visibility in seconds

        Returns:
            None
        """
        ele = self.wait_find_element(by_locator_strategy, locator, timeout)
        ele.click()
        ele.clear()
        ele.send_keys(text)


class EclipseChe(WebBrowser):
    """
    Class for managing Eclipse CHE specific functionalities
    """

    def __init__(self, browser):
        super().__init__(browser)
        self.configuration_name = None
        self.configuration_ele_locator = None

    def create_run_configuration(self):
        """
        Creates run configuration for MTA
        """
        self.driver.switch_to.default_content()
        self.wait_switch_frame(By.ID, "ide-application-iframe", 60)
        # Click on MTA Explorer icon
        mta_plugin_ele = self.wait_find_element(
            By.XPATH,
            "//div/ul[@class='p-TabBar-content']\
            /li[@id='shell-tab-plugin-view-container:rhamt-explorer']",
            120,
        )
        mta_icon_click_counter = 2
        if "p-mod-current" not in mta_plugin_ele.get_attribute("class"):
            mta_icon_click_counter = 3
        for _ in range(mta_icon_click_counter):
            mta_plugin_ele.click()
        # Create new run configuration
        self.wait_click_element(By.XPATH, "//div[@title='New Configuration']")
        # Wait for all the page frames to load
        time.sleep(20)
        # Switch to the last frame to find main html content for configuration
        self.wait_switch_frame(By.TAG_NAME, "iframe")
        self.wait_switch_frame(By.XPATH, "//iframe[@id='active-frame']", 60)
        self.wait_switch_frame(By.TAG_NAME, "iframe")
        config_name_ele = self.wait_find_element(By.XPATH, "//input[@id='name-input']")
        self.configuration_name = config_name_ele.get_attribute("value")
        self.driver.switch_to.default_content()
        self.wait_switch_frame(By.ID, "ide-application-iframe", 60)
        config_ele_locator = self.wait_find_element(
            By.XPATH,
            "//div[@class='ReactVirtualized__Grid__innerScrollContainer' and @role='rowgroup']\
                //div[@class='noWrapInfoTree']/span[contains(text(), '{}')]".format(
                self.configuration_name,
            ),
        )
        self.configuration_ele_locator = config_ele_locator

    def handle_login_interrupt(self):
        """
        Handles error card appearing ocassionally before and after login
        """
        try:
            login_failed_header = self.driver.find_element_by_xpath(
                "//h1[contains(text(), 'We are sorry')]",
            )
            if login_failed_header.is_displayed():
                self.driver.refresh()
        except Exception:
            logging.debug("Login interruption did not occur !")
            return

    def open_workspace(self):
        """
        Opens the Eclipse CHE workspace
        """
        self.open_url(url=config_data["workspace_url"])
        self.driver.maximize_window()
        # Click on Login Dev Sandbox link
        self.wait_click_element(by_locator_strategy=By.XPATH, locator="//a[text()='DevSandbox']")
        self.handle_login_interrupt()
        # Perform user login
        self.wait_find_element(By.XPATH, "//div[@class='kc-card']")
        login_username = self._get_workspace_username()
        self.write_text(By.XPATH, "//input[@id='username']", login_username)
        # Click on Next button
        self.driver.find_element_by_xpath("//button[@id='login-show-step2']").click()
        login_password = self._get_workspace_password()
        self.write_text(By.XPATH, "//input[@id='password']", login_password)
        # Click Login button
        self.driver.find_element_by_xpath("//input[@id='kc-login']").click()
        self.handle_login_interrupt()
        # Wait for workspace to load and click on che-ide-tests workspace
        self.wait_find_element(By.XPATH, "//span[@class='che-toolbar-title-label']", 60)
        self.wait_click_element(By.XPATH, "//span[contains(text(), 'che-ide-tests')]")
        workspace_status_ele = self.wait_find_element(By.XPATH, "//span[@id='workspace-status']")
        workspace_status = str(workspace_status_ele.text).lower()
        final_workspace_status = ""
        if workspace_status == "stopped":
            self.driver.find_element_by_xpath("//button[contains(text(), 'Run')]").click()
        elif workspace_status == "running":
            final_workspace_status = "running"
        cutoff = time.time() + 150
        while workspace_status == "stopped" or workspace_status == "starting":
            status_ele = self.driver.find_element_by_xpath("//span[@id='workspace-status']")
            current_status = str(status_ele.text).lower()
            if current_status == "running":
                final_workspace_status = current_status
                break
            if time.time() > cutoff:
                break
            time.sleep(2)
        if final_workspace_status != "running":
            raise Exception("The workspace could not be started !")
        self.wait_click_element(By.XPATH, "//a[contains(text(), 'Open')]")
        # Check workspace frame has loaded
        self.wait_switch_frame(By.ID, "ide-application-iframe", 90)

    def run_analysis(self, migration_target="quarkus1"):
        """
        Runs analysis on project in eclipse che workspace and returns story points

        Args:
            migration_target (str): Migration target for project analysis

        Returns:
            story_points (str): Story points for project analysis
        """
        if self.configuration_name is None and self.configuration_ele_locator is None:
            raise Exception("Configuration has not been created !")
        self.driver.switch_to.default_content()
        self.wait_switch_frame(By.ID, "ide-application-iframe")
        # Switch to the last frame to find main html content for configuration
        self.wait_switch_frame(By.TAG_NAME, "iframe")
        self.wait_switch_frame(By.XPATH, "//iframe[@id='active-frame']", 60)
        self.wait_switch_frame(By.TAG_NAME, "iframe")
        # Enter project name and select migration_target
        self.wait_click_element(By.XPATH, "//span[@id='input-details']/dl/dd/div/a")
        self.write_text(
            By.XPATH, "//input[@id='editDialogInput']", config_data["workspace_project_path"],
        )
        self.driver.find_element_by_xpath("//input[@id='editDialogInput']").send_keys(Keys.ENTER)
        self.wait_click_element(By.XPATH, "//input[@id='target-{}']".format(migration_target))
        # Run the configuration from sidebar
        self.driver.switch_to.default_content()
        self.wait_switch_frame(By.ID, "ide-application-iframe")
        action = ActionChains(self.driver)
        # Right click action and run the analysis
        action.context_click(self.configuration_ele_locator).perform()
        self.wait_click_element(
            By.XPATH, "//div[@class='p-Widget p-Menu']/ul/li/div[contains(text(), 'Run')]",
        )
        # Wait for analysis to start
        self.wait_find_element(
            By.XPATH,
            "//div[@class='theia-notifications-container theia-notification-toasts open']\
                //span[contains(text(), 'Analysis in progress')]",
            60,
        )
        # Wait for analysis to complete
        self.wait_find_element(
            By.XPATH,
            "//div[@class='theia-notifications-container theia-notification-toasts open']\
                //span[contains(text(), 'Analysis complete')]",
            120,
        )
        # Open report
        self.wait_click_element(
            By.XPATH,
            "//div[@class='theia-notifications-container theia-notification-toasts open']\
                //button[contains(text(), 'Open Report')]",
        )
        time.sleep(3)
        # Switch to report tab and get story points
        self.driver.switch_to.window(self.driver.window_handles[1])
        story_points = self.wait_find_element(By.XPATH, "//span[@class='points']").text
        # Switch back to workspace tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        return story_points

    def delete_configuration(self, configuration_name):
        """
        Deletes the configuration based on its name

        Args:
            configuration_name (str): The name of configuration to be deleted

        Returns:
            None
        """
        self.driver.switch_to.default_content()
        self.wait_switch_frame(By.ID, "ide-application-iframe")
        config_to_delete = self.wait_find_element(
            By.XPATH,
            "//div[@class='ReactVirtualized__Grid__innerScrollContainer' and @role='rowgroup']\
                //div[@class='noWrapInfoTree']/span[contains(text(), '{}')]".format(
                configuration_name,
            ),
        )
        action = ActionChains(self.driver)
        # Right click and delete configuration
        action.context_click(config_to_delete).perform()
        self.wait_click_element(
            By.XPATH, "//div[@class='p-Widget p-Menu']/ul/li/div[contains(text(), 'Delete')]",
        )
