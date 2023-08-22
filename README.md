# windup_ide_tests

## About the project
This project is for creating automated tests for verifying the functionality of MTA IDE plugin. This is an extension of [windup_integration_test](https://github.com/windup/windup_integration_test) extensively created for coverage of IDEs. Currently below IDEs have been covered:

| IDE           | Version  |
| ------------- |----------|
| Eclipse IDE for J2EE developers  | 2023-03  |
| VS Code  | 1.54.1   |
| Eclipse CHE  | theia    |
| IntelliJ IDEA  | 2022.3.1 |

**Supported OS**

Works on *Linux/RHEL/Fedora* with X11 windowing system enabled (does not work with Wayland scheme)

## Getting Started
To get started with project in development mode or basic usage, follow the below steps:

**Pre-requisites**

- Python 3+ installed
- JDK 11 installed, if there are multiple JDK version installed on the system, make sure JDK 11 is set as the default
- Respective IDE (to be tested) installed on local machine
- MTA IDE plugin installed in that IDE
- The project to be analysed is imported in IDE
   - this project can be used [Windup rulesets](https://github.com/midays/windup-rulesets)

**Installation**

1. Clone the forked repository and move to repo home
    ```
    git clone https://github.com/<user>/windup-ide-tests.git
    cd windup-ide-tests
    ```
2. Create python3 virtual env

    `python3 -m venv .ide_env`

3. Activate virtual env

    `source .ide_env/bin/activate`

4. Install from setup

    `pip install .`
5. Edit the **ide_config.json** file and provide full paths to the windup CLI, and to the windup-rulesets project

    `cd ~/windup_ide_tests/src/conf`

6. For each IDE, there exists a relevant config file under **src/config/<ide>_config.json**. Make sure to update the fields as required
   1. **ide_path**: The path to the IDE executable
   2. **plugin_cache_path**: The path to the cache folder should be under `~/.windup/tooling/<ide>/`

**Contributing to the project**

1. Fork the repository
2. Clone the forked repo `git clone https://github.com/<user>/windup-ide-tests.git`
3. Run the aforementioned installation steps
4. Create new branch `git checkout -b <new_branch_name>`
5. Run pre-commit check `pre-commit run -a`
6. Commit the changes `git commit -m 'Explanatory commit message'`
7. Push your changes to branch `git push origin <new_branch_name>`
8. Open new pull request

## License
Distributed under Eclipse Public License. See [LICENSE](https://github.com/nitishSr/windup-ide-tests/blob/main/LICENSE) for more information.
