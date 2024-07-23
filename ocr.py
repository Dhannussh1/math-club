import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
import json
import requests

def upload_image():
    url = "https://ocr2.asprise.com/api/v1/receipt"
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if not file_path:
        return  

    try:
        with open(file_path, 'rb') as image_file:
            res = requests.post(url, data={'api_key': 'TEST', 'recognizer': 'auto', 'ref_no': 'oct_python_123'},
                                files={'file': image_file})

        res.raise_for_status()  # Raise an error for bad status codes

        result = res.json()
        with open('finalr.json', 'w') as f:
            json.dump(result, f, indent=4)

        process_and_display_result(result, 'finalr.json')

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to upload image: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to decode the response as JSON.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def process_and_display_result(data, json_file):
    try:
        receipts = data['receipts']
        if not receipts:
            messagebox.showinfo("No Data", "No receipts found in the response.")
            return

        receipt = receipts[0]
        items = receipt['items']

        result_text = f"Your purchase at {receipt['merchant_name']}\n"
        result_text += "-" * 30 + "\n"
        for item in items:
            result_text += f"{item['description']} {receipt['currency']} {item['amount']}\n"
        result_text += "-" * 30 + "\n"
        result_text += f"Subtotal: {receipt['currency']} {receipt['subtotal']}\n"
        result_text += f"Tax: {receipt['currency']} {receipt['tax']}\n"
        result_text += "-" * 30 + "\n"
        result_text += f"Total: {receipt['currency']} {receipt['total']}\n\n"

        # Append the entire JSON content
        with open(json_file, 'r') as f:
            json_data = json.load(f)
            json_text = json.dumps(json_data, indent=4)
            result_text += "Full JSON Response:\n"
            result_text += json_text

        display_result(result_text)

    except KeyError as e:
        messagebox.showerror("Error", f"Key error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def display_result(text):
    result_box.config(state=tk.NORMAL)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, text)
    result_box.config(state=tk.DISABLED)

root = tk.Tk()
root.title("OCR Application")
root.geometry("800x600")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=20)

result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=100, height=30)
result_box.pack(pady=20)

root.mainloop()
