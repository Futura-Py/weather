<h1 align="center">Future Weather</h1>

A simple weather app that uses the OpenWeatherMap API to get the weather for a given city. 

## Installation

To run this app, you will need Python 3 installed on your computer. Clone this repository and navigate to the directory containing the `main.py` file. 

Use the following command to install the required packages:
```bash
pip install -r requirements.txt
```


Once the packages are installed, you can run the app using the following command:

```bash
python3 main.py
```
or
```bash
py3 main.py
```


## Usage

When you run the app, a window will open with a search bar, a label to display the weather information, and two buttons. 

To search for the weather in a city, simply enter the name of the city in the search bar and click the "Search for City" button. The app will display the temperature in Celsius for that city in the label. 

To exit the app, click the "Exit" button. 

# Documentation

Additionally, the code contains several functions, methods, and classes:

### `self_return_decorator()`
A decorator function that allows for chaining of methods. This function takes a method as an argument and returns a new function that calls the original method and returns the instance of the class.

### `App()`
A class that inherits from the Tk class and defines the main window of the app. The __init__ method sets up the menubar, window, and widgets. The about, resize_app, exit_app, and OWMCITY methods define the behavior of the corresponding buttons in the app.

### `.about()`
A method that displays a message box with information about the app.

### `.resize_app()`
A method that uses tkinter to detect the minimum size of the app, get the center of the screen, and place the app there.

### `.exit_app()`
A method that exits the app.

### `.OWMCITY()`
A method that sends a request to the OpenWeatherMap API to get the weather for a given city and displays the temperature in Celsius in the label. If the city is not found, the label displays an error message.

# Final Notes

## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request. 
## Pre-Commit Actions

Before making any commits, run the following command:

```bash
black .; isort .; ruff . --fix
```

This will automatically format the code to follow the PEP 8 style guide and run several linters to catch any errors or warnings

## License

This project is licensed under the MIT License. See the LICENSE file for details.