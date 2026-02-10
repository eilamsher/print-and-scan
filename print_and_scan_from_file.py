import csv
from pathlib import Path
import time
import tkinter as tk
from tkinter import filedialog

from utils import load_json
from wiliot_tools.test_equipment.test_equipment import CognexDataMan, ZebraPrinter


DEFAULT_PRINTER_CONFIG = {"printer_name": "Zebra_Technologies_ZTC_ZT421-203dpi_ZPL","dpi": 203, "label_format_path": "",
                          "label_width_in": 4, "label_height_in": 6, "label_gap_in": 0.2}
PRINTER_CONFIG_PATH = Path(__file__).parent / "printer_config.json"

def verify_scanned_data(scanned_data) -> bool:
    if len(scanned_data) != 2:
        return False
    return True

def show_scan_failure_popup() -> str:
    """Show a popup when scan fails. Returns 'rescan' or 'reprint'."""
    result = []
    root = tk.Tk()
    root.title("Scan Failed")
    root.geometry("300x120")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    tk.Label(root, text="Scan unsuccessful", font=("Arial", 14)).pack(pady=(15, 10))
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Rescan", width=10,
              command=lambda: (result.append("rescan"), root.destroy())).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Reprint", width=10,
              command=lambda: (result.append("reprint"), root.destroy())).pack(side=tk.LEFT, padx=10)
    root.protocol("WM_DELETE_WINDOW", lambda: (result.append("rescan"), root.destroy()))
    root.mainloop()
    return result[0]

def main():
    csv_path = filedialog.askopenfilename(title="Please select a CSV print file")
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        label_content = list(reader)

    scanner = CognexDataMan()
    scanner.reset()
    printer_params = load_json(PRINTER_CONFIG_PATH, DEFAULT_PRINTER_CONFIG)
    printer_params["label_content_path"] = csv_path
    printer = ZebraPrinter(**printer_params)
    ind = 0
    while ind < len(label_content):
        printer.print_label_by_ind(ind)
        time.sleep(2) # wait for the label to be printed before scanning
        scanned_data = scanner.read_batch_with_trigger(n_msg=2)
        num_retries = 0
        while not verify_scanned_data(scanned_data):
            if num_retries > 3:
                break
            scanned_data = scanner.read_batch_with_trigger(n_msg=2)
            num_retries += 1
        if num_retries <= 3:
            ind += 1

if __name__ == "__main__":
    main()
