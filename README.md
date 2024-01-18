# kraka-rk

1. Download and Install Python:

Visit the Python website: https://www.python.org/downloads/: https://www.python.org/downloads/
Click the button that says "Download the latest version for Mac OS X"
Run the installer: Double-click the downloaded file and follow the on-screen instructions.

2. Install Git:

Download the Git installer for Mac: https://git-scm.com/download/mac: https://git-scm.com/download/mac
Run the installer: Double-click the downloaded file and follow the on-screen instructions.

3. Clone the GitHub Repository:

Open the Terminal app: You can find it in the Applications > Utilities folder.

Navigate to your desired directory: Use the cd command. For example, to go to your Desktop, type: cd Desktop

Clone the repository: Type the following command, replacing https://github.com/username/reponame with the actual GitHub repository URL:

Bash
git clone https://github.com/username/reponame
Use code with caution. Learn more
4. Install Anaconda or Miniconda:

Download the installer for macOS: https://www.anaconda.com/products/distribution: https://www.anaconda.com/products/distribution
Run the installer: Double-click the downloaded file and follow the on-screen instructions.
5. Create a Conda Environment:

Open the Terminal app:

Create the environment: Type the following command:

Bash
conda create -n kraka-env -f kraka-environment.yml
Use code with caution. Learn more
6. Activate the Environment:

Type the following command:

Bash
conda activate kraka-env
Use code with caution. Learn more
7. Install Dependencies with Pip:

Navigate to the cloned repository: Use the cd command.

Install dependencies: Type the following command:

Bash
pip install -r requirements.txt
Use code with caution. Learn more
8. Run python -W ignore main.py --read ./input-stp-files/test2.stp

Type the following command:

Bash
python main.py
Use code with caution. Learn more
