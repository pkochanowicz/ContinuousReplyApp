# Continuous: The Far-Out Facebook Messenger Chatbot
=====================================================

**What is ContinuousReplyApp?**

ContinuousReplyApp is an open-source Python script that automates sending messages on Facebook Messenger using a local LLaMA model. This script uses the Playwright library to interact with the browser and send responses.

**Features**

* Automate sending messages on Facebook Messenger
* Use a local LLaMA model for generating responses
* Supports multiple styles of response (e.g., "Who are we today?")

**Requirements**

* Python 3.12+
* `playwright` library (`pip install playwright`)
* `requests` library (`pip install requests`)
* Local LLaMA model setup

**Setup**

1. Create a new file called `config.txt` and add your local LLaMA model URL.
2. Run the script using `python main.py`.

**How it Works**

1. The script reads the configuration from the `config.txt` file.
2. It launches a Google Chrome browser instance and logs in to Facebook Messenger.
3. When a new message is received, the script generates a response using the local LLaMA model.
4. The response is then sent back to the sender.

**Styles of Response**

To change the style of response, simply enter your preferred style when prompted by the script (e.g., "Who are we today?").

**Example of use:**
https://www.youtube.com/watch?v=XJo8JXx7k60 - two bots chatting

**Troubleshooting**

* If the script fails to launch the browser or log in to Facebook Messenger, ensure that you have the correct configuration and that Playwright is installed.
* If the script fails to generate a response, check that your local LLaMA model is set up correctly.

**Code Structure**

The code is organized into several classes and functions:

* `LLamaClient`: A class for interacting with the local LLaMA model.
* `run_messenger`: A function for launching the browser and logging in to Facebook Messenger.
* `receive_message`: A function for receiving messages from Facebook Messenger.
* `get_response`: A function for generating responses using the local LLaMA model.
* `write_fb_message`: A function for sending responses back to the sender.

**License**

ContinuousReplyApp is released under the MIT License. See LICENSE.md for details.