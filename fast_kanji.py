#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2025 stormoid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Fast Kanji - A Kanji Component Search App
https://github.com/stormoid/fast_kanji

["Small tool to quickly Search for Kanji based on the English meaning of components.
This way, if you know your radicals, you won't need to play where's waldo to find kanjis quickly"]
"""
import json
import os
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import scrolledtext

class KanjiSearchApp:
    def __init__(self, master, data_file, kanjidic_file):
        self.master = master
        master.title("Fast Kanji — stormoid")
        master.geometry("900x850")
        self.med_font = ("Arial", 13)
        self.large_font = ("Arial", 18)

        # --- Styling ---
        self.setup_styles()

        # Load Kanji data
        self.kanji_data = self.load_kanji_data(data_file)

        # Load Kanjidic2 data
        self.kanjidic_data = self.load_kanjidic_data(kanjidic_file)

        # Store selected components
        self.selected_components = set()
        
        # Common Kanji Only Checkbox
        self.common_only = tk.BooleanVar(value=True)

        # Create widgets (now called before set_theme_colors)
        self.create_widgets()

        # Apply initial theme (now called after creating widgets)
        self.set_theme_colors(self.current_theme)

    def setup_styles(self):
        """Sets up the dark and light mode styles."""

        self.style = ttk.Style()

        # --- Dark Mode Colors ---
        self.dark_bg_color = "#313335"  # Dark grey background
        self.dark_fg_color = "#EAEAE5"  # Light grey text
        self.dark_button_bg = "#212325"
        self.dark_button_fg = "#EAEAE5"
        self.dark_listbox_bg = "#292B2D"
        self.dark_listbox_fg = "#EAEAE5"
        self.dark_listbox_select_bg = "#444444"
        self.dark_listbox_select_fg = "#EAEAE5"
        self.dark_entry_bg = "#292B2D"
        self.dark_entry_fg = "#EAEAE5"
        self.dark_frame_bg = "#313335"
        self.dark_entry_insert_bg = "#EAEAE5"

        # --- Light Mode Colors ---
        self.light_bg_color = "#D3C4A5"  # White background
        self.light_fg_color = "#000000"  # Black text
        self.light_button_bg = "#E0E0E0"
        self.light_button_fg = "#000000"
        self.light_listbox_bg = "#C4B597"
        self.light_listbox_fg = "#000000"
        self.light_listbox_select_bg = "#A59778"
        self.light_listbox_select_fg = "#000000"
        self.light_entry_bg = "#C4B597"
        self.light_entry_fg = "#000000"
        self.light_frame_bg = "#D3C4A5"
        self.light_entry_insert_bg = "#000000"

        # --- Common Styling ---
        self.style.configure('TLabelframe.Label', font=("Arial", 15))

        # --- Initial Theme ---
        self.current_theme = "dark"  # Start with dark mode

    def set_theme_colors(self, theme):
        """Sets the theme colors based on the selected theme."""

        if theme == "dark":
            bg_color = self.dark_bg_color
            fg_color = self.dark_fg_color
            button_bg = self.dark_button_bg
            button_fg = self.dark_button_fg
            listbox_bg = self.dark_listbox_bg
            listbox_fg = self.dark_listbox_fg
            listbox_select_bg = self.dark_listbox_select_bg
            listbox_select_fg = self.dark_listbox_select_fg
            entry_bg = self.dark_entry_bg
            entry_fg = self.dark_entry_fg
            frame_bg = self.dark_frame_bg
            entry_insert_bg = self.dark_entry_insert_bg
            self.style.theme_use('default')
        else:  # Light mode
            bg_color = self.light_bg_color
            fg_color = self.light_fg_color
            button_bg = self.light_button_bg
            button_fg = self.light_button_fg
            listbox_bg = self.light_listbox_bg
            listbox_fg = self.light_listbox_fg
            listbox_select_bg = self.light_listbox_select_bg
            listbox_select_fg = self.light_listbox_select_fg
            entry_bg = self.light_entry_bg
            entry_fg = self.light_entry_fg
            frame_bg = self.light_frame_bg
            entry_insert_bg = self.light_entry_insert_bg
            self.style.theme_use('default')

        # Configure default colors for ttk widgets
        self.style.configure('.', background=frame_bg, foreground=fg_color,
                        insertbackground=entry_insert_bg, fieldbackground=entry_bg,
                        selectbackground=listbox_select_bg, selectforeground=listbox_select_fg)

        # Remove border from LabelFrame (affects all LabelFrames)
        self.style.configure('TLabelframe', borderwidth=0, relief='flat')

        # Configure other specific ttk widget elements
        self.style.configure('TLabel', background=frame_bg, foreground=fg_color)
        self.style.configure('TFrame', background=frame_bg)
        self.style.configure('TLabelframe.Label', background=frame_bg, foreground=fg_color)
        self.style.configure('TCheckbutton', background=frame_bg, foreground=fg_color, focuscolor=frame_bg)
        self.style.map('TCheckbutton',
           indicatorcolor=[("selected", "#079EAA"), ("!selected", frame_bg)],
           background=[('active', frame_bg)]
        )

        # Update colors of existing widgets
        self.master.configure(bg=bg_color)
        self.input_text.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_insert_bg, relief="flat")
        self.components_listbox.configure(bg=listbox_bg, fg=listbox_fg, selectbackground=listbox_select_bg, selectforeground=listbox_select_fg, borderwidth=0, highlightthickness=0, relief="flat")
        self.results_listbox.configure(bg=listbox_bg, fg=listbox_fg, selectbackground=listbox_select_bg, selectforeground=listbox_select_fg, borderwidth=0, highlightthickness=0, relief="flat")
        self.kanji_details_text.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_insert_bg, relief="flat")
    
    def toggle_theme(self):
        """Toggles between dark and light themes."""
        if self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        self.set_theme_colors(self.current_theme)

    def create_widgets(self):
        """Creates and places the widgets in the window."""

        # Input Frame
        input_frame = ttk.LabelFrame(self.master, text="Enter Component Meanings (one per line)")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5, font=self.med_font)
        self.input_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.input_text.bind("<KeyRelease>", self.update_results)

        # Checkboxes Frame (to hold both checkboxes)
        checkboxes_frame = ttk.Frame(input_frame)
        checkboxes_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Common Only Checkbox
        common_checkbox = ttk.Checkbutton(checkboxes_frame, text="Common Kanjis Only (2500)", variable=self.common_only, command=self.update_kanji_results)
        common_checkbox.pack(side="left", padx=(0, 10))

        # Theme Toggle Checkbox
        self.theme_toggle_checkbox = ttk.Checkbutton(checkboxes_frame, text="Light Mode", command=self.toggle_theme)
        self.theme_toggle_checkbox.pack(side="right", padx=(10, 0))

        # Matching Components and Kanji Frame
        components_kanji_frame = ttk.Frame(self.master)
        components_kanji_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Matching Components Frame
        self.components_frame = ttk.LabelFrame(components_kanji_frame, text="Matching Components")
        self.components_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        self.components_listbox = tk.Listbox(self.components_frame, selectmode=tk.MULTIPLE, exportselection=False, font=self.large_font)
        self.components_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.components_listbox.bind("<<ListboxSelect>>", self.on_component_select)

        # Results Frame (Matching Kanji)
        results_frame = ttk.LabelFrame(components_kanji_frame, text="Matching Kanji")
        results_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.results_listbox = tk.Listbox(results_frame, exportselection=False, font=self.large_font)
        self.results_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.results_listbox.bind("<<ListboxSelect>>", self.on_kanji_select)

        # Kanji Details Frame
        kanji_details_frame = ttk.LabelFrame(self.master, text="Kanji Details")
        kanji_details_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.kanji_details_text = scrolledtext.ScrolledText(kanji_details_frame, wrap=tk.WORD, height=12, state="disabled", font=self.large_font)
        self.kanji_details_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configure grid resizing
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)  # Allow input_text to expand vertically
        input_frame.columnconfigure(0, weight=1) # Allow input_text to expand horizontally
        checkboxes_frame.columnconfigure(0, weight=1)
        components_kanji_frame.rowconfigure(0, weight=1)
        components_kanji_frame.columnconfigure(0, weight=1)
        components_kanji_frame.columnconfigure(1, weight=1)
        self.components_frame.rowconfigure(0, weight=1)
        self.components_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        kanji_details_frame.rowconfigure(0, weight=1)
        kanji_details_frame.columnconfigure(0, weight=1)
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("./data")

        return os.path.join(base_path, relative_path)

    def load_kanji_data(self, data_file):
        """Loads the Kanji data from the JSON file."""
        data_file_path = self.resource_path(data_file)
        try:
            with open(data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{data_file_path}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{data_file_path}'.")
            return {}

    def load_kanjidic_data(self, kanjidic_file):
        """Loads the Kanjidic2 data from the JSON file."""
        kanjidic_file_path = self.resource_path(kanjidic_file)
        try:
            with open(kanjidic_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{kanjidic_file_path}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{kanjidic_file_path}'.")
            return {}

    def update_results(self, event=None):
        """Updates the results based on the input text."""
        meanings = self.input_text.get("1.0", tk.END).strip().split('\n')
        meanings = [m.strip() for m in meanings if m.strip()]

        if len("".join(meanings)) < 1:
            self.components_listbox.delete(0, tk.END)
            self.results_listbox.delete(0, tk.END)
            self.kanji_details_text.config(state="normal")
            self.kanji_details_text.delete("1.0", tk.END)
            #self.kanji_details_text.insert(tk.END, "Enter a letter to search.\n")
            self.kanji_details_text.config(state="disabled")
            return

        self.matching_components = self.find_matching_components(meanings)
        self.update_component_listbox()
        self.update_kanji_results()

    def update_component_listbox(self):
        """Updates the listbox of matching components."""
        self.components_listbox.delete(0, tk.END)

        for component, details in self.matching_components.items():
            if 'meaning' in details:
                self.components_listbox.insert(tk.END, f"{component} ({details['meaning']})")

    def on_component_select(self, event=None):
        """Handles component selection from the listbox."""
        # Prevent deselection when clicking on Kanji listbox
        self.master.after(10, self.keep_component_selection)

        selected_indices = self.components_listbox.curselection()
        new_selected_components = {list(self.matching_components.keys())[index] for index in selected_indices}

        if self.selected_components != new_selected_components:
            self.selected_components = new_selected_components
            self.update_kanji_results()

    def keep_component_selection(self):
        """Keeps the component selection active."""
        selected_indices = [list(self.matching_components.keys()).index(comp) for comp in self.selected_components if comp in self.matching_components]
        for index in selected_indices:
            self.components_listbox.selection_set(index)

    def update_kanji_results(self):
        """Updates the Kanji results based on selected components."""
        matching_kanji = self.find_kanji_with_all_components(self.selected_components)

        self.results_listbox.delete(0, tk.END)
        if matching_kanji:
            for kanji in matching_kanji:
                if self.common_only.get():
                    if self.is_common_kanji(kanji):
                        self.results_listbox.insert(tk.END, kanji)
                else:
                    self.results_listbox.insert(tk.END, kanji)
        else:
            self.results_listbox.insert(tk.END, "No matching Kanji")

    def is_common_kanji(self, kanji):
        """Checks if a Kanji is considered common based on the presence of a frequency value in Kanjidic2."""
        kanji_entry = self.find_kanji_in_kanjidic(kanji)
        if kanji_entry:
            return kanji_entry.get('freq') is not None
        return False

    def find_kanji_in_kanjidic(self, kanji):
        """Finds the Kanji entry in the loaded Kanjidic data."""
        for entry in self.kanjidic_data:
            if entry.get('literal') == kanji:
                return entry
        return None

    def find_matching_components(self, meanings):
        """Finds components that have any of the specified meanings at the beginning of the word."""
        matching_components = {}
        for component, details in self.kanji_data.items():
            if 'meaning' in details:
                component_meanings = [m.strip() for m in details['meaning'].split(',')]
                if any(component_meaning.lower().startswith(meaning.lower()) for meaning in meanings for component_meaning in component_meanings):
                    matching_components[component] = details
        return matching_components

    def find_kanji_with_all_components(self, selected_components):
        """Finds Kanji that contain all the specified components."""
        if not selected_components:
            return []

        kanji_lists = [self.kanji_data[component]['kanji'] for component in selected_components if component in self.kanji_data]

        if kanji_lists:
            common_kanji = set(kanji_lists[0])
            for kanji_list in kanji_lists[1:]:
                common_kanji.intersection_update(kanji_list)
            return list(common_kanji)
        else:
            return []

    def on_kanji_select(self, event=None):
        """Handles Kanji selection from the listbox."""
        selected_index = self.results_listbox.curselection()
        if selected_index:
            selected_kanji = self.results_listbox.get(selected_index[0])
            self.display_kanji_details(selected_kanji)

    def display_kanji_details(self, kanji):
        """Displays the details of the selected Kanji."""
        kanji_entry = self.find_kanji_in_kanjidic(kanji)
        if kanji_entry:
            self.kanji_details_text.config(state="normal")
            self.kanji_details_text.delete("1.0", tk.END)

            literal = kanji_entry.get('literal', '')
            jisho_url = f"https://jisho.org/search/{literal}%20%23kanji"
            kanshudo_url = f"https://www.kanshudo.com/kanji/{literal}"

            # Insert the literal first
            self.kanji_details_text.insert(tk.END, f"{literal} | ")

            # Add Jisho link
            self.kanji_details_text.insert(tk.END, "Jisho", "jisho_link")
            self.kanji_details_text.tag_config("jisho_link", foreground="#079EAA", underline=0)
            self.kanji_details_text.tag_bind("jisho_link", "<Button-1>", lambda e, url=jisho_url: self.open_url(url))

            # Add separator
            self.kanji_details_text.insert(tk.END, " — ")

            # Add Kanshudo link
            self.kanji_details_text.insert(tk.END, "Kanshudo", "kanshudo_link")
            self.kanji_details_text.tag_config("kanshudo_link", foreground="#079EAA", underline=0)
            self.kanji_details_text.tag_bind("kanshudo_link", "<Button-1>", lambda e, url=kanshudo_url: self.open_url(url))

            # Add a newline for better formatting
            self.kanji_details_text.insert(tk.END, "\n")

            # Now add the rest of the details
            details = self.extract_kanji_details(kanji_entry)
            self.kanji_details_text.insert(tk.END, details)

            self.kanji_details_text.config(state="disabled")
        else:
            self.kanji_details_text.config(state="normal")
            self.kanji_details_text.delete("1.0", tk.END)
            self.kanji_details_text.insert(tk.END, "Kanji details not found in Kanjidic2.")
            self.kanji_details_text.config(state="disabled")


    def extract_kanji_details(self, kanji_entry):
        """Extracts details from a Kanjidic2 character entry (JSON format)."""
        literal = kanji_entry.get('literal', '')
        details = ""

        # Meanings
        meanings = kanji_entry.get('reading_meaning', {}).get('meaning', [])
        if meanings:
            details += "Meanings: " + ", ".join(meanings) + "\n"

        # Readings
        readings_on = [r['value'] for r in kanji_entry.get('reading_meaning', {}).get('reading', []) if r['r_type'] == 'ja_on']
        readings_kun = [r['value'] for r in kanji_entry.get('reading_meaning', {}).get('reading', []) if r['r_type'] == 'ja_kun']

        if readings_on or readings_kun:
            details += "\nReadings:\n"
            if readings_on:
                details += "On: " + "  or  ".join(readings_on) + "\n"
            if readings_kun:
                details += "Kun: " + "  or  ".join(readings_kun) + "\n"

        grade = kanji_entry.get('grade')
        stroke_count = kanji_entry.get('stroke_count')
        freq = kanji_entry.get('freq')
        jlpt = kanji_entry.get('jlpt')

        details += "\n"
        if grade:
            details += f"Grade: {grade}\n"
        if stroke_count:
            details += f"Stroke Count: {stroke_count}\n"
        if freq:
            details += f"Frequency: {freq}\n"
        if jlpt:
            details += f"JLPT Level: {jlpt}\n"

        return details

    def open_url(self, url):
        """Opens the given URL in the default web browser."""
        webbrowser.open_new(url)

def main():
    root = tk.Tk()
    app = KanjiSearchApp(root, "fullcomps.json", "kanjidic2_stripped.json")
    root.mainloop()

if __name__ == "__main__":
    main()
