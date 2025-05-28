from widgets import SearchableCombobox
from logic import *
import customtkinter as ctk
from lists_database import *

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Relic-izer 3000")
    root.iconbitmap("holocron2.ico")
    # root.geometry("800x600")
    root.resizable(False, False)
    calculation_history = []

    def block_non_numeric(event):
        if not (event.char.isdigit() or event.keysym in ("BackSpace", "Left", "Right", "Tab", "Delete")):
            return "break"
        return None

    def sanitize_spinbox_input(spinbox):
        value = spinbox.get()
        if not value.isdigit():
            spinbox.delete(0, ctk.END)

    def select_all(event):
        event.widget.select_range(0, 'end')
        return "break"

    def target_focus_out_handler(event):
        sanitize_spinbox_input(target_entry)
        on_entry_focus_out(current_entry, target_entry, current_frame, target_frame)

    def highlight_frame(frame, status):
        frame.highlight_status = status
        color = {"default": "grey", "focus": "blue", "valid": "green", "invalid": "red"}.get(status, "grey")
        frame.configure(border_color=color, border_width=2)

    def on_global_click(event):
        widget = event.widget.winfo_containing(event.x_root, event.y_root)

        for entry in (current_entry, target_entry):
            if widget != entry:
                entry.event_generate("<FocusOut>")

        for combobox in (name_entry, status_effect_combobox):
            if hasattr(combobox, "on_global_click"):
                combobox.on_global_click(event)

    def on_root_focus_out(event):
        for combobox in (name_entry, status_effect_combobox):
            if hasattr(combobox, "hide_dropdown"):
                combobox.hide_dropdown()

    def handle_status_effect_selection(effect_name):
        characters = status_effects.get(effect_name, [])
        if characters:
            output_text = f"{effect_name}:\n• " + "\n• ".join(characters)
            current_text = text_output.get("1.0", tk.END).strip()
            if current_text:
                text_output.insert(tk.END, f"\n\n{output_text}")
            else:
                text_output.insert("1.0", output_text)

    def on_status_effect_selected(effect):
        associated_characters = status_effects.get(effect, [])
        text = f"***** {effect} *****\n" + ", \n".join(
            associated_characters) if associated_characters else "No associated characters found."
        text_output.configure(state="normal")
        text_output.delete("1.0", "end")
        text_output.insert("end", text)
        text_output.configure(state="disabled")

    root.bind("<Button-1>", on_global_click)
    root.bind("<FocusOut>", on_root_focus_out)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    content_frame = ctk.CTkFrame(root)
    content_frame.grid(row=0, column=0, sticky="nsew")
    pad_args = {"padx": 10, "pady": 10}

    current_label = ctk.CTkLabel(content_frame, text="Current Relic Level (0–8):")
    current_label.grid(row=0, column=0, sticky="w", **pad_args)

    current_frame = ctk.CTkFrame(content_frame, corner_radius=5)
    current_frame.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    current_frame.highlight_status = "default"

    current_entry = ctk.CTkEntry(current_frame, width=50)
    current_entry.grid(padx=5, pady=5)
    current_entry.bind("<KeyPress>", block_non_numeric)
    current_entry.bind("<FocusIn>", lambda e: (on_entry_focus_in(current_frame), select_all(e)))
    current_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(
        current_entry=current_entry,
        target_entry=target_entry,
        current_frame=current_frame,
        target_frame=target_frame))

    target_label = ctk.CTkLabel(content_frame, text="Target Relic Level (1–9):")
    target_label.grid(row=1, column=0, sticky="w", **pad_args)

    target_frame = ctk.CTkFrame(content_frame, corner_radius=5)
    target_frame.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    target_frame.highlight_status = "default"

    target_entry = ctk.CTkEntry(target_frame, width=50)
    target_entry.grid(padx=5, pady=5)
    target_entry.bind("<KeyPress>", block_non_numeric)
    target_entry.bind("<FocusIn>", lambda e: (on_entry_focus_in(target_frame), select_all(e)))
    target_entry.bind("<FocusOut>", target_focus_out_handler)

    name_label = ctk.CTkLabel(content_frame, text="Character Name (optional):")
    name_label.grid(row=2, column=0, sticky="w", **pad_args)

    name_frame = ctk.CTkFrame(content_frame, corner_radius=5)
    name_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    name_frame.highlight_status = "default"

    name_entry = SearchableCombobox(name_frame, width=200, values=character_names)
    name_entry.grid(padx=5, pady=5)
    name_entry.bind("<FocusIn>", lambda e: highlight_frame(name_frame, "focus"))
    name_entry.bind("<FocusOut>", lambda e: highlight_frame(name_frame, "default"))

    status_effect_entry = ctk.CTkLabel(content_frame, text="Status Effects and Abilities:")
    status_effect_entry.grid(row=3, column=0, sticky="w", **pad_args)

    status_frame = ctk.CTkFrame(content_frame, corner_radius=5)
    status_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
    status_frame.highlight_status = "default"

    status_effect_combobox = SearchableCombobox(
        status_frame,
        values=sorted(status_effects.keys()),
        width=200,
        selection_callback=on_status_effect_selected)
    status_effect_combobox.grid(padx=5, pady=5)

    status_effect_combobox.bind("<FocusIn>", lambda e: highlight_frame(status_frame, "focus"))
    status_effect_combobox.bind("<FocusOut>", lambda e: highlight_frame(status_frame, "default"))

    button_frame = ctk.CTkFrame(content_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=15)

    add_button = ctk.CTkButton(button_frame, text="Add to queue", command=lambda: add_calculation(
        text_output, current_entry, target_entry, current_frame, target_frame, calculation_history, name_entry))
    add_button.grid(row=0, column=0, padx=10)

    calc_button = ctk.CTkButton(button_frame, text="Calculate", command=lambda: summarize_all(
        calculation_history, text_output, current_entry, target_entry, current_frame, target_frame))
    calc_button.grid(row=0, column=1, padx=10)

    clear_button = ctk.CTkButton(button_frame, text="Wipe them out", command=lambda: clear_all(
        current_entry=current_entry,
        target_entry=target_entry,
        name_entry=name_entry,
        status_effect_combobox=status_effect_combobox,
        text_output=text_output,
        calculation_history=calculation_history,
        current_frame=current_frame,
        target_frame=target_frame))
    clear_button.grid(row=0, column=2, padx=10)

    text_output = ctk.CTkTextbox(content_frame, width=600, height=200, wrap="word")
    text_output.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

    print_output(Opening_Message, text_output=text_output)
    current_entry.focus_set()

    root.mainloop()



