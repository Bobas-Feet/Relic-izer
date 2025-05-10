import tkinter as tk
from tkinter import messagebox
from lists_database import *


def calculate_mats(relic):

    if relic < 0 or relic > 8:
        return None, None

    return salvage_reqs[relic], signalData_reqs[relic]


def calculate_mats_sum(current_relic, target_relic):

    total_salvage_dif = [0] * len(Salvage)
    total_signalData_dif = [0] * len(Signal_Data)
    for relic_level in range(current_relic, target_relic):
        salvage_needed, signalData_needed = calculate_mats(relic_level)
        total_salvage_dif = [x + y for x, y in zip(total_salvage_dif, salvage_needed)]
        total_signalData_dif = [x + y for x, y in zip(total_signalData_dif, signalData_needed)]

    return total_salvage_dif, total_signalData_dif


def print_output(text, replace_top=False, text_output=None):

    if replace_top:
        # Replace only the top line (like updating a status bar)
        text_output.delete("1.0", "2.0")
        text_output.insert("1.0", text + "\n")
    else:
        # Standard append-to-bottom behavior
        text_output.insert(tk.END, text + "\n")
        text_output.see(tk.END)  # scroll to bottom if needed


def reset_field_styles(current_frame=None, target_frame=None):

    default_color = "SystemButtonFace"
    if current_frame:
        current_frame.config(highlightbackground=default_color, highlightcolor=default_color)
    if target_frame:
        target_frame.config(highlightbackground=default_color, highlightcolor=default_color)


def clear_all(current_entry=None, target_entry=None, name_entry=None, text_output=None,
              calculation_history=None, current_frame=None, target_frame=None):

    confirm = messagebox.askyesno("Confirm", "All of them?")
    if confirm:
        current_entry.delete(0, tk.END)
        target_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        text_output.delete(1.0, tk.END)
        calculation_history.clear()
        reset_field_styles(current_frame, target_frame)


def validate_inputs(current_entry=None, target_entry=None, current_frame=None, target_frame=None):

    default_color = "SystemButtonFace"
    valid = True
    try:
        current = int(current_entry.get())
    except ValueError:
        current = None
    try:
        target = int(target_entry.get())
    except ValueError:
        target = None

    # Reset to default border
    current_frame.config(highlightbackground=default_color)
    target_frame.config(highlightbackground=default_color)

    if current is None or not (0 <= current <= 8):
        current_frame.config(highlightbackground="red")
        valid = False

    if target is None or not (1 <= target <= 9):
        target_frame.config(highlightbackground="red")
        valid = False

    if current is not None and target is not None and current >= target:
        current_frame.config(highlightbackground="red")
        target_frame.config(highlightbackground="red")
        valid = False

    return valid


def highlight_entry(entry_widget, valid):

    if valid:
        entry_widget.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
    else:
        entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)


def highlight_frame(frame, state):
    if frame is None:
        return
    default_color = "SystemButtonFace"
    if state == "focus":
        frame.config(highlightbackground="blue", highlightcolor="blue", highlightthickness=2)
    elif state == "valid":
        frame.config(highlightbackground="green", highlightcolor="green", highlightthickness=2)
    else:  # default
        frame.config(highlightbackground=default_color, highlightcolor=default_color, highlightthickness=1)


def add_calculation(text_output=None, current_entry=None, target_entry=None, current_frame=None, target_frame=None,
                    calculation_history=None, name_entry=None):

    text_output.delete(1.0, tk.END)

    if not validate_inputs(current_entry, target_entry, current_frame, target_frame):
        print_output("Something's missing. Either it's Current Relic, Target Relic, or both", text_output=text_output)
        return

    try:
        current = int(current_entry.get())
        target = int(target_entry.get())

        if not (0 <= current <= 8):
            current_frame.config(highlightbackground="red", highlightcolor="red")
            print_output("Current level must be between 0 and 8.", text_output=text_output)
            return
        if not (1 <= target <= 9):
            target_frame.config(highlightbackground="red", highlightcolor="red")
            print_output("Target level must be between 1 and 9.", text_output=text_output)
            return
        if current >= target:
            current_frame.config(highlightbackground="red", highlightcolor="red")
            target_frame.config(highlightbackground="red", highlightcolor="red")
            print_output("This is a Relic **UPGRADING** tool. You can't go down.", text_output=text_output)
            return

        name = name_entry.get().strip()
        calculation_history.append((name, current, target))
        name_entry.delete(0, tk.END)

        if name:
            print_output(f"Added (Relic {current} → {target}) for {name}"
                         f" to the queue,\nClick 'Calculate' to see totals.", text_output=text_output)
        else:
            print_output(f"Relic {current} → {target} ready, Click 'Calculate' to see totals.", text_output=text_output, replace_top=True)

    except ValueError:
        highlight_entry(current_entry, False)
        highlight_entry(target_entry, False)
        print_output("Relic levels are numerical, not alphabetical, or "
                     "whatever that was.", text_output=text_output, replace_top=True)


