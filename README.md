# Satellite Chatbot
**A clever little bot for our satellite operators**

## Installation
1. CD into the cloned git repo and run `$ python -m venv .env`
2. Activate the virtual environment with the command `$ .env\Scripts\activate.bat`  
    a. If a pip upgrade is needed, run `$ python -m pip install --upgrade pip`
3. Install the required packages with `$ pip install -r requirements.txt`
4. Install the English model with `$ python -m spacy download en_core_web_sm`
5. Run the command `$ rasa train` to create the model and confirm a working installation

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

### Diagnostic Form
To initiate the diagnotic questions, tell the bot something like _"something is wrong"_ or 
_"what is wrong with my weather satellite"_  
**Example:**  
<pre>
    Your input ->  oh no! something is wrong!
    Did you get an alert?
    Your input ->  yes , I did
    Enter the Failure ID (Number between 1 and 15)
    Your input ->  okay, the FID is 13
    The Spacecraft has rejected a command from ground
</pre>

### Sensor Info
To ask the bot about sensors on the satellite, you can say something like 
_"show me the sensors"_ or _"what sensors are on the satellite"_  

Then you ask about a specific sensor for more details

**Example:**
<pre>
    Your input ->  show me the sensors
    Our current sensor list is as follows:
    --------------------------------------------
    solar ultraviolet imager
    space environmental in-situ suite
    magnetometer
    extreme ultraviolet x-ray irradiance sensor
    advanced baseline imager sensor
    --------------------------------------------
    Feel free to ask about any sensor
    Your input ->  what does the advanced baseline imager sensor do?
    The Advanced Baseline Imager is the primary instrument for imaging Earth's weather, 
    oceans and environment. ABI views Earth with three times more spectral channels, 
    four times the resolution, and five times faster scanning that previous GOES.
</pre>

### Asking for Weather
You can also ask for the current weather in a city

**Example:**
<pre>
    Your input ->  how is the weather in Los Angeles
     Temperature (in kelvin unit) = 283.42
     Atmospheric pressure (in hPa unit) = 1021
     Humidity (in percentage) = 67
     Description = broken clouds
</pre>

### Other Example Questions the Bot can Answer
- What time of day will I have access to the satellite?
- how will the weather affect my satellite?
- how fast does my satellite transmit data?
- is my satellite maintaining orbit?
- what orbit is my satellite in?
- when did my satellite launch?
- when does my satellite need to be replaced?
- what day does the mission for this satellite end?
- who was this satellite built by?
- what is the name of this satellite?
- how much does this satellite cost?
- what is your name?