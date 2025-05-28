import customtkinter as ctk
from tkinter import Toplevel, Listbox, Scrollbar, StringVar, END, SINGLE
import tkinter as tk
from logic import *


class SearchableCombobox(ctk.CTkEntry):
    def __init__(self, master=None, values=None, width=200, selection_callback=None, **kwargs):
        self.var = ctk.StringVar()
        super().__init__(master, textvariable=self.var, **kwargs)
        self.master = master
        self.values = values or []
        self.filtered_values = self.values
        self.dropdown_visible = False
        self.selected_index = None
        self.dropdown_window = None
        self.dropdown_frame = None
        self.scrollbar = None
        self.listbox = None
        self.create_dropdown()
        self.track_parent_movement()
        self.selection_callback = selection_callback

        self.bind("<KeyRelease>", self.on_keyrelease)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Down>", self.on_arrow_down)
        self.bind("<Up>", self.on_arrow_up)
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.hide_dropdown)
        self.bind("<Button-1>", self.on_click)

        # Bind a global click event to detect outside clicks
        self.master.bind("<Button-1>", self.on_global_click, "+")

    def create_dropdown(self):
        # this method needs to be the first to be defined - keep this at the top *** *** ***

        self.dropdown_window = tk.Toplevel(self)
        self.dropdown_window.withdraw()
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.attributes("-topmost", True)

        self.dropdown_frame = ctk.CTkFrame(self.dropdown_window, corner_radius=0)
        self.dropdown_frame.pack(fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.dropdown_frame, orientation="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            self.dropdown_frame,
            yscrollcommand=self.scrollbar.set,
            selectmode="browse",
            activestyle="none",
            exportselection=False
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.configure(command=self.listbox.yview)

        self.listbox.bind("<Leave>", self.on_listbox_leave)
        self.listbox.bind("<Motion>", self.on_listbox_motion)
        self.listbox.bind("<Button-1>", self.on_listbox_click)

    def on_click(self, event):
        if not self.dropdown_visible:
            self.update_filtered_values()
            self.show_dropdown()

    def on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        self.update_filtered_values()
        self.show_dropdown()

    def on_focus_in(self, event=None):
        self.configure(insertontime=600)
        self.update_filtered_values()
        self.show_dropdown()

    def on_focus_out(self, event=None):
        self.after(50, self.check_focus_out)

    def check_focus_out(self):
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        under_widget = self.dropdown_window.winfo_containing(x, y)

        # Don't hide dropdown if pointer is over dropdown, scrollbar, or listbox
        if not (under_widget and (
                under_widget == self.listbox or under_widget == self.scrollbar or under_widget.winfo_toplevel() == self.dropdown_window)) \
                and not self.winfo_containing(x, y):
            self.hide_dropdown()

    def on_arrow_down(self, event=None):
        if not self.dropdown_visible:
            self.update_filtered_values()
            self.show_dropdown()
        if self.filtered_values:
            if self.selected_index is None:
                self.selected_index = 0
            else:
                self.selected_index = (self.selected_index + 1) % len(self.filtered_values)
            self.update_listbox_selection()

    def on_arrow_up(self, event=None):
        if self.dropdown_visible and self.filtered_values:
            if self.selected_index is None:
                self.selected_index = len(self.filtered_values) - 1
            else:
                self.selected_index = (self.selected_index - 1) % len(self.filtered_values)
            self.update_listbox_selection()

    def on_return(self, event=None):
        if self.dropdown_visible and self.selected_index is not None:
            value = self.filtered_values[self.selected_index]
            self.set(value)
            if self.selection_callback:
                self.selection_callback(value)
        self.hide_dropdown()

    def on_listbox_select(self, event):
        if not self.listbox.curselection():
            return

        index = self.listbox.curselection()[0]
        value = self.listbox.get(index)

        # Set selected value
        self.var.set(value)
        self.hide_dropdown()

        # Callback for selection
        if self.selection_callback:
            self.selection_callback(value)

    def on_listbox_click(self, event):
        index = self.listbox.nearest(event.y)
        if index >= 0:
            selected = self.listbox.get(index)
            self.var.set(selected)  # update Entry value
            self.set(selected)
            if self.selection_callback:
                self.selection_callback(selected)
            self.after(50, self.hide_dropdown)
            self.icursor(ctk.END)
            self.selection_clear()

    def on_listbox_hover(self, event):
        index = self.listbox.nearest(event.y)
        if 0 <= index < len(self.filtered_values):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.selected_index = index

    def on_listbox_leave(self, event):
        self.listbox.selection_clear(0, tk.END)
        self.selected_index = None

    def on_listbox_motion(self, event):
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(index)
        self.listbox.activate(index)

    def update_filtered_values(self):
        typed = self.get().lower()
        self.filtered_values = [v for v in self.values if typed in v.lower()]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.filtered_values:
            self.listbox.insert(tk.END, item)
        self.selected_index = None

        num_items = len(self.filtered_values)
        height = min(8, num_items)
        self.listbox.configure(height=height)

    def update_listbox_selection(self):
        self.listbox.selection_clear(0, tk.END)
        if self.selected_index is not None:
            self.listbox.selection_set(self.selected_index)
            self.listbox.see(self.selected_index)

    def show_dropdown(self):
        if not self.filtered_values:
            self.hide_dropdown()
            return

        self.update_listbox()

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width = self.winfo_width()
        # Dynamically adjust height based on filtered items (max 8 items, each ~20px height)
        height = min(8, len(self.filtered_values)) * 20
        self.dropdown_window.geometry(f"{width}x{height}+{x}+{y}")
        self.dropdown_window.deiconify()
        self.dropdown_visible = True

    def hide_dropdown(self, event=None):
        self.dropdown_window.withdraw()
        self.dropdown_visible = False
        self.selected_index = None

    def on_global_click(self, event):
        # Prevent hiding dropdown if click is within dropdown window
        if self.dropdown_window and self.dropdown_window.winfo_ismapped():
            widget = event.widget
            if widget == self or widget.winfo_toplevel() == self.dropdown_window:
                return  # Clicked inside dropdown—do nothing

        self.hide_dropdown()

    def update_dropdown_position(self):
        if self.dropdown_window and self.dropdown_window.winfo_ismapped():
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.dropdown_window.geometry(f"+{x}+{y}")

    def track_parent_movement(self):
        if self.dropdown_window and self.dropdown_window.winfo_ismapped():
            self.update_dropdown_position()
        self.after(2, self.track_parent_movement)  # poll every 100 ms

    def set(self, value):
        self.delete(0, tk.END)
        self.insert(0, value)

    def get(self):
        return super().get()
