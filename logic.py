import tkinter as tk
from tkinter import messagebox
from lists_database import *


frame_highlight_states = {}
DEFAULT_GUIDANCE = ("               Before calculation, adjust your desired Current and\n"
                    "                Target relics, click Add to Queue, then Calculate.")
HIGHLIGHT_THICKNESS = 2


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


def print_output(text, replace_top=False, text_output=None, append_default=False):

    if not text_output:
        return

    # Append default message if requested
    full_text = text
    if append_default:
        full_text += f"\n\n{DEFAULT_GUIDANCE}"

    if replace_top:
        # Replace only the first line (used like a status bar)
        text_output.delete("1.0", "2.0")
        text_output.insert("1.0", full_text + "\n")
    else:
        # Append message to the end
        text_output.insert(tk.END, full_text + "\n\n")
        text_output.see(tk.END)  # Scroll to bottom to show latest message


def highlight_frame(frame, status):


    colors = {
        "default": "SystemButtonFace",
        "focus": "blue",
        "valid": "green",
        "invalid": "red"
    }
    frame.config(
        highlightbackground=colors[status],
        highlightcolor=colors[status],
        highlightthickness=HIGHLIGHT_THICKNESS  # consistent thickness
    )

    if status != "focus":
        frame.highlight_status = status


def validate_inputs(current_entry=None, target_entry=None,
                    current_frame=None, target_frame=None):

    valid = True
    max_relic = 9  # set max relic for future potential change

    try:
        current = int(current_entry.get())
    except (ValueError, AttributeError):
        current = None
    try:
        target = int(target_entry.get())
    except (ValueError, AttributeError):
        target = None

        # Reset highlights
    if current_frame:
        highlight_frame(current_frame, "default")
    if target_frame:
        highlight_frame(target_frame, "default")

    current_valid = current is not None and 0 <= current <= 8
    target_valid = target is not None and 1 <= target <= max_relic

    if not current_valid:
        valid = False
        if current_frame:
            highlight_frame(current_frame, "invalid")
    if not target_valid:
        valid = False
        if target_frame:
            highlight_frame(target_frame, "invalid")

    if current_valid and target_valid:
        if current >= target:
            valid = False
            if current_frame:
                highlight_frame(current_frame, "invalid")
            if target_frame:
                highlight_frame(target_frame, "invalid")

    return valid, current, target


def reset_field_styles(*frames):

    for frame in frames:
        if frame:
            highlight_frame(frame, "default")


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

        print_output(DEFAULT_GUIDANCE, text_output=text_output)


def highlight_entry(entry_widget, valid):

    if valid:
        entry_widget.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
    else:
        entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)


def add_calculation(text_output=None, current_entry=None, target_entry=None, current_frame=None,
                    target_frame=None, calculation_history=None, name_entry=None):
    try:
        text_output.delete(1.0, tk.END)

        is_valid, current, target = validate_inputs(
            current_entry=current_entry,
            target_entry=target_entry,
            current_frame=current_frame,
            target_frame=target_frame
        )

        if not is_valid:
            print_output("Invalid inputs. Check again.", text_output=text_output)
            return

        highlight_frame(current_frame, "default")
        highlight_frame(target_frame, "default")

        name = name_entry.get().strip()
        calculation_history.append((name, current, target))
        name_entry.delete(0, tk.END)

        msg = (f"Added (Relic {current} → {target}) for {name} to the queue,\nClick 'Calculate' to see totals."
               if name else
               f"Relic {current} → {target} ready, Click 'Calculate' to see totals.")
        print_output(msg, text_output=text_output, replace_top=not name)

    except ValueError:
        highlight_frame(current_frame, "invalid")
        highlight_frame(target_frame, "invalid")
        print_output("Relic levels are numerical, not alphabetical, or whatever that was.", text_output=text_output, replace_top=True)


# def summarize_all(calculation_history=None, text_output=None,
#                   current_entry=None, target_entry=None,
#                   current_frame=None, target_frame=None):
#     text_output.delete(1.0, tk.END)
#
#     if not calculation_history:
#         highlight_frame(current_frame, "invalid")
#         highlight_frame(target_frame, "invalid")
#         print_output("Before calculation, adjust your desired Cuerrent and Target relics, click Add to Queue, then Calculate.", text_output=text_output)
#         return
#
#     is_valid, current, target = validate_inputs(
#         current_entry=current_entry,
#         target_entry=target_entry,
#         current_frame=current_frame,
#         target_frame=target_frame
#     )
#
#     if not is_valid:
#         highlight_frame(current_frame, "invalid")
#         highlight_frame(target_frame, "invalid")
#         print_output("Something's missing. Either it's Current Relic, Target Relic, or both.", text_output=text_output)
#         return
#
#     highlight_frame(current_frame, "valid")
#     highlight_frame(target_frame, "valid")
#
#     total_salvage = [0] * len(Salvage)
#     total_signal = [0] * len(Signal_Data)
#     output_lines = ["                          === INDIVIDUAL SUMMARY ===\n"]
#
#     for i, (name, current, target) in enumerate(calculation_history, 1):
#         label = f"{name}" if name else f"Upgrade #{i}"
#         output_lines.append(f"=== {label} ===")
#         salvage_diff, signal_diff = calculate_mats_sum(current, target)
#         output_lines.append(f" - Relic {current} → Relic {target} - ")
#
#         # Only show "Salvage" section if there's data
#         if any(amount > 0 for amount in salvage_diff):
#             output_lines.append("Salvage")
#             for s_name, amount in zip(Salvage, salvage_diff):
#                 if amount > 0:
#                     output_lines.append(f"   - {s_name}: {amount}")
#
#         # Only show "Signal Data" section if there's data
#         if any(amount > 0 for amount in signal_diff):
#             output_lines.append("Signal Data")
#             for sig_name, amount in zip(Signal_Data, signal_diff):
#                 if amount > 0:
#                     output_lines.append(f"   - {sig_name}: {amount}")
#
#         output_lines.append("")
#
#         total_salvage = [x + y for x, y in zip(total_salvage, salvage_diff)]
#         total_signal = [x + y for x, y in zip(total_signal, signal_diff)]
#
#     # Only append GRAND TOTAL if there is more than one line in the queue
#     if len(calculation_history) > 1:
#         output_lines.append("                               === GRAND TOTAL ===\n")
#
#         # Only show total salvage if there is any salvage data
#         if any(amount > 0 for amount in total_salvage):
#             output_lines.append("Salvage")
#             for s_name, amount in zip(Salvage, total_salvage):
#                 if amount > 0:
#                     output_lines.append(f"   - {s_name}s: {amount} pieces")
#
#         # Only show total signal data if there is any signal data
#         if any(amount > 0 for amount in total_signal):
#             output_lines.append("Signal Data")
#             for sig_name, amount in zip(Signal_Data, total_signal):
#                 if amount > 0:
#                     output_lines.append(f"   - {sig_name}: {amount}")
#         output_lines.append("")
#
#     print_output("\n".join(output_lines), text_output=text_output)
#     text_output.yview_moveto(0.0)

