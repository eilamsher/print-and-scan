import csv
import time
from tkinter import filedialog

from wiliot_tools.test_equipment.test_equipment import CognexDataMan, ZebraPrinter


def verify_scanned_data(scanned_data) -> bool:
    if len(scanned_data) != 2:
        return False
    return True

def main():
    label_format_path = ''
    csv_path = filedialog.askopenfilename(title="Please select a CSV print file")
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        label_content = list(reader)

    scanner = CognexDataMan()
    scanner.reset()
    printer_params = {"dpi": 203, "label_format_path": label_format_path, "label_content_path": csv_path, "starting_ind": 0, "label_width_in": 4, "label_height_in": 6, "label_gap_in": 0.2}
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
