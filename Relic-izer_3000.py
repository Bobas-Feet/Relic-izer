import tkinter as tk
from tkinter import ttk, messagebox


Salvage = ["Carbonite circuit board", "Bronzium wiring", "Chromium transistor", "Aurodium heatsink",
           "Electrium conductor", "Zinbiddle card", "Impulse detector", "Aeromagnifier",
           "Gyrda keypad", "Droid brain"]

Signal_Data = ["Fragmented [light blue]", "Incomplete [green]", "Flawed [dark blue]"]

character_names = [
    "Ahsoka Tano", "Darth Vader", "Luke Skywalker", "Rey", "Kylo Ren",
    "Yoda", "Palpatine", "Han Solo", "Chewbacca", "Leia Organa",
    # Add the rest of your character names here...
]


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


class SearchableCombobox(tk.Frame):
    def __init__(self, master, values, max_height=6, **kwargs):
        super().__init__(master)
        self.values = values
        self.filtered_values = list(values)
        self.var = tk.StringVar()

        # Entry widget
        self.entry = ttk.Entry(self, textvariable=self.var, width=kwargs.get("width", 30))
        self.entry.pack(fill=tk.BOTH, expand=True)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.entry.bind("<Button-1>", self.show_dropdown)

        # Dropdown frame
        self.dropdown_frame = tk.Toplevel(self)
        self.dropdown_frame.withdraw()
        self.dropdown_frame.overrideredirect(True)
        self.dropdown_frame.attributes("-topmost", True)

        # Scrollable listbox
        self.listbox = tk.Listbox(self.dropdown_frame, activestyle="dotbox")
        self.scrollbar = tk.Scrollbar(self.dropdown_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind listbox behavior
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Motion>", self.on_hover)
        self.listbox.bind("<Leave>", lambda e: self.listbox.selection_clear(0, tk.END))

        self.max_height = max_height
        self.listbox_visible = False
        self.current_selection = None

        # Focus management: entry and listbox
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.listbox.bind("<FocusOut>", self.on_focus_out)

        # Global click-outside check
        self.master.bind_all("<Button-1>", self.check_click_outside)

        # Flag for tracking scrollbar interactions
        self.scrollbar_interaction = False
        self.scrollbar.bind("<ButtonPress-1>", self.on_scrollbar_interaction)
        self.scrollbar.bind("<ButtonRelease-1>", self.on_scrollbar_interaction)

        # Window move handling for dropdown
        self.root = self.winfo_toplevel()
        self.root.bind("<Configure>", self.on_window_move)

    def on_scrollbar_interaction(self, event):
        """Flag when the user interacts with the scrollbar."""
        self.scrollbar_interaction = True
        # Reset the interaction flag shortly after the interaction
        self.after(100, self.reset_scrollbar_interaction)

    def reset_scrollbar_interaction(self):
        """Reset the scrollbar interaction flag after the interaction is done."""
        self.scrollbar_interaction = False

    def on_keyrelease(self, event=None):
        """Handle key release for filtering values."""
        query = self.var.get().lower()
        self.filtered_values = [v for v in self.values if query in v.lower()] if query else list(self.values)
        self.update_dropdown()

    def show_dropdown(self, event=None):
        """Show the dropdown if it is not visible and the input is not the same as the current selection."""
        if not self.listbox_visible and self.var.get() != self.current_selection:
            self.update_dropdown()
        self.position_dropdown()

    def position_dropdown(self):
        """Position the dropdown relative to the entry widget."""
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        width = self.entry.winfo_width()
        self.dropdown_frame.geometry(f"{width}x{self.listbox.winfo_reqheight()}+{x}+{y}")
        self.dropdown_frame.deiconify()
        self.listbox_visible = True

    def update_dropdown(self):
        """Update the listbox with the filtered values and position the dropdown."""
        self.listbox.delete(0, tk.END)
        for item in self.filtered_values:
            self.listbox.insert(tk.END, item)

        height = min(len(self.filtered_values), self.max_height)
        self.listbox.config(height=height)
        if self.filtered_values:
            self.position_dropdown()
        else:
            self.hide_dropdown()

    def hide_dropdown(self):
        """Hide the dropdown."""
        self.dropdown_frame.withdraw()
        self.listbox_visible = False

    def on_hover(self, event):
        """Highlight the item under the mouse pointer."""
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)

    def on_select(self, event=None):
        """Handle selection from the listbox."""
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            self.var.set(value)
            self.current_selection = value
            self.hide_dropdown()  # Close dropdown after selection

    def on_focus_out(self, event=None):
        """Handle focus out events to close the dropdown if necessary."""
        if self.scrollbar_interaction:  # Only close if not interacting with the scrollbar
            self.after(100, self._check_focus_loss)

    def _check_focus_loss(self):
        """Check if focus is lost and close the dropdown if necessary."""
        if not (self.entry.focus_get() == self.entry or self.listbox.focus_get() == self.listbox):
            self.hide_dropdown()

    def check_click_outside(self, event):
        """Close dropdown if clicked outside the entry or dropdown."""
        if self.scrollbar_interaction:  # Prevent closing if interacting with scrollbar
            return

        widget = event.widget
        if widget not in (self.entry, self.listbox) and not self._is_child_of(widget, self.dropdown_frame):
            self.hide_dropdown()

    def _is_child_of(self, widget, parent):
        """Helper function to check widget hierarchy."""
        while widget:
            if widget == parent:
                return True
            widget = widget.master
        return False

    def on_window_move(self, event):
        """Reposition the dropdown when the window is moved."""
        if self.listbox_visible:
            self.after(10, self.position_dropdown)

    def get(self):
        """Get the current value of the combobox."""
        return self.var.get()

    def delete(self, start, end):
        """Delete text from the entry."""
        self.entry.delete(start, end)

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
        print_output("Something's missing. Either it's Current Relic, Target Relic, or both")
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
            current_frame.config(highlightbackground="red", highlightcolor="red")
            target_frame.config(highlightbackground="red", highlightcolor="red")
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
        print_output("Something's missing. Either it's Current Relic, Target Relic, or both.")
        return

    if not calculation_history:
        print_output("Before calculation, you'll need to add to the queue at least one line, genius.")
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

    print_output("\n".join(output_lines))
    text_output.yview_moveto(0.0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Relic-izer 3000")
# root.geometry("300x200")

    calculation_history = []

    current_frame = tk.Frame(root, highlightthickness=2)
    target_frame = tk.Frame(root, highlightthickness=2)
    name_frame = tk.Frame(root, highlightthickness=2)

    tk.Label(root, text="Current Relic Level (0–8):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    current_entry = tk.Spinbox(current_frame, from_=0, to=8, width=5)
    current_entry.pack()
    current_entry.delete(0, tk.END)  # Make blank on startup
    current_frame.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Target Relic Level (1–9):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    target_entry = tk.Spinbox(target_frame, from_=1, to=9, width=5)
    target_entry.pack()
    target_entry.delete(0, tk.END)  # Make blank on startup
    target_frame.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Character Name (optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    name_entry = SearchableCombobox(name_frame, values=character_names, width=30)
    name_entry.pack()
    name_frame.grid(row=2, column=1, padx=5, pady=5)

    text_output = tk.Text(root, width=80, height=20, wrap="word")
    text_output.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


# Buttons
    tk.Button(root, text="Add to Queue", command=add_calculation).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(root, text="Calculate", command=summarize_all).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(root, text="Wipe them out", command=clear_all).grid(row=2, column=2, padx=5, pady=5)

    root.mainloop()