def summarize_all(calculation_history=None, text_output=None,
                  current_entry=None, target_entry=None,
                  current_frame=None, target_frame=None):
    text_output.delete(1.0, tk.END)

    if not calculation_history:
        highlight_frame(current_frame, "invalid")
        highlight_frame(target_frame, "invalid")
        print_output(
            "Before calculation, adjust your desired Current and Target relics, "
            "click Add to Queue, then Calculate.", text_output=text_output)
        return

    is_valid, current, target = validate_inputs(
        current_entry=current_entry,
        target_entry=target_entry,
        current_frame=current_frame,
        target_frame=target_frame
    )

    if not is_valid:
        highlight_frame(current_frame, "invalid")
        highlight_frame(target_frame, "invalid")
        print_output("Something's missing. Either it's Current Relic, Target Relic, or both.", text_output=text_output)
        return

    highlight_frame(current_frame, "valid")
    highlight_frame(target_frame, "valid")

    output_lines = ["                          === INDIVIDUAL SUMMARY ===\n"]

    total_salvage = [0] * len(Salvage)
    total_signal = [0] * len(Signal_Data)

    for i, (name, cur, tgt) in enumerate(calculation_history, 1):
        label = name if name else f"Upgrade #{i}"
        output_lines.append(f"=== {label} ===")
        output_lines.append(f" - Relic {cur} → Relic {tgt} - ")

        salvage_diff, signal_diff = calculate_mats_sum(cur, tgt)

        if any(amount > 0 for amount in salvage_diff):
            output_lines.append("Salvage")
            for s_name, amount in zip(Salvage, salvage_diff):
                if amount > 0:
                    output_lines.append(f"   - {s_name}: {amount}")

        if any(amount > 0 for amount in signal_diff):
            output_lines.append("Signal Data")
            for sig_name, amount in zip(Signal_Data, signal_diff):
                if amount > 0:
                    output_lines.append(f"   - {sig_name}: {amount}")

        output_lines.append("")
        total_salvage = [x + y for x, y in zip(total_salvage, salvage_diff)]
        total_signal = [x + y for x, y in zip(total_signal, signal_diff)]

    if len(calculation_history) > 1:
        output_lines.append("                               === GRAND TOTAL ===\n")

        if any(amount > 0 for amount in total_salvage):
            output_lines.append("Salvage")
            for s_name, amount in zip(Salvage, total_salvage):
                if amount > 0:
                    output_lines.append(f"   - {s_name}s: {amount} pieces")

        if any(amount > 0 for amount in total_signal):
            output_lines.append("Signal Data")
            for sig_name, amount in zip(Signal_Data, total_signal):
                if amount > 0:
                    output_lines.append(f"   - {sig_name}: {amount}")

        output_lines.append("")

    print_output("\n".join(output_lines), text_output=text_output)
    text_output.yview_moveto(0.0)




def on_entry_focus_in(frame):
    highlight_frame(frame, "focus")


def on_entry_focus_out(current_entry, target_entry, current_frame, target_frame):
    if current_frame.highlight_status != "focus":
        highlight_frame(current_frame, current_frame.highlight_status)
    if target_frame.highlight_status != "focus":
        highlight_frame(target_frame, target_frame.highlight_status)


def is_widget_in_dropdown(widget, dropdown):
    if not dropdown:
        return False
    if widget == dropdown:
        return True
    parent = widget
    while parent:
        if parent == dropdown:
            return True
        parent = parent.master
    return False


def on_global_click(event, current_entry, target_entry, name_entry,
                    current_frame, target_frame, name_frame):
    widget = event.widget

    # Check if click is inside dropdown
    def is_dropdown_widget(w):

        while w:
            if isinstance(w, tk.Toplevel) and "searchable_combobox_dropdown" in str(w):
                return True
            w = w.master
        return False

    if widget in (current_entry, target_entry, name_entry) or is_dropdown_widget(widget):
        return

    # Trigger focus-out logic and remove cursor from active entry
    for entry, frame in[
             (current_entry, current_frame),
             (target_entry, target_frame),
             (name_entry, name_frame)
    ]:
        if entry == entry.focus_get():
            entry.selection_clear()
            entry.winfo_toplevel().focus_set()
            highlight_frame(frame, frame.highlight_status)


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
