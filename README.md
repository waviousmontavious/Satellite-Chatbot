# Satellite Chatbot
**A clever little bot for our satellite operators**

## Installation
1. CD into the cloned git repo and run `$ python -m venv .env`
2. Activate the virtual environment with the command `$ .env\Scripts\activate.bat`  
    a. If a pip upgrade is needed, run `$ python -m pip install --upgrade pip`
3. Install the required packages with `$ pip install -r requirements.txt`
4. Run the command `$ rasa train` to create the model and confirm a working installation

#### Rasa X (Optional)
With Rasa X, you can interact with the bot through your browser.  
To install:  
`$ pip install rasa-x --extra-index-url https://pypi.rasa.com/simple`  
To install with pip version > 20.2:  
`$ pip install --use-deprecated=legacy-resolver rasa-x --extra-index-url https://pypi.rasa.com/simple`  
To run Rasa X:  
`$ rasa x`  
This should open a browser tab to `http://localhost:5002`

## Usage

To interact with the bot through a CLI, start by running the actions server with
`$ rasa run actions`  
Then, open and new terminal, activate the environment, and run
`$ rasa shell` to start the bot

## Examples

_Examples of Q&As_