import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
import base64
from openai import OpenAI
import os
from PIL import Image, ImageTk  # Import PIL for image handling

# Import your existing create_and_save_candlestick_chart function
# Ensure 'price_data.py' is in the same directory as this script
from price_data import create_and_save_candlestick_chart as cs
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file; for your safety!
# --- Configuration ---
api_key = os.getenv("API_KEY")
# --- OpenAI Configuration (from your provided code) ---
client = OpenAI(
    api_key=api_key,  # Replace with your actual AvalAI API key
    base_url="https://api.avalai.ir/v1",  # Base URL for AvalAI
)


# --- Function to encode the image to Base64 (from your provided code) ---
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image file not found: {image_path}")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error encoding image: {e}")
        return None


# --- Main GUI Application Class ---
class CryptoChartAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Chart Analyzer")
        self.geometry("1000x800")  # Adjust window size as needed for your chart and text

        # Configure the main window's grid to center content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Center horizontally

        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self, text="Chart Parameters", padding="10 10 10 10")
        input_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")  # Use grid for overall layout

        # Configure input_frame columns to center its content
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        # Cryptocurrency Symbol
        ttk.Label(input_frame, text="Cryptocurrency:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.symbols = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "LTC/USDT", "NOT/USDT", "SOL/USDT", "DOGE/USDT"]  # Add more as needed
        self.symbol_var = tk.StringVar(self)
        self.symbol_var.set(self.symbols[0])  # default value
        self.symbol_menu = ttk.OptionMenu(input_frame, self.symbol_var, self.symbols[0], *self.symbols)
        self.symbol_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Timeframe
        ttk.Label(input_frame, text="Timeframe:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.timeframes = ["1h", "4h", "1d", "1w"]  # Add more as needed
        self.timeframe_var = tk.StringVar(self)
        self.timeframe_var.set(self.timeframes[0])  # default value
        self.timeframe_menu = ttk.OptionMenu(input_frame, self.timeframe_var, self.timeframes[0], *self.timeframes)
        self.timeframe_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Limit
        ttk.Label(input_frame, text="Limit (Data Points):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.limit_var = tk.StringVar(self)
        self.limit_var.set("100")  # default value
        self.limit_entry = ttk.Entry(input_frame, textvariable=self.limit_var, width=10)
        self.limit_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # --- Custom Prompt Text Box (Multi-line) ---
        ttk.Label(input_frame, text="Custom Prompt:").grid(row=3, column=0, sticky="nw",
                                                           pady=5)  # sticky="nw" to align label to top-left of text area

        # Create the Text widget for multi-line input
        # Note: tk.Text does NOT use textvariable directly
        self.custom_prompt_text_widget = tk.Text(input_frame, wrap="word", width=50,height=5)  # height sets number of lines
        self.custom_prompt_text_widget.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        # Optional: Add a scrollbar if the text can be very long
        prompt_scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.custom_prompt_text_widget.yview)
        prompt_scrollbar.grid(row=3, column=2, sticky="ns")  # Place scrollbar next to the text widget
        self.custom_prompt_text_widget.config(yscrollcommand=prompt_scrollbar.set)  # Link text widget to scrollbar

        # Optional: Set initial text (different from Entry/StringVar)
        self.custom_prompt_text_widget.insert("1.0", "Seek common price action patterns such as triangles, "
                                                     "wedges, breakthroughs, Double Bottoms, Double Tops, or ...")


        # Generate Button
        self.generate_button = ttk.Button(input_frame, text="Generate Chart & Get Hint",
                                          command=self.process_chart_and_hint)
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=10)  # Centered due to columnspan

        # --- Chart Display Frame ---
        chart_frame = ttk.LabelFrame(self, text="Candlestick Chart", padding="10 10 10 10")
        chart_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")  # Use grid for overall layout

        # Configure chart_frame to center its content
        chart_frame.grid_rowconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(0, weight=1)

        self.chart_label = ttk.Label(chart_frame)
        self.chart_label.grid(row=0, column=0, sticky="")  # No sticky, let weight do the centering

        # --- Hint Display Frame ---
        hint_frame = ttk.LabelFrame(self, text="Trading Hint", padding="10 10 10 10")
        hint_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")  # Use grid for overall layout

        # Configure hint_frame to center its content
        hint_frame.grid_rowconfigure(0, weight=1)
        hint_frame.grid_columnconfigure(0, weight=1)

        self.hint_text = tk.Text(hint_frame, wrap="word", height=10, width=80, font=("Arial", 10))
        self.hint_text.grid(row=0, column=0, sticky="nsew")  # Use nsew to make it fill and expand
        self.hint_text.insert(tk.END, "Click 'Generate Chart & Get Hint' to see the analysis.")
        self.hint_text.config(state=tk.DISABLED)  # Make it read-only initially

    def process_chart_and_hint(self):
        """
        Gathers user input, updates GUI status, and initiates the chart generation
        and OpenAI analysis in a non-blocking way.
        """
        symbol = self.symbol_var.get()
        timeframe = self.timeframe_var.get()
        try:
            limit = int(self.limit_var.get())
            if limit <= 0:
                raise ValueError("Limit must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid positive integer for Limit. {e}")
            return

        # Disable button and update status while processing to prevent re-clicks
        self.generate_button.config(state=tk.DISABLED)
        self.hint_text.config(state=tk.NORMAL)  # Enable for editing
        self.hint_text.delete(1.0, tk.END)
        self.hint_text.insert(tk.END, "Generating chart and fetching hint... Please wait.\n")
        self.hint_text.config(state=tk.DISABLED)  # Disable again
        self.update_idletasks()  # Force GUI to update immediately

        # Schedule the actual analysis task to run after a short delay.
        # This allows the GUI to update its status message before blocking operations start.
        self.after(100, self._perform_analysis_task, symbol, timeframe, limit)

    def _perform_analysis_task(self, symbol, timeframe, limit):
        """
        Contains the core logic for generating the chart, encoding it,
        calling the OpenAI API, and displaying the results.
        """
        image_path = "test.png"  # This is where your cs() function saves the image

        try:
            # 1. Call your existing cs function to generate the candlestick chart
            self.update_status("Generating chart...")
            # 'kucoin' is hardcoded as in your original script.
            # If you want this user-selectable, add an OptionMenu for it.
            df_string = cs(symbol=symbol, timeframe=timeframe, exchange='kucoin', limit=limit)
            print(df_string)

            # 2. Display the generated chart in the GUI
            if os.path.exists(image_path):
                img = Image.open(image_path)

                # Define the exact dimensions you want
                desired_width = 500
                desired_height = 300

                # Use Image.resize() to force the exact dimensions
                # Be aware this will distort the image if its original aspect ratio is not 7:5
                img = img.resize((desired_width, desired_height), Image.LANCZOS)  # Use LANCZOS for good quality

                img_tk = ImageTk.PhotoImage(img)
                self.chart_label.config(image=img_tk)
                self.chart_label.image = img_tk  # IMPORTANT: Keep a reference to prevent garbage collection
                self.update_status("Chart displayed.")
            else:
                messagebox.showerror("Error", f"Failed to generate chart. Image file '{image_path}' not found.")
                self.update_status("Chart generation failed.")
                return

            # 3. Get the Base64 string of the image
            self.update_status("Encoding image for API...")
            base64_image = encode_image(image_path)
            if base64_image is None:
                self.update_status("Image encoding failed.")
                return

            # 4. Call OpenAI API with the encoded image
            self.update_status("Calling AvalAI API for hint...")
            # Access the text from a tk.Text widget
            # "1.0" means from the first character of the first line
            # "end-1c" means to the end of the text, excluding the final newline character
            user_prompt = self.custom_prompt_text_widget.get("1.0", "end-1c")

            prompt_text = f"""
                        Based on the candlestick chart, considering potential trends, support/resistance levels, and common fractal patterns provide a trading signal.
                        Only list the position type (Long, Short, None), stoploss, takeprofit as below:
                        Position Side:
                        Current Price:
                        StopLoss:
                        StopLoss (Percentage):
                        TakeProfit:
                        TakeProfit (Percentage):
                        Do not add anything more than this structure; only add up to 100 words description about why the signal was generated (After 2 empty lines)!
                        Use accurate values not rounded
                        Also, firstly consider {user_prompt} with higher priority (if is not meaningless).
                        """
            response = client.chat.completions.create(
                model="gpt-4o",  # Or another vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        ],
                    }
                ],
            )

            # 5. Display the trading hint
            hint = response.choices[0].message.content
            self.hint_text.config(state=tk.NORMAL)  # Enable to write
            self.hint_text.delete(1.0, tk.END)  # Clear previous content
            self.hint_text.insert(tk.END, hint)
            self.hint_text.config(state=tk.DISABLED)  # Disable again for read-only
            self.update_status("Analysis complete.")

        except Exception as e:
            error_message = f"An unexpected error occurred during analysis: {e}"
            messagebox.showerror("Error", error_message)
            self.hint_text.config(state=tk.NORMAL)
            self.hint_text.delete(1.0, tk.END)  # Clear previous messages
            self.hint_text.insert(tk.END, f"Error: {e}")
            self.hint_text.config(state=tk.DISABLED)
            self.update_status("Analysis failed.")
        finally:
            self.generate_button.config(state=tk.NORMAL)  # Re-enable the button

    def update_status(self, message):
        """Helper to update the status in the hint text area."""
        self.hint_text.config(state=tk.NORMAL)
        # Check if the text widget contains only initial or status messages
        current_text = self.hint_text.get(1.0, tk.END).strip()
        if not current_text or "Click 'Generate Chart & Get Hint'" in current_text or current_text.startswith(
                "Generating chart") or current_text.startswith("Encoding image") or current_text.startswith(
            "Calling AvalAI"):
            self.hint_text.delete(1.0, tk.END)  # Clear if it's a status line

        self.hint_text.insert(tk.END, message + "\n")
        self.hint_text.see(tk.END)  # Scroll to the end
        self.hint_text.config(state=tk.DISABLED)
        self.update_idletasks()  # Force a GUI refresh


# --- Run the application ---
if __name__ == "__main__":
    app = CryptoChartAnalyzer()
    app.mainloop()