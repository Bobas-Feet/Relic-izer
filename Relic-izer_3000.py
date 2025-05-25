from widgets import SearchableCombobox
from logic import *


if __name__ == "__main__":

    try:
        def block_non_numeric(event):
            if not (event.char.isdigit() or event.keysym in ("BackSpace", "Left", "Right", "Tab", "Delete")):
                return "break"
            return None


        def sanitize_spinbox_input(spinbox):
            value = spinbox.get()
            if not value.isdigit():
                spinbox.delete(0, tk.END)


        def target_focus_out_handler(event):
            sanitize_spinbox_input(target_entry)
            on_entry_focus_out(
                current_entry=current_entry,
                target_entry=target_entry,
                current_frame=current_frame,
                target_frame=target_frame
            )


        def on_status_effect_selected(event=None):
            selected_effect = status_effect_combobox.get()
            characters = status_effects.get(selected_effect, [])
            output_text = f"Characters with '{selected_effect}':\n\n"
            output_text += "\n".join(f"• {name}" for name in characters) if characters else "None found."

            text_output.config(state="normal")
            text_output.delete("1.0", "end")
            text_output.insert("1.0", output_text)
            text_output.config(state="disabled")

        root = tk.Tk()
        root.title("Relic-izer 3000")
        root.iconbitmap("holocron2.ico")
        root.resizable(False, False)

        calculation_history = []

        # Initialize the text_output widget before it's used anywhere
        text_output = tk.Text(root, width=80, height=20, wrap="word")
        text_output.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Current spinbox
        tk.Label(root, text="Current Relic Level (0–8):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        current_frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray", highlightcolor="gray", bd=1,
                              relief="solid")
        current_frame.highlight_status = "default"
        current_entry = tk.Spinbox(current_frame, from_=0, to=8, width=5)
        current_entry.pack()
        current_entry.delete(0, tk.END)  # Make blank on startup
        current_entry.bind("<KeyPress>", block_non_numeric)
        current_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(current_frame))
        current_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(
            current_entry=current_entry,
            target_entry=target_entry,
            current_frame=current_frame,
            target_frame=target_frame
        ))
        current_frame.grid(row=0, column=1, padx=5, pady=5)

        # Target spinbox
        tk.Label(root, text="Target Relic Level (1–9):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        target_frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray", highlightcolor="gray", bd=1,
                              relief="solid")
        target_frame.highlight_status = "default"
        target_entry = tk.Spinbox(target_frame, from_=1, to=9, width=5)
        target_entry.pack()
        target_entry.delete(0, tk.END)  # Make blank on startup
        target_entry.bind("<KeyPress>", block_non_numeric)
        target_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(target_frame))
        target_entry.bind("<FocusOut>", target_focus_out_handler)

        target_frame.grid(row=1, column=1, padx=5, pady=5)

        # Character name box
        tk.Label(root, text="Character Name (optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        name_frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray", highlightcolor="gray", bd=1,
                              relief="solid")
        name_frame.highlight_status = "default"
        name_entry = SearchableCombobox(name_frame, values=character_names, width=30)
        name_entry.pack()
        name_entry.bind("<FocusIn>", lambda e: highlight_frame(name_frame, "focus"))
        name_entry.bind("<FocusOut>", lambda e: highlight_frame(name_frame, "default"))
        name_frame.grid(row=2, column=1, padx=5, pady=5)

        # Status Effect dropdown
        tk.Label(root, text="Status Effect Lookup:").grid(row=3, column=0, padx=5, pady=(5, 0), sticky="w")
        status_effect_combobox = SearchableCombobox(root, values=sorted(status_effects.keys()), width=30)
        status_effect_combobox.grid(row=3, column=1, padx=5, pady=(5, 0), sticky="w")
        status_effect_combobox.bind("<<ComboboxSelected>>", on_status_effect_selected)
        status_effect_combobox.bind("<Return>", on_status_effect_selected)

        # Text output display
        text_output = tk.Text(root, width=80, height=20, wrap="word", state="normal")


        # Add to Queue Button
        tk.Button(root, text="Add to Queue", command=lambda: add_calculation(
            text_output=text_output,
            current_entry=current_entry,
            target_entry=target_entry,
            current_frame=current_frame,
            target_frame=target_frame,
            calculation_history=calculation_history,
            name_entry=name_entry
        )).grid(row=0, column=2, padx=5, pady=5)

        # Calculate Button
        tk.Button(root, text="Calculate", command=lambda: summarize_all(
            calculation_history=calculation_history,
            text_output=text_output,
            current_entry=current_entry,
            target_entry=target_entry,
            current_frame=current_frame,
            target_frame=target_frame
        )).grid(row=1, column=2, padx=5, pady=5)

        # Wipe them out
        tk.Button(root, text="Wipe them out", command=lambda: clear_all(
            current_entry=current_entry,
            target_entry=target_entry,
            name_entry=name_entry,
            text_output=text_output,
            calculation_history=calculation_history,
            current_frame=current_frame,
            target_frame=target_frame,
            status_effect_combobox = status_effect_combobox
        )).grid(row=2, column=2, padx=5, pady=5)

        root.bind_all(
             "<Button-1>",
             lambda event: on_global_click(
                 event,
                 current_entry=current_entry,
                 target_entry=target_entry,
                 name_entry=name_entry,
                 current_frame=current_frame,
                 target_frame=target_frame,
                 name_frame=name_frame
         ),
         add='+'
         )

        print_output(DEFAULT_GUIDANCE, text_output=text_output)
        root.mainloop()

    except KeyboardInterrupt:
        print('\nMay the Force be with you')


