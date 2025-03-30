# Youtube Comment Remove about Gambling (e.g., MAX33) in Thai language

This project utilizes Artificial Intelligence (AI) to analyze the meaning of user comments and determine whether they are related to gambling. The analysis is performed using a Bayesian Networks Model, which has achieved a high overall accuracy rate of 92%.

## Pre-requisites

You need two things for this to work:


1. To setup an OAuth client id in the [Google Developer Console](https://console.cloud.google.com/apis/credentials).
    * You will need to create a project, but you can use an account other than the one you wish to delete comments from if you wish.
    * You will need to configure an OAuth consent screen, just filling in the required stuff should be fine.
    * You will need to add yourself and anyone else that will be using this app as test users.
    * Once you have finished creating the OAuth client config, dowload the secret file, name it `creds.json` and place it in the top directory of the repo.
    * Once the OAuth client config is done enable the [Youtube Data API V3](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
## Getting Started

### Installation
Ensure your environment is:
- Python >= 3.8
  Install wheel by `pip install wheel`

Then, install the remaining requirements with `pip install -r requirements.txt`.
For the gradio demo, an additional `pip install -r requirements-demo.txt` is required.
1. Clone the repository
   git clone https://github.com/your-username/your-repo.git
cd your-repo
2. (Optional) Create a virtual environment
   python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
3. Install dependencies
   pip install -r requirements.txt
## Running

On a machine with a valid Python installation (I tested on version 3.10.6) run `python main.py` and enter the requested information.
* The path to your takeout folder should be the top level folder you get upon extracting the zip file.
* If you get path errors you may need to mess around with the values in the `CommentDeleter` class.
* I ran this in a conda environment, but venv should also work fine.  If you run on iOS or Linux some of the packages in the requirements file may be platform specific to Windows.

## Clean-up

Once you are done deleting your comments its best to delete your API key if you do not expect to keep using it.
