<h1 align="center">Futura Weather</h1>

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

To search for the weather in a city, simply enter the name of the city in the search bar and click the "Search for City" button. The app will display the status of weather, followed by maximum, minimum and current temperature with how the temperature feels, and following that presents the humidity, pressure, visibility and wind speed in respective labels. The name of the city will be added above the search bar, in its respective label.

To exit the app, click the "Exit" button. 

# Documentation

Additionally, the code contains several functions, methods, and classes:

### `App()`
A class that inherits from the Tk class and defines the main window of the app. The __init__ method sets up the menubar, window, and widgets. The about, resize_app, exit_app, and OWMCITY methods define the behavior of the corresponding buttons in the app.

#### `.about()`
A method that displays a message box with information about the app.

#### `.resize_app()`
A method that uses tkinter to detect the minimum size of the app, get the center of the screen, and place the app there.

#### `.reset_app()`
This method clears all the labels or can take an input of 9 strings in a list and set each label to the corresponding string.

#### `.OWMCITY()`
A method that sends a request to the OpenWeatherMap API to get the weather for a given city. Once the data is recieved, the method determines wether the call worked and if not, updates the city label correspondingly. If the API call does indeed succeed, it will update the labels by calling `.update_labels()` with a list of 9 strings corresponding to the data recieved. Note that because the application allows changing of units from Celsius to Fahrenheit (Metric/Imperial), it will run some calculations to convert the data to the proper units.

#### `.update_labels()`
This method takes an input of 9 strings which default to all empty strings that allow the application to modify the weather info labels with one's desired text.

#### `.update_settings()`
This method runs when a user uses one or the other settings dropdowns and it determines if a setting was changed and, if so, it updates the settings file accordingly and updates any labels to the proper units or the color theme to the chosen one.

## Contributing

Contributions are welcome! If you find a bug, typo, or have an idea for a new feature, please open an [issue](https://github.com/Futura-Py/weather/issues/new) or submit a [pull request](https://github.com/Futura-Py/weather/compare). 
## Pre-Commit Actions

Before making any commits, run the following command:

```bash
black .; isort .; ruff . --fix
```
Or, if you have the [`just` command runner](https://just.systems/) installed:
```bash
just format
```

This will automatically format the code to follow the PEP 8 style guide and run several linters to catch any errors or warnings

## License

This project is licensed under the MIT License. See the LICENSE file for details.