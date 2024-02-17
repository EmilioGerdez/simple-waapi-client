Simple WhatsApp Chatbot with Flask and waapi (Python)
This project is a simple Python-based chatbot demonstrating communication with WhatsApp through the waapi API using Flask and requests libraries. It showcases basic functionality for sending and receiving text messages, along with a menu structure utilizing a dictionary (rutas).

Key Features:

Sends and receives text messages via WhatsApp using waapi API.
Implements a basic menu system with options and submenus using a dictionary.
Demonstrates usage of Flask for web application handling.
Includes sample code for easy understanding and potential expansion.
Project Setup:

Clone the repository:
git clone https://github.com/EmilioGerdez/simple-waapi-client
Install dependencies:
pip install Flask requests python-dotenv
Create .env file:
Replace placeholders with your actual waapi token and phone number.
Example .env content:
WAAPI_TOKEN=YOUR_TOKEN
WAAPI_INSTANCE=YOUR_INSTANCE_ID
Run the application:
python app.py
Menu example:

The rutas dictionary in app.py defines the menu structure. You can customize this to create your own interactive functionalities.

Please note that sending messages without user consent might violate WhatsApp policies. Use this project responsibly and adhere to ethical guidelines.

Further considerations:

This is a basic example. You can expand it to handle attachments, media, multimedia messages, persistent storage, etc.
Implement error handling and validation for robust functionality.
Consider authentication and security measures for production environments.
I hope this helps! Feel free to modify and personalize this project.
