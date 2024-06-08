# Dash Dashboard Project

![Cloud](pics\image.png)

![Cloud](pics\image1.png)

## Project Overview

This project involves creating an interactive dashboard using Plotly Dash. The dashboard visualizes data and provides insights through various graphs and charts.

## Features

- Interactive data visualizations
- Real-time data updates
- User-friendly interface
- Customizable layout (soon cross filtering between bubble chart and remaining graphs)

## Installation

1. Clone the repository:
    ```sh
    git clone 
    ```
2. Navigate to the project directory:
    ```sh
    cd dash-dashboard
    ```
3. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```
2. Open your web browser and go to:
    ```
    http://127.0.0.1:8050
    ```

## Project Structure

(data is only for testing, this isnt the original source)

```
dash_dashboard/
├── app.py
├── data/
│   └── house_price_data_20-05-2024.parquet
├── layouts.py
├── utils.py
├── requirements.txt
└── assets/
    └── style.css
```


| Directory/File    | Description                           |
|-------------------|---------------------------------------|
| `app.py`          | Main application file                 |
| `assets/`         | Directory for CSS and JavaScript files|
| `data/`           | Directory for data files              |
| `components/`     | Directory for custom Dash components  |
| `layouts/`        | Directory for layout definitions      |

