# AI-Trading-Hints

## Table of Contents

  * About The Project
  * Features
  * Getting Started
      * Prerequisites
      * Installation
      * API Key Setup
  * Usage
  * How it Works
  * Contributing
  * License
  * Contact
  * Acknowledgments

## About The Project

**AI-Trading-Hints** is a user-friendly desktop application designed to assist cryptocurrency traders and enthusiasts by providing AI-driven analysis of candlestick charts. Built with Python and Tkinter, it allows users to generate customizable charts and then leverages a vision-capable AI model to interpret the chart patterns and suggest potential trading signals.

This tool aims to offer quick, AI-assisted insights into market trends and common price action patterns, helping users make more informed trading decisions.

## Features

  * **Customizable Chart Generation:** Easily select cryptocurrency pairs (e.g., BTC/USDT, ETH/USDT), various timeframes (1h, 4h, 1d, 1w), and the number of historical candles to analyze.
  * **Interactive Candlestick Charts:** Generates and displays clear, resizable candlestick charts directly within the application's GUI.
  * **AI-Powered Chart Analysis:** Integrates with a multimodal AI model to perform sophisticated analysis of the generated chart image.
  * **Customizable AI Prompt:** Empower the AI's analysis by providing your own specific instructions or patterns to look for, such as "Seek common price action patterns like triangles, wedges, breakthroughs, Double Bottoms, Double Tops."
  * **Structured Trading Hints:** Receives and displays a concise, formatted trading hint from the AI, including proposed position type (Long, Short, None), current price, calculated stop-loss, and take-profit targets with percentages, accompanied by a brief explanation.
  * **Intuitive Graphical User Interface (GUI):** A clean and responsive interface built with Tkinter ensures ease of use.

## Getting Started

To get a copy of the project up and running on your local machine, follow these simple steps.

### Prerequisites

  * Python 3.8+
  * `pip` (Python package installer)
  * **Chrome or Chromium browser**: Required by the `kaleido` package for image export.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DrSavalan/AI-Trading-Hints.git
    cd AI-Trading-Hints
    ```
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
      * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
      * On Windows:
        ```bash
        venv\Scripts\activate
        ```
4.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need a `requirements.txt` file. If you don't have one, run `pip freeze > requirements.txt` in your activated virtual environment after installing necessary libraries like `openai`, `Pillow`, `python-dotenv`, `plotly`, `kaleido`, `pandas`, `numpy`, and `ccxt`.)*

### API Key Setup

This project requires an API key for an AI service. By default, the code is configured to use **AvalAI**. This choice is particularly beneficial for users in regions like Iran, where direct access to OpenAI's services might be limited due to international restrictions. AvalAI provides an OpenAI-compatible endpoint, allowing users to leverage these powerful models.

  * **For users in Iran:** Obtain your API key from AvalAI (their service is designed to provide access to models like GPT-4o without direct IP restrictions).
  * **For other users:** You can obtain an API key directly from OpenAI.

<!-- end list -->

1.  **Create a `.env` file:** In the root directory of your project (the same location as `main.py` or your main application file), create a file named `.env`.
2.  **Add your API key to `.env`:**
    ```
    API_KEY=YOUR_ACTUAL_API_KEY_HERE
    ```
    **Important:** Do NOT share or commit this `.env` file to your Git repository\! Ensure `.env` is listed in your `.gitignore` file.

**Connecting to OpenAI Directly (for users outside restricted regions):**
If you are located outside regions with direct OpenAI access limitations and prefer to connect directly to OpenAI's API, you will still use the same `API_KEY` environment variable. However, you will need to **remove or comment out the `base_url` argument** in the `OpenAI` client initialization in your `main.py` (or equivalent file).

Original code (for AvalAI):

```python
client = OpenAI(
    api_key=api_key,
    base_url="https://api.avalai.ir/v1",
)
```

Modified code (for direct OpenAI):

```python
client = OpenAI(
    api_key=api_key,
    # base_url="https://api.avalai.ir/v1", # Comment out or remove this line
)
```

By default, the OpenAI Python client connects to OpenAI's official API endpoint if `base_url` is not specified.

## Usage

1.  **Run the application:**

    ```bash
    python main.py # Or whatever your main script is named
    ```

    (Ensure your virtual environment is activated.)

2.  **Select Parameters:** Use the dropdowns to choose your desired cryptocurrency, timeframe, and the number of candles.

3.  **Enter Custom Prompt (Optional):** Type specific instructions or patterns you want the AI to focus on in the "Custom Prompt" text box.

4.  **Generate Hint:** Click the "Generate Chart & Get Hint" button.

5.  **View Results:** The candlestick chart will be displayed, and the AI's trading hint will appear in the "Trading Hint" text box.

## How it Works

The application orchestrates the following steps:

1.  **User Input:** Gathers selected crypto, timeframe, limit, and any custom prompt.
2.  **Chart Generation:** The `price_data.py` module fetches historical OHLCV (Open, High, Low, Close, Volume) data for the specified cryptocurrency, timeframe, and limit using the `ccxt` library (defaulting to KuCoin).
3.  **Plotly Visualization:** The fetched data is transformed into a Pandas DataFrame, and a candlestick chart is created using Plotly.
4.  **Image Saving (Kaleido):** The Plotly figure is then saved as a PNG image (`test.png`) using the `kaleido` package, which facilitates static image export from Plotly.
5.  **Image Encoding:** The `test.png` image is encoded into a Base64 string.
6.  **AI API Call:** The Base64 encoded image and the user's comprehensive text prompt are sent to a vision-capable AI model via the configured API endpoint (either AvalAI for regions with restrictions like Iran, or directly to OpenAI for others).
7.  **Hint Display:** The AI's response, containing the structured trading hint, is received and displayed in the application's GUI.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

DrSavalan
Your Email - mechsavalan@gmail.com (optional)

Project Link: [https://github.com/DrSavalan/AI-Trading-Hints](https://www.google.com/search?q=https://github.com/DrSavalan/AI-Trading-Hints)

## Acknowledgments

  * Tkinter
  * OpenAI Python Library
  * AvalAI (a service enabling access to AI models in regions with restrictions)
  * Matplotlib
  * Pandas
  * Plotly
  * Kaleido
  * python-dotenv
  * Pillow
  * ccxt
