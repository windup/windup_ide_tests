from src.lib.base_desktop import BaseDesktop
import logging


class CodeReadyStudio(BaseDesktop):
    """
        Library for defining the basic functionalities
        adapted for usage with CodeReadyStudio IDE
    """

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in IDE

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type='image',
                                   locator='mta_perspective.png')
            return True
        except Exception as exc:
            logging.debug('An error occured while finding \
                MTA perspective tab ! {}'.format(str(exc)))
            if 'No matches found' in str(exc):
                return False
            else:
                raise Exception(exc)

    def open_mta_perspective(self):
        """
        Opens MTA perspective in IDE
        """
        if self.is_open_mta_perspective():
            logging.info('MTA perspective is already opened !')
            return
        else:
            """
            Click on Window -> Perspective -> Open Perspective
            -> Other -> MTA -> Click on Open button
            """
            self.click_element(locator_type='text', locator='Window')
            self.click_element(locator_type='text', locator='Perspective')
            self.click_element(locator_type='image',
                               locator='open_perspective.png')
            try:
                self.click_element(locator_type='text', locator='Other...')
            except Exception as exc:
                # Re-attempt to click 'Other' using image locator
                if 'No matches found' in str(exc):
                    self.click_element(locator_type='image',
                                       locator='other_alt.png')
                else:
                    raise Exception(exc)
            self.click_element(locator_type='image',
                               locator='open_perspective_header.png')
            self.type_text(text='mta')
            open_perspective_button = self.image_locator('open_button.png')
            self.move_mouse(open_perspective_button)
            self.click(action='double_click')

    def run_simple_analysis(self, project='weblogic', packages=[]):
        """
        Runs analysis by adding the project and/or packages passed as argument

        Args:
            project (str): Full name of project to be analysed
            packages (list): List of packages to be added to analysis

        Returns:
            None
        """
        """
        Click on Run MTA Configuration icon -> Add Project button
        -> Type Project name -> Click on OK button
        Confirm analysis has started by finding generating report
        """
        self.click_element(locator_type='image', locator='mta_run.png')
        self.click_element(locator_type='image',
                           locator='run_conf_header.png')
        # Region defining the Add Project Button
        self.click_element(locator_type='region',
                           coordinates=[1371, 364, 1441, 400])
        self.click_element(locator_type='image',
                           locator='projects_header.png')
        self.type_text(text=project)
        self.wait_find_element(locator_type='image',
                               locator='project_highlighted.png')
        self.click_element(locator_type='image', locator='ok_button.png')
        self.click_element(locator_type='image',
                           locator='run_config_button.png')
        self.wait_find_element(locator_type='image',
                               locator='generating_report.png')

    def is_analysis_complete(self):
        """
        Checks if run analysis has been completed

        Returns:
            bool: True if analysis was completed
        """
        self.wait_find_element(locator_type='image',
                               locator='run_complete.png',
                               timeout=120.0, interval=5.0)
        return True
