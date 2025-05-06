import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


Salvage = [
    "Carbonite circuit board", "Bronzium wiring", "Chromium transistor", "Aurodium heatsink",
    "Electrium conductor", "Zinbiddle card", "Impulse detector", "Aeromagnifier",
    "Gyrda keypad", "Droid brain"
]
Signal_Data = ["Fragmented [light blue]", "Incomplete [green]", "Flawed [dark blue]"]

salvage_reqs = [
    [40, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # R0
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # R1
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # R2
    [30, 40, 40, 0, 0, 0, 0, 0, 0, 0],  # R3
    [30, 40, 30, 20, 0, 0, 0, 0, 0, 0],  # R4
    [20, 30, 30, 20, 20, 0, 0, 0, 0, 0],  # R5
    [20, 30, 20, 20, 20, 10, 0, 0, 0, 0],  # R6
    [0, 0, 20, 20, 20, 20, 20, 20, 0, 0],  # R7
    [0, 0, 20, 20, 20, 20, 20, 20, 20, 20],  # R8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # R9
]

signalData_reqs = [
    [0, 0, 0], [15, 0, 0], [20, 15, 0], [20, 25, 0],
    [20, 25, 15], [20, 25, 25], [20, 25, 35], [20, 25, 45],
    [30, 30, 55], [0, 0, 0]
]


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


root = tk.Tk()
root.title("Relic-izer 3000")

calculation_history = []

current_frame = tk.Frame(root, highlightthickness=2)
target_frame = tk.Frame(root, highlightthickness=2)
name_frame = tk.Frame(root)

tk.Label(root, text="Current Relic Level (0–8):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
current_entry = tk.Entry(current_frame, width=10)
current_entry.pack()
current_frame.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Target Relic Level (1–9):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
target_entry = tk.Entry(target_frame, width=10)
target_entry.pack()
target_frame.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Character Name (optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(name_frame, width=20)
name_entry.pack()
name_frame.grid(row=2, column=1, padx=5, pady=5)

text_output = tk.Text(root, width=80, height=20, wrap="word")
text_output.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


def print_output(text, replace_top=False):

    if replace_top:
        # Replace only the top line (like updating a status bar)
        text_output.delete("1.0", "2.0")
        text_output.insert("1.0", text + "\n")
    else:
        # Standard append-to-bottom behavior
        text_output.insert(tk.END, text + "\n")
        text_output.see(tk.END)  # scroll to bottom if needed


def reset_field_styles():
    current_frame.config(highlightbackground="gray", highlightcolor="gray")
    target_frame.config(highlightbackground="gray", highlightcolor="gray")


def clear_all():

    confirm = messagebox.askyesno("Confirm", "All of them?")
    if confirm:
        current_entry.delete(0, tk.END)
        target_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        text_output.delete(1.0, tk.END)
        calculation_history.clear()
        highlight_entry(current_entry, True)
        highlight_entry(target_entry, True)
        reset_field_styles()


def highlight_entry(entry_widget, valid):
    if valid:
        entry_widget.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
    else:
        entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)


def validate_inputs():
    reset_field_styles()
    valid = True

    if not current_entry.get().strip():
        current_frame.config(highlightbackground="red", highlightcolor="red")
        valid = False
    if not target_entry.get().strip():
        target_frame.config(highlightbackground="red", highlightcolor="red")
        valid = False

    return valid


def highlight_frame(frame, is_error):
    frame.config(highlightbackground="red" if is_error else "white", highlightcolor="red" if is_error else "white")


def add_calculation():

    text_output.delete(1.0, tk.END)

    if not validate_inputs():
        print_output("Something's missing.")
        return

    try:
        current = int(current_entry.get())
        target = int(target_entry.get())

        if not (0 <= current <= 8):
            current_frame.config(highlightbackground="red", highlightcolor="red")
            print_output("Current level must be between 0 and 8.")
            return
        if not (1 <= target <= 9):
            target_frame.config(highlightbackground="red", highlightcolor="red")
            print_output("Target level must be between 1 and 9.")
            return
        if current >= target:
            print_output("This is a Relic **UPGRADING** tool. You can't go down.")
            return

        name = name_entry.get().strip()
        calculation_history.append((name, current, target))
        name_entry.delete(0, tk.END)

        if name:
            print_output(f"Added (Relic {current} → {target}) for {name} to the queue,\nClick 'Calculate' to see totals.")
        else:
            print_output(f"Relic {current} → {target} ready, Click 'Calculate' to see totals.", replace_top=True)

    except ValueError:
        highlight_entry(current_entry, False)
        highlight_entry(target_entry, False)
        print_output("Relic levels are numerical, not alphabetical, or whatever that was.", replace_top=True)


def summarize_all():

    text_output.delete(1.0, tk.END)

    if not validate_inputs():
        print_output("Something's Missing.")
        return

    text_output.delete(1.0, tk.END)

    if not calculation_history:
        print_output("Before you calculate, you'll need to enter at least one upgrade, genius.")
        return

    total_salvage = [0] * len(Salvage)
    total_signal = [0] * len(Signal_Data)
    output_lines = ["                          === INDIVIDUAL SUMMARY ===\n"]

    for i, (name, current, target) in enumerate(calculation_history, 1):
        label = f"{name}" if name else f"Upgrade #{i} (Relic {current} → Relic {target})"
        output_lines.append(f"==={label}===")
        salvage_diff, signal_diff = calculate_mats_sum(current, target)

        output_lines.append(f"{i}. Relic {current} → Relic {target}")
        output_lines.append("Salvage")
        for s_name, amount in zip(Salvage, salvage_diff):
            if amount > 0:
                output_lines.append(f"   - {s_name}: {amount}")

        output_lines.append("Signal Data")
        for sig_name, amount in zip(Signal_Data, signal_diff):
            if amount > 0:
                output_lines.append(f"   - {sig_name}: {amount}")
        output_lines.append("")

        total_salvage = [x + y for x, y in zip(total_salvage, salvage_diff)]
        total_signal = [x + y for x, y in zip(total_signal, signal_diff)]

    output_lines.append("                               === GRAND TOTAL ===")
    output_lines.append("Salvage")
    for s_name, amount in zip(Salvage, total_salvage):
        if amount > 0:
            output_lines.append(f"   - {s_name}s: {amount} pieces")
    output_lines.append("Signal Data")
    for sig_name, amount in zip(Signal_Data, total_signal):
        if amount > 0:
            output_lines.append(f"   - {sig_name}: {amount}")
    output_lines.append("")

    print_output("\n".join(output_lines))


# Buttons
tk.Button(root, text="Add to Queue", command=add_calculation).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text="Calculate", command=summarize_all).grid(row=1, column=2, padx=5, pady=5)
tk.Button(root, text="Wipe them out", command=clear_all).grid(row=2, column=2, padx=5, pady=5)

root.mainloop()