def summarize_all(calculation_history=None, text_output=None,
                  current_entry=None, target_entry=None,
                  current_frame=None, target_frame=None):
    text_output.delete(1.0, tk.END)

    if not validate_inputs(current_entry=current_entry, target_entry=target_entry,
                       current_frame=current_frame, target_frame=target_frame):
        print_output("Something's missing. Either it's Current Relic, Target Relic, or both.", text_output=text_output)
        return

    if not calculation_history:
        print_output("Before calculation, you'll need to add to the queue at least one line, genius.", text_output=text_output)
        return

    total_salvage = [0] * len(Salvage)
    total_signal = [0] * len(Signal_Data)
    output_lines = ["                          === INDIVIDUAL SUMMARY ===\n"]

    for i, (name, current, target) in enumerate(calculation_history, 1):
        label = f"{name}" if name else f"Upgrade #{i}"
        output_lines.append(f"=== {label} ===")
        salvage_diff, signal_diff = calculate_mats_sum(current, target)
        output_lines.append(f" - Relic {current} → Relic {target} - ")

        # Only show "Salvage" section if there's data
        if any(amount > 0 for amount in salvage_diff):
            output_lines.append("Salvage")
            for s_name, amount in zip(Salvage, salvage_diff):
                if amount > 0:
                    output_lines.append(f"   - {s_name}: {amount}")

        # Only show "Signal Data" section if there's data
        if any(amount > 0 for amount in signal_diff):
            output_lines.append("Signal Data")
            for sig_name, amount in zip(Signal_Data, signal_diff):
                if amount > 0:
                    output_lines.append(f"   - {sig_name}: {amount}")

        output_lines.append("")

        total_salvage = [x + y for x, y in zip(total_salvage, salvage_diff)]
        total_signal = [x + y for x, y in zip(total_signal, signal_diff)]

    # Only append GRAND TOTAL if there is more than one line in the queue
    if len(calculation_history) > 1:
        output_lines.append("                               === GRAND TOTAL ===\n")

        # Only show total salvage if there is any salvage data
        if any(amount > 0 for amount in total_salvage):
            output_lines.append("Salvage")
            for s_name, amount in zip(Salvage, total_salvage):
                if amount > 0:
                    output_lines.append(f"   - {s_name}s: {amount} pieces")

        # Only show total signal data if there is any signal data
        if any(amount > 0 for amount in total_signal):
            output_lines.append("Signal Data")
            for sig_name, amount in zip(Signal_Data, total_signal):
                if amount > 0:
                    output_lines.append(f"   - {sig_name}: {amount}")
        output_lines.append("")

    print_output("\n".join(output_lines), text_output=text_output)
    text_output.yview_moveto(0.0)


def on_entry_focus_out(current_entry=None, target_entry=None,
                       current_frame=None, target_frame=None):
    try:
        current = int(current_entry.get())
        target = int(target_entry.get())
        if 0 <= current <= 8 and 1 <= target <= 9 and current < target:
            highlight_frame(current_frame, "valid")
            highlight_frame(target_frame, "valid")
            return
    except ValueError:
        pass  # Validation failed, just reset to default

    highlight_frame(current_frame, "default")
    highlight_frame(target_frame, "default")


def reset_focus_on_global_click(event, current_entry, target_entry, current_frame, target_frame):

    # Check if the focus is still on current_entry or target_entry
    focused_widget = event.widget.focus_get()

    # Reset frames if focus is lost and not on the entry fields
    if focused_widget not in (current_entry, target_entry):
        highlight_frame(current_frame, "default")
        highlight_frame(target_frame, "default")


def on_global_click(event, current_entry=None, target_entry=None, current_frame=None,
                    target_frame=None, name_entry=None, name_frame=None):
    widget = event.widget

    if not all([current_entry, target_entry, name_entry,
                current_frame, target_frame, name_frame]):
        return

    entries = [current_entry, target_entry, name_entry]

    if widget not in entries:
        # Not an entry field, so remove focus and reset styles unless valid
        try:
            current = int(current_entry.get())
            target = int(target_entry.get())
            if 0 <= current <= 8 and 1 <= target <= 9 and current < target:
                highlight_frame(current_frame, "valid")
                highlight_frame(target_frame, "valid")
            else:
                highlight_frame(current_frame, "default")
                highlight_frame(target_frame, "default")
        except ValueError:
            highlight_frame(current_frame, "default")
            highlight_frame(target_frame, "default")

        highlight_frame(name_frame, "default")
        # root.focus_set()  # Remove focus from entry widgets


def on_entry_focus_out_delayed(current_entry=None, target_entry=None,
                               current_frame=None, target_frame=None):
    def delayed_check():
        # Check if the focus is still on the current or target entry fields
        focused_widget = current_entry.winfo_toplevel().focus_get()

        # If the focus is not on either of the relevant fields, reset their highlights
        if focused_widget not in (current_entry, target_entry):
            try:
                current = int(current_entry.get())
                target = int(target_entry.get())

                if 0 <= current <= 8 and 1 <= target <= 9 and current < target:
                    highlight_frame(current_frame, "valid")
                    highlight_frame(target_frame, "valid")
                else:
                    highlight_frame(current_frame, "default")
                    highlight_frame(target_frame, "default")
            except ValueError:
                # Reset frames if invalid input
                highlight_frame(current_frame, "default")
                highlight_frame(target_frame, "default")

    current_entry.after(2, delayed_check)


