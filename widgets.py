from tkinter import ttk
from logic import *


class SearchableCombobox(tk.Frame):
    def __init__(self, master, values, max_height=8, **kwargs):
        super().__init__(master)
        self.values = values
        self.filtered_values = list(values)
        self.var = tk.StringVar()

        # Entry widget
        self.entry = ttk.Entry(self, textvariable=self.var, width=kwargs.get("width", 30))
        self.entry.pack(fill=tk.BOTH, expand=True)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.entry.bind("<Button-1>", self.show_dropdown)

        # Keyboard navigation
        self.entry.bind("<Down>", self.on_key_down)
        self.entry.bind("<Up>", self.on_key_up)
        self.entry.bind("<Return>", self.on_return)
        self.entry.bind("<Escape>", self.on_escape)

        # Dropdown frame
        self.dropdown_frame = tk.Toplevel(self)
        self.dropdown_frame.withdraw()
        self.dropdown_frame.overrideredirect(True)
        self.dropdown_frame.attributes("-topmost", True)

        # Scrollable listbox
        self.listbox = tk.Listbox(self.dropdown_frame, activestyle="dotbox", exportselection=False)
        self.scrollbar = tk.Scrollbar(self.dropdown_frame, orient="vertical", command=self.listbox.yview, takefocus=False)
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

        # Focus management
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.listbox.bind("<FocusOut>", self.on_focus_out)

        # Global click-outside check
        self.master.bind_all("<Button-1>", self.check_click_outside)

        # Scrollbar interaction flag
        self.scrollbar_interaction = False
        self.scrollbar.bind("<ButtonPress-1>", self.on_scrollbar_interaction)
        self.scrollbar.bind("<ButtonRelease-1>", self.on_scrollbar_interaction)

        # Window movement reposition
        self.root = self.winfo_toplevel()
        self.root.bind("<Configure>", self.on_window_move)
        self.root.bind("<Unmap>", self.on_root_unmap)
        self.root.bind("<FocusOut>", self.on_root_focus_out)

    def on_root_unmap(self, event=None):
        # Only hide dropdown if the root window was minimized
        if str(self.root.state()) == "iconic":
            self.hide_dropdown()

    def on_root_focus_out(self, event=None):
        # Delay check to allow focus routing to settle
        self.after(2, self._check_app_focus)

    def _check_app_focus(self):
        # Hide dropdown if the app lost focus (i.e., no toplevels have focus)
        focused_widget = self.root.focus_displayof()
        if focused_widget is None or not str(focused_widget).startswith(str(self.root)):
            self.hide_dropdown()

    def on_key_down(self, event=None):
        if not self.listbox_visible:
            self.update_dropdown()
            return "break"
        current_index = self.listbox.index(tk.ACTIVE)
        next_index = current_index + 1 if current_index is not None else 0
        if next_index < self.listbox.size():
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(next_index)
            self.listbox.activate(next_index)
            self.listbox.see(next_index)
        return "break"

    def on_key_up(self, event=None):
        if not self.listbox_visible:
            return "break"
        current_index = self.listbox.index(tk.ACTIVE)
        prev_index = current_index - 1 if current_index is not None else self.listbox.size() - 1
        if prev_index >= 0:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(prev_index)
            self.listbox.activate(prev_index)
            self.listbox.see(prev_index)
        return "break"

    def on_return(self, event=None):
        index = self.listbox.index(tk.ACTIVE)
        if index is not None and 0 <= index < self.listbox.size():
            value = self.listbox.get(index)
            self.var.set(value)
            self.current_selection = value
        self.hide_dropdown()
        return "break"

    def on_escape(self, event):
        self.hide_dropdown()
        return "break"

    def on_keyrelease(self, event=None):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        query = self.var.get().lower()
        self.filtered_values = [v for v in self.values if query in v.lower()] if query else list(self.values)
        self.update_dropdown()

    def show_dropdown(self, event=None):
        if not self.listbox_visible and self.var.get() != self.current_selection:
            self.update_dropdown()
        self.position_dropdown()
        self.entry.focus_set()

    def position_dropdown(self):
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        width = self.entry.winfo_width()
        self.dropdown_frame.geometry(f"{width}x{self.listbox.winfo_reqheight()}+{x}+{y}")
        self.dropdown_frame.deiconify()
        self.listbox_visible = True

    def update_dropdown(self):
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
        self.dropdown_frame.withdraw()
        self.listbox_visible = False

    def on_hover(self, event):
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.activate(index)

    def on_select(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            self.var.set(value)
            self.current_selection = value
        self.hide_dropdown()

    def on_focus_out(self, event=None):
        if self.scrollbar_interaction:
            self.after(100, self._check_focus_loss)


    def _check_focus_loss(self):
        focused_widget = self.root.focus_get()
        if focused_widget not in (self.entry, self.listbox, self.scrollbar):
            self.hide_dropdown()
            self.entry.selection_clear()
            self.entry.icursor(tk.END)
            self.entry.master.focus_set()  # Shift focus to the frame to drop cursor


    def check_click_outside(self, event):
        if self.scrollbar_interaction:
            return
        widget = event.widget
        if widget not in (self.entry, self.listbox, self.scrollbar) and not self._is_child_of(widget,
                                                                                              self.dropdown_frame):
            self.hide_dropdown()
            self.entry.selection_clear()
            self.entry.icursor(tk.END)

    def _is_child_of(self, widget, parent):
        while widget:
            if widget == parent:
                return True
            widget = widget.master
        return False

    def on_scrollbar_interaction(self, event):
        self.scrollbar_interaction = True
        self.after(100, self.reset_scrollbar_interaction)
        self.entry.focus_set()

    def reset_scrollbar_interaction(self):
        self.scrollbar_interaction = False

    def on_window_move(self, event):

        if self.listbox_visible:
            self.after(1, self.position_dropdown)

    def get(self):
        return self.var.get()

    def delete(self, start, end):
        self.entry.delete(start, end)


# class SearchableCombobox(tk.Frame):
#     def __init__(self, master, values=None, placeholder="Search...", *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         self.values = values if values else []
#         self.placeholder = placeholder
#         self.placeholder_active = False
#         self.dropdown_visible = False
#         self.selected_index = None
#
#         self.var = tk.StringVar()
#         self.entry = tk.Entry(self, textvariable=self.var, fg="grey")
#         self.entry.pack(fill=tk.BOTH, expand=True)
#
#         self._set_placeholder()
#
#         self.entry.bind("<FocusIn>", self._on_focus_in)
#         self.entry.bind("<FocusOut>", self._on_focus_out)
#         self.entry.bind("<KeyRelease>", self._on_key_release)
#         self.entry.bind("<Down>", self._on_down_key)
#
#         self.listbox = None
#         self.scrollbar = None
#         self.dropdown_window = None
#
#     def _set_placeholder(self):
#         self.var.set(self.placeholder)
#         self.entry.config(fg="grey")
#         self.placeholder_active = True
#
#     def _clear_placeholder(self):
#         self.var.set("")
#         self.entry.config(fg="black")
#         self.placeholder_active = False
#
#     def _on_focus_in(self, event):
#         if self.placeholder_active:
#             self._clear_placeholder()
#
#     def _on_focus_out(self, event):
#         if not self.var.get():
#             self._set_placeholder()
#         # Close dropdown on focus out (if dropdown wasn't clicked)
#         self.after(100, self._maybe_close_dropdown)
#
#     def _on_key_release(self, event):
#         if self.placeholder_active:
#             return
#         if event.keysym in ("Down", "Up", "Return", "Escape"):
#             return
#         self._update_dropdown()
#
#     def _on_down_key(self, event):
#         if self.dropdown_visible and self.listbox:
#             self.listbox.focus_set()
#             self.listbox.selection_clear(0, tk.END)
#             self.listbox.selection_set(0)
#             self.listbox.activate(0)
#             self.selected_index = 0
#         return "break"
#
#     def _maybe_close_dropdown(self):
#         if self.dropdown_window and not self.entry.focus_get() and not self.listbox.focus_get():
#             self._hide_dropdown()
#
#     def _update_dropdown(self):
#         typed = self.var.get()
#         if not typed:
#             filtered = self.values
#         else:
#             filtered = [item for item in self.values if typed.lower() in item.lower()]
#
#         if not filtered:
#             self._hide_dropdown()
#             return
#
#         if not self.dropdown_window:
#             self._create_dropdown()
#
#         self._populate_listbox(filtered)
#         self._show_dropdown()
#
#     def _create_dropdown(self):
#         self.dropdown_window = tk.Toplevel(self)
#         self.dropdown_window.wm_overrideredirect(True)
#         self.dropdown_window.attributes("-topmost", True)
#
#         self.listbox = tk.Listbox(self.dropdown_window, selectmode=tk.SINGLE, activestyle="none")
#         self.scrollbar = tk.Scrollbar(self.dropdown_window, orient=tk.VERTICAL, command=self.listbox.yview)
#         self.listbox.config(yscrollcommand=self.scrollbar.set)
#
#         self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
#         self.listbox.bind("<ButtonRelease-1>", self._on_listbox_select)
#         self.listbox.bind("<Return>", self._on_listbox_select)
#         self.listbox.bind("<Escape>", lambda e: self._hide_dropdown())
#         self.listbox.bind("<Up>", self._on_listbox_up)
#         self.listbox.bind("<Down>", self._on_listbox_down)
#
#     def _populate_listbox(self, items):
#         self.listbox.delete(0, tk.END)
#         for item in items:
#             self.listbox.insert(tk.END, item)
#
#     def _show_dropdown(self):
#         if not self.dropdown_window or not self.listbox:
#             return
#
#         x = self.entry.winfo_rootx()
#         y = self.entry.winfo_rooty() + self.entry.winfo_height()
#         w = self.entry.winfo_width()
#         max_height = min(len(self.listbox.get(0, tk.END)), 6)
#         h = self.entry.winfo_height() * max_height
#
#         self.dropdown_window.geometry(f"{w}x{h}+{x}+{y}")
#         self.dropdown_window.deiconify()
#         self.dropdown_visible = True
#
#     def _hide_dropdown(self):
#         if self.dropdown_window:
#             self.dropdown_window.withdraw()
#         self.dropdown_visible = False
#         self.selected_index = None
#
#     def _on_listbox_select(self, event):
#         selection = self.listbox.curselection()
#         if selection:
#             index = selection[0]
#             value = self.listbox.get(index)
#             self.var.set(value)
#             self.entry.config(fg="black")
#             self.placeholder_active = False
#         self._hide_dropdown()
#         self.entry.focus_set()
#
#     def _on_listbox_up(self, event):
#         if self.selected_index is not None and self.selected_index > 0:
#             self.selected_index -= 1
#             self.listbox.selection_clear(0, tk.END)
#             self.listbox.selection_set(self.selected_index)
#             self.listbox.activate(self.selected_index)
#         return "break"
#
#     def _on_listbox_down(self, event):
#         size = self.listbox.size()
#         if self.selected_index is not None and self.selected_index < size - 1:
#             self.selected_index += 1
#             self.listbox.selection_clear(0, tk.END)
#             self.listbox.selection_set(self.selected_index)
#             self.listbox.activate(self.selected_index)
#         return "break"
#
#     def get(self):
#         if self.placeholder_active:
#             return ""
#         return self.var.get()
#
#     def set(self, value):
#         self.var.set(value)
#         self.entry.config(fg="black")
#         self.placeholder_active = False
