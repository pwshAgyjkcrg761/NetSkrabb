# ==============================================================================
# SCRIPT: NetSkraab.py
# VERSION: 2026.07.04__13.30.28
# TARGET: Python 3.14.5
#
# Copyright (C) 2026 pwshAgyjkcrg761
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
# ==============================================================================
# <PROTECTED>
# ==============================================================================
# AI INSTRUCTIONS v2026.06.24__06.54.45 : 
#
# 1. MESSAGE STAMP: 
#    - Every response containing code MUST begin with a standalone version stamp.
#    - Use CHICAGO TIME (Central Time), 24-hour clock.
#    - Format: YYYY.MM.DD__HH.MM.SS.
#    - CRITICAL: Use the time provided in the prompt or at https://www.timeanddate.com/worldclock/usa/chicago. Ensure minutes are exact.
#
# 2. VERSION SNIPPET PROHIBITION:
#    - DO NOT provide code snippets, anchors, or steps to update the script's internal VERSION comment or $scriptVersion variable. 
#    - The user handles internal file versioning manually based on the Message Stamp.
#
# 3. SCRIPT OUTPUT (SURGICAL FIXES ONLY):
#    - Provide minimal, highly targeted, surgical edits. Do not rewrite large blocks or entire functions.
#    - Always use a codebox with a copy button.
#    - Multiple modifications MUST be presented strictly ONE step at a time. Wait for user confirmation before proceeding to the next step. 
#    - DO NOT modify or refactor any code inside <PROTECTED> tags.
#
# 4. VERBATIM ANCHOR PROTOCOL (FOR NOTEPAD++):
#    - To facilitate "Find" in Notepad++, always structure edits with:
#      - "Verbatim Anchor (Before)" - The exact lines of existing code immediately before the change.
#      - "Verbatim Anchor (After)" - The exact lines of existing code immediately after the change.
#      - "Snippet to REPLACE" - The exact code block to be deleted.
#      - "What to PASTE in its place" - The new code block to be inserted.
#    - Do not summarize, truncate, or refactor the existing code used as an anchor.
#    - Match spaces, comments, and symbols exactly as they appear in the file.
#
# 5. CONTENT PRESERVATION:
#    - Do not remove, modify, or strip out telemetry data or DevDebug information from any provided code.
#==============================================================================
#==============================================================================
# </PROTECTED>
import sys
from PyQt6.QtWidgets import (QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QPlainTextEdit, QMenuBar, QStatusBar)
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QComboBox, QDialog, QCheckBox, QDialogButtonBox, QFrame

# Easily maintainable application metadata configuration
APP_VERSION = "2026.07.04__13.30.28"

class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(400, 300)
        
        self.init_ui(current_settings)

    def init_ui(self, settings):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # 1. Master Checkbox
        self.chk_enable_all = QCheckBox("Enable All (Overrides individual settings below)")
        layout.addWidget(self.chk_enable_all)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # 2. Pipeline Ordered Checkboxes
        self.chk_remove_part = QCheckBox("Remove \"Part\" Text Prefix")
        self.chk_convert_slash = QCheckBox("Convert Forward Slash to Division Slash (∕)")
        self.chk_fullwidth_chars = QCheckBox("Use Legal Full-width Variants (？ and ；)")
        self.chk_remove_illegal = QCheckBox("Remove Remaining Windows Illegal Characters")
        self.chk_lowercase = QCheckBox("Lowercase Mode")

        # Helper function to generate clean description labels for examples
        def make_example_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #888888; margin-left: 20px; font-size: 11px;")
            return lbl

        lbl_part_ex = make_example_label("Example: \"part 2\" or \"title (2)\" becomes \"2\" or \"title 2\"")
        lbl_slash_ex = make_example_label("Example: Allows \"/\" to display visually as \"∕\" without breaking folder trees")
        lbl_fw_ex = make_example_label("Example: Converts standard \"?\" and \";\" to safe \"？\" and \"；\" for shells like PowerShell")
        lbl_illegal_ex = make_example_label("Example: Strips raw \\ / : * ? \" < > | characters, and removes the standard legal ;")
        lbl_lower_ex = make_example_label("Example: Forces all final text output characters into lowercase format")

        # Grouping sub-checkboxes for easy macro loop operations
        self.sub_checkboxes = [
            self.chk_remove_part,
            self.chk_convert_slash,
            self.chk_fullwidth_chars,
            self.chk_remove_illegal,
            self.chk_lowercase
        ]

        # Grouping labels to match up with the disable/enable interlocking toggles
        self.example_labels = [lbl_part_ex, lbl_slash_ex, lbl_fw_ex, lbl_illegal_ex, lbl_lower_ex]

        # Alternating layouts step-by-step down the display widget stack
        layout.addWidget(self.chk_remove_part)
        layout.addWidget(lbl_part_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_convert_slash)
        layout.addWidget(lbl_slash_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_fullwidth_chars)
        layout.addWidget(lbl_fw_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_remove_illegal)
        layout.addWidget(lbl_illegal_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_lowercase)
        layout.addWidget(lbl_lower_ex)
        layout.addSpacing(8)

        # 3. Dialog Buttons (Save / Cancel)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Load states from configuration dict
        self.chk_enable_all.setChecked(settings.get('enable_all', True))
        self.chk_remove_part.setChecked(settings.get('remove_part', True))
        self.chk_convert_slash.setChecked(settings.get('convert_slash', True))
        self.chk_fullwidth_chars.setChecked(settings.get('fullwidth_chars', True))
        self.chk_remove_illegal.setChecked(settings.get('remove_illegal', True))
        self.chk_lowercase.setChecked(settings.get('lowercase', True))

        # Connect Master checkbox toggle to the interlocking gray-out behavior
        self.chk_enable_all.toggled.connect(self.update_sub_checkboxes_status)
        self.update_sub_checkboxes_status(self.chk_enable_all.isChecked())

    def update_sub_checkboxes_status(self, checked):
        # When Enable All is manipulated, update visual states, checkboxes, and description labels
        for chk in self.sub_checkboxes:
            chk.setDisabled(checked)
            chk.setChecked(checked)
        for lbl in self.example_labels:
            lbl.setDisabled(checked)

    def get_settings(self):
        return {
            'enable_all': self.chk_enable_all.isChecked(),
            'remove_part': self.chk_remove_part.isChecked(),
            'convert_slash': self.chk_convert_slash.isChecked(),
            'fullwidth_chars': self.chk_fullwidth_chars.isChecked(),
            'remove_illegal': self.chk_remove_illegal.isChecked(),
            'lowercase': self.chk_lowercase.isChecked()
        }

class EpListCleanUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"NetSkrabb v{APP_VERSION}")
        import json
        import os

        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NetSkraab.config.json")
        
        # Baseline fallback defaults
        default_settings = {
            'enable_all': True,
            'remove_part': True,
            'convert_slash': True,
            'fullwidth_chars': True,
            'remove_illegal': True,
            'lowercase': True,
            'min_digits': 2,
            'theme': 'System',
            'profile': 'MyAnimeList.net'
        }

        # Try to load existing configuration, otherwise use defaults
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.settings_config = json.load(f)
            except Exception:
                self.settings_config = default_settings
        else:
            self.settings_config = default_settings

        # Manage Window Sizing and Coordinates Geometry
        default_width = 700
        default_height = 600

        if 'window_x' in self.settings_config and 'window_y' in self.settings_config:
            # Restore saved size and desktop space coordinates
            self.setGeometry(
                self.settings_config['window_x'],
                self.settings_config['window_y'],
                self.settings_config.get('window_w', default_width),
                self.settings_config.get('window_h', default_height)
            )
        else:
            # First launch execution: center horizontally and vertically on primary screen
            from PyQt6.QtGui import QGuiApplication
            primary_screen = QGuiApplication.primaryScreen()
            if primary_screen:
                screen_geometry = primary_screen.availableGeometry()
                center_x = int((screen_geometry.width() - default_width) / 2) + screen_geometry.x()
                # To push the window down visually, add a static pixel offset to center_y (e.g., + 40)
                center_y = int((screen_geometry.height() - default_height) / 2) + screen_geometry.y() + 30
                self.setGeometry(center_x, center_y, default_width, default_height)
            else:
                self.setGeometry(100, 100, default_width, default_height)

        # Re-apply maximized desktop scaling bounds if it was closed in that state
        if self.settings_config.get('window_maximized', False):
            self.showMaximized()
        
        # Apply the configured theme engine stylesheet rules on launch
        self.apply_theme_stylesheet(self.settings_config.get('theme', 'System'))

        self.init_ui()

    def init_ui(self):
        # 1. Menu Bar
        self.create_menu_bar()
        
        # Main Layout container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 2. URL Input Row
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste webpage URL here...")
        self.fetch_btn = QPushButton("Fetch Text")
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.fetch_btn)
        main_layout.addLayout(url_layout)

        # 3. Profile Selection Row
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Site Profile:")
        self.profile_dropdown = QComboBox()
        self.profile_dropdown.addItems(["MyAnimeList.net", "epguides.com", "Wikipedia.org"])
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.profile_dropdown)
        # Dictionary classifying site profiles by region/type
        self.profile_types = {
            "MyAnimeList.net": "Anime",
            "epguides.com": "Western",
            "Wikipedia.org": "Western"
        }

        # Add a spacing stretch, then insert the dynamic episode number width box
        profile_layout.addSpacing(20)
        
        from PyQt6.QtWidgets import QSpinBox
        self.digits_label = QLabel("Min Digits:")
        self.digits_spinbox = QSpinBox()
        self.digits_spinbox.setRange(1, 9)
        self.digits_spinbox.setValue(self.settings_config.get('min_digits', 2))
        from PyQt6.QtCore import Qt
        self.digits_spinbox.setFixedWidth(75)  # Expanded width to leave typing space
        self.digits_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Keep text neatly centered
        
        # Automatically update the persistent config dictionary whenever the user changes the box value
        self.digits_spinbox.valueChanged.connect(self.save_digits_config_directly)
        
        profile_layout.addWidget(self.digits_label)
        profile_layout.addWidget(self.digits_spinbox)
        profile_layout.addStretch()
        main_layout.addLayout(profile_layout)

        # Select the last saved profile configuration on launch
        saved_profile = self.settings_config.get('profile', 'MyAnimeList.net')
        profile_index = self.profile_dropdown.findText(saved_profile)
        if profile_index >= 0:
            self.profile_dropdown.setCurrentIndex(profile_index)

        # Connect signals for runtime changes
        self.profile_dropdown.currentTextChanged.connect(self.toggle_digits_visibility)
        self.profile_dropdown.currentTextChanged.connect(self.save_profile_config_directly)

        # Absolute Numbering Row Container (for dynamic visibility toggles)
        self.abs_container = QWidget()
        abs_layout = QHBoxLayout(self.abs_container)
        abs_layout.setContentsMargins(0, 0, 0, 0)
        
        self.abs_checkbox = QCheckBox("Use Absolute Numbering")
        self.abs_checkbox.setChecked(self.settings_config.get('use_absolute', False))
        
        self.abs_start_label = QLabel("Start Number:")
        self.abs_start_spinbox = QSpinBox()
        self.abs_start_spinbox.setRange(1, 9999)
        self.abs_start_spinbox.setValue(self.settings_config.get('abs_start_num', 1))
        self.abs_start_spinbox.setFixedWidth(85)
        self.abs_start_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.abs_start_spinbox.setGroupSeparatorShown(False)
        
        self.abs_checkbox.toggled.connect(self.save_absolute_config_directly)
        self.abs_start_spinbox.valueChanged.connect(lambda: self.save_absolute_config_directly())
        
        self.abs_start_label.setEnabled(self.abs_checkbox.isChecked())
        self.abs_start_spinbox.setEnabled(self.abs_checkbox.isChecked())
        self.abs_checkbox.toggled.connect(lambda checked: self.abs_start_label.setEnabled(checked))
        self.abs_checkbox.toggled.connect(lambda checked: self.abs_start_spinbox.setEnabled(checked))
        
        abs_layout.addWidget(self.abs_checkbox)
        abs_layout.addSpacing(10)
        abs_layout.addWidget(self.abs_start_label)
        abs_layout.addWidget(self.abs_start_spinbox)
        abs_layout.addStretch()
        main_layout.addWidget(self.abs_container)

        # 4. Input Text Box Area
        input_label = QLabel("Raw Text / Source Code:")
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("Paste raw web text here or fetch from a URL...")
        
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_text)

        # Image Download Contextual Layout
        self.image_layout = QHBoxLayout()
        
        self.img_download_checkbox = QCheckBox("Download Cover Image", self)
        self.img_download_checkbox.setChecked(False)
        self.img_download_checkbox.stateChanged.connect(self.toggle_img_button_state)
        self.image_layout.addWidget(self.img_download_checkbox)
        
        self.img_choose_btn = QPushButton("Choose Cover...", self)
        self.img_choose_btn.setEnabled(False)
        self.img_choose_btn.clicked.connect(self.open_image_picker_dialog)
        self.image_layout.addWidget(self.img_choose_btn)
        
        main_layout.addLayout(self.image_layout)

        # 4. Action Button
        self.clean_btn = QPushButton("CLEAN && FORMAT")
        # Make the main action button stand out slightly with a larger font
        btn_font = QFont()
        btn_font.setBold(True)
        btn_font.setPointSize(10)
        self.clean_btn.setFont(btn_font)
        self.clean_btn.setMinimumHeight(40)
        
        main_layout.addWidget(self.clean_btn)

        # 5. Output Text Box Area
        output_label = QLabel("Cleaned Windows Filenames:")
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)  # Protect output from accidental typing
        self.output_text.setPlaceholderText("Cleaned results will appear here...")
        
        main_layout.addWidget(output_label)
        main_layout.addWidget(self.output_text)

        # 6. Quick Action Row (Clear & Copy)
        copy_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.clicked.connect(self.clear_fields)
        copy_layout.addWidget(self.clear_btn)
        
        copy_layout.addStretch()  # Pushes button to the right side
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setMinimumWidth(150)
        copy_layout.addWidget(self.copy_btn)
        
        main_layout.addLayout(copy_layout)

        # 7. Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

        # Connect button placeholders to verify layout interaction later
        self.fetch_btn.clicked.connect(self.placeholder_fetch)
        self.clean_btn.clicked.connect(self.placeholder_clean)
        self.copy_btn.clicked.connect(self.placeholder_copy)

        # Set initial layout visibility state safely now that all elements are initialized
        self.toggle_digits_visibility(self.profile_dropdown.currentText())

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("&File")
        
        clear_action = QAction("&Clear All", self)
        clear_action.setStatusTip("Clear input and output text boxes")
        clear_action.triggered.connect(self.clear_fields)
        
        exit_action = QAction("&Exit", self)
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(clear_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Tools Menu
        tools_menu = menu_bar.addMenu("&Tools")
        settings_action = QAction("&Settings", self)
        settings_action.setStatusTip("Configure global string filter pipelines")
        settings_action.triggered.connect(self.open_settings_dialog)
        tools_menu.addAction(settings_action)
        
        # Theme Sub-Menu
        theme_menu = tools_menu.addMenu("&Theme")
        
        from PyQt6.QtGui import QActionGroup
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)
        
        current_theme = self.settings_config.get('theme', 'System')
        
        for mode in ["Dark", "Light", "System"]:
            action = QAction(mode, self, checkable=True)
            action.setStatusTip(f"Switch application layout to {mode} mode")
            if mode == current_theme:
                action.setChecked(True)
            action.triggered.connect(self.handle_theme_change)
            theme_menu.addAction(action)
            self.theme_group.addAction(action)

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.setStatusTip("Show application version and license details")
        about_action.triggered.connect(self.open_about_dialog)
        help_menu.addAction(about_action)

    def placeholder_fetch(self):
        import urllib.request
        import re
        
        url = self.url_input.text().strip()
        if not url:
            self.statusBar().showMessage("Please provide a URL to fetch.")
            return

        selected_profile = self.profile_dropdown.currentText()

        # Automatically redirect main series entries to their respective episode sub-pages
        if selected_profile == "MyAnimeList.net" and url:
            # Check if it's a main title URL but doesn't already end with /episode or /episode/
            if "/anime/" in url and not re.search(r'/episode(?:/\d+)?/?$', url):
                # Clean up any trailing query parameters or trailing slashes first
                base_url = url.split('?')[0].rstrip('/')
                url = f"{base_url}/episode"
        if selected_profile == "epguides.com":
            self.statusBar().showMessage("Fetching data from epguides.com...")
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_text = response.read().decode('utf-8', errors='ignore')
                
                # Extract the maze export ID parameter embedded in the source html page
                maze_match = re.search(r'exportToCSVmaze\.asp\?maze=(\d+)', html_text, re.IGNORECASE)
                if not maze_match:
                    self.statusBar().showMessage("Could not locate CSV export ID on the epguides page.")
                    return
                
                maze_id = maze_match.group(1)
                csv_url = f"https://epguides.com/common/exportToCSVmaze.asp?maze={maze_id}"
                
                req_csv = urllib.request.Request(csv_url, headers=headers)
                with urllib.request.urlopen(req_csv, timeout=10) as csv_resp:
                    csv_text = csv_resp.read().decode('utf-8', errors='ignore')
                
                # Parse columns safely line-by-line while keeping raw spacing intact
                csv_lines = csv_text.splitlines()
                episodes_found = []
                for line in csv_lines:
                    if not line.strip() or line.startswith('number,'):
                        continue
                    
                    # Split the line from the left side up to the airdate column index
                    parts = line.split(',', 4)
                    if len(parts) >= 5 and parts[0].strip().isdigit():
                        try:
                            s_num = int(parts[1].strip())
                            e_num = int(parts[2].strip())
                            
                            # The remainder string contains: "Title","URL"
                            remainder = parts[4].strip()
                            
                            # Safely extract the title by isolating the text inside the quotes, or splitting from the right URL
                            if remainder.startswith('"'):
                                # Find where the title field quote actually closes before the comma divider
                                if '",' in remainder:
                                    ep_title = remainder.split('",', 1)[0][1:].strip()
                                else:
                                    end_quote_idx = remainder.rfind('"')
                                    ep_title = remainder[1:end_quote_idx].strip()
                            else:
                                # Fallback if titles aren't quoted: split off the last comma separating the URL
                                ep_title = remainder.rsplit(',', 1)[0].strip()
                                
                            if ep_title:
                                import html
                                # Ensure all HTML character entities are fully decoded and explicitly fix ampersands
                                ep_title = html.unescape(ep_title).replace('&amp;', '&').strip()
                                # Re-construct string syntax matching what placeholder_clean looks for
                                episodes_found.append(f"1. {s_num}-{e_num} 00 AAA 00 {ep_title}")
                        except ValueError:
                            continue
                
                if episodes_found:
                    self.input_text.setPlainText('\n'.join(episodes_found))
                    self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} episodes from epguides CSV.")
                else:
                    self.input_text.setPlainText("No valid episode rows could be parsed from the CSV stream.")
                return
            except Exception as e:
                self.statusBar().showMessage(f"Error fetching from epguides: {str(e)}")
                return

        self.statusBar().showMessage("Fetching data from MyAnimeList.net...")
        
        try:
            from html.parser import HTMLParser
            import html

            class MALEpisodesParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.episodes = []
                    self.pagination_urls = set()
                    self.current_num = None
                    self.in_num_cell = False
                    self.in_title_cell = False
                    self.in_title_link = False
                    self.in_pagination = False
                    self.current_title_chunks = []

                def handle_starttag(self, tag, attrs):
                    attrs_dict = dict(attrs)
                    cls = attrs_dict.get('class', '')
                    
                    if tag == 'td' and 'episode-number' in cls:
                        self.in_num_cell = True
                    elif tag == 'td' and 'episode-title' in cls:
                        self.in_title_cell = True
                    elif tag == 'a' and self.in_title_cell:
                        self.in_title_link = True
                        self.current_title_chunks = []
                    elif tag == 'div' and 'pagination' in cls:
                        self.in_pagination = True
                    elif tag == 'a' and self.in_pagination:
                        href = attrs_dict.get('href', '')
                        if href:
                            self.pagination_urls.add(href)

                def handle_data(self, data):
                    if self.in_num_cell:
                        cleaned_num = data.strip()
                        if cleaned_num.isdigit():
                            self.current_num = int(cleaned_num)
                    elif self.in_title_link:
                        self.current_title_chunks.append(data)

                def handle_endtag(self, tag):
                    if tag == 'td' and self.in_num_cell:
                        self.in_num_cell = False
                    elif tag == 'a' and self.in_title_link:
                        self.in_title_link = False
                        full_title = "".join(self.current_title_chunks).strip()
                        full_title = html.unescape(full_title).strip()
                        if self.current_num is not None and full_title and not full_title.startswith('http'):
                            self.episodes.append((self.current_num, full_title))
                    elif tag == 'td' and self.in_title_cell:
                        self.in_title_cell = False
                    elif tag == 'div' and self.in_pagination:
                        self.in_pagination = False

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
            }

            # Phase 1: Fetch the primary page link given in the UI
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html_text = response.read().decode('utf-8', errors='ignore')

            parser = MALEpisodesParser()
            parser.feed(html_text)
            
            # Phase 2: If additional offset pages exist, process them sequentially
            visited_urls = {url}
            extra_urls = sorted(list(parser.pagination_urls))
            
            for extra_url in extra_urls:
                if extra_url not in visited_urls:
                    visited_urls.add(extra_url)
                    try:
                        self.statusBar().showMessage(f"Fetching additional episodes from offset page...")
                        req_extra = urllib.request.Request(extra_url, headers=headers)
                        with urllib.request.urlopen(req_extra, timeout=10) as response_extra:
                            html_extra = response_extra.read().decode('utf-8', errors='ignore')
                        parser.feed(html_extra)
                    except Exception:
                        pass

            # De-duplicate rows by episode number and format output text cleanly
            unique_episodes = {}
            for ep_num, full_title in parser.episodes:
                unique_episodes[ep_num] = full_title
                
            episodes_found = [f"{num} {unique_episodes[num]}" for num in sorted(unique_episodes.keys())]

            if episodes_found:
                self.input_text.setPlainText('\n'.join(episodes_found))
                self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} episodes from MyAnimeList.")
            else:
                self.input_text.setPlainText("No episodes could be found using the structural HTML parser.")
                self.statusBar().showMessage("Fetch complete, but no matching table rows found.")
                
        except Exception as e:
            self.statusBar().showMessage(f"Network error during fetch: {str(e)}")

    def placeholder_clean(self):
        import re
        raw_text = self.input_text.toPlainText()
        if not raw_text.strip():
            self.statusBar().showMessage("No text to clean.")
            return

        selected_profile = self.profile_dropdown.currentText()
        cleaned_episodes = []

        if selected_profile == "MyAnimeList.net":
            current_abs_num = self.abs_start_spinbox.value() if self.abs_checkbox.isChecked() else None
            
            for line in raw_text.splitlines():
                line_str = line.strip()
                match = re.match(r'^(\d+)\s+(.+)$', line_str)
                if match:
                    raw_title = match.group(2).strip()
                    title_part = re.sub(r'^(Filler|Recap)', '', raw_title).strip()

                    # Apply the centralized configuration text transformations
                    title_part = self.apply_user_filters(title_part)

                    # Determine target number sequence assignment rule
                    if current_abs_num is not None:
                        target_num = current_abs_num
                        current_abs_num += 1
                    else:
                        target_num = int(match.group(1))

                    # Dynamically pull padding constraints directly from the GUI selector
                    digit_width = self.digits_spinbox.value()
                    formatted_line = f"{target_num:0{digit_width}d} {title_part}"
                    cleaned_episodes.append(formatted_line)
                        
        else:
            # Shared processing pipeline for Western profiles (4-digit matrix format)
            def format_western_episode(season, episode, raw_title):
                clean_title = re.sub(r'^(Filler|Recap)', '', raw_title).strip()
                clean_title = self.apply_user_filters(clean_title)
                return f"{season:02d}{episode:02d} {clean_title}"

            if selected_profile == "epguides.com":
                for line in raw_text.splitlines():
                    line_str = line.strip()
                    match = re.match(r'^\d+\.\s+(\d+)-(\d+)\s+\d{2}\s+[A-Za-z]{3}\s+\d{2}\s+(.+)$', line_str)
                    if match:
                        cleaned_episodes.append(
                            format_western_episode(int(match.group(1)), int(match.group(2)), match.group(3))
                        )
            
            elif selected_profile == "Wikipedia.org":
                current_season = 1
                for line in raw_text.splitlines():
                    line_str = line.strip()
                    season_match = re.search(r'\bSeason\s+(\d+)\b', line_str, flags=re.IGNORECASE)
                    if season_match:
                        current_season = int(season_match.group(1))
                        continue
                    
                    match = re.search(r'^\d+\s+(\d+)\s+"([^"]+)"', line_str)
                    if match:
                        cleaned_episodes.append(
                            format_western_episode(current_season, int(match.group(1)), match.group(2))
                        )

        if cleaned_episodes:
            self.output_text.setPlainText('\n'.join(cleaned_episodes))
            self.statusBar().showMessage(f"Successfully cleaned {len(cleaned_episodes)} episodes.")
        else:
            self.statusBar().showMessage("Could not find any matching episode patterns.")

    def placeholder_copy(self):
        output_content = self.output_text.toPlainText()
        if not output_content.strip():
            self.statusBar().showMessage("No cleaned text to copy.")
            return
            
        clipboard = QApplication.clipboard()
        clipboard.setText(output_content)
        self.statusBar().showMessage("Cleaned text successfully copied to clipboard.")

    def clear_fields(self):
        self.url_input.clear()
        self.input_text.clear()
        self.output_text.clear()
        self.statusBar().showMessage("Fields cleared")

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.settings_config, self)
        if dialog.exec():
            import json
            self.settings_config = dialog.get_settings()
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings_config, f, indent=4)
                self.statusBar().showMessage("Settings successfully saved to config file.")
            except Exception as e:
                self.statusBar().showMessage(f"Settings saved in memory, but failed to write to disk: {str(e)}")

    def open_about_dialog(self):
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtCore import Qt
        
        about_text = (
            f"<b>NetSkraab v{APP_VERSION}</b><br>"
            "Copyright (C) 2026 pwshAgyjkcrg761<br>"
            "GPLv3<br><br>"
            "This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.<br><br>"
            "This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details.<br><br>"
            "You should have received a copy of the GNU General Public License "
            "along with this program. If not, see "
            "<a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">https://www.gnu.org/licenses/gpl-3.0.html</a>."
        )
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About NetSkraab")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(about_text)
        msg_box.exec()

    def handle_theme_change(self):
        import json
        selected_action = self.theme_group.checkedAction()
        if not selected_action:
            return
            
        theme_mode = selected_action.text()
        self.settings_config['theme'] = theme_mode
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings_config, f, indent=4)
            self.apply_theme_stylesheet(theme_mode)
            self.statusBar().showMessage(f"Theme changed to {theme_mode}")
        except Exception:
            pass

    

    def save_digits_config_directly(self, value):
        import json
        self.settings_config['min_digits'] = value
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings_config, f, indent=4)
        except Exception:
            pass

    def apply_theme_stylesheet(self, mode):
        from PyQt6.QtGui import QPalette, QColor
        app_inst = QApplication.instance()
        
        # Completely clear out any previously pinned global stylesheets to allow native components to draw properly
        app_inst.setStyleSheet("")
        
        target_mode = mode
        if mode == "System":
            import winreg
            is_os_dark = False
            try:
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                if value == 0:
                    is_os_dark = True
            except Exception:
                pass
            target_mode = "Dark" if is_os_dark else "Light"

        # Force the cross-platform Fusion style engine universally so QPalette rules are strictly followed in all modes
        from PyQt6.QtWidgets import QStyleFactory
        app_inst.setStyle(QStyleFactory.create("Fusion"))

        palette = QPalette()
        
        if target_mode == "Dark":
            # Canvas Surfacing Layouts
            palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#2d2d2d"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#252526"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#333333"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#aaaaaa"))
            
            # Interactive Core States
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#007acc"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            
            # Gray-out / Disabled State Map
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#666666"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor("#1e1e1e"))
        else:
            # Explicit Light high-contrast color slots to guarantee readability over an OS Dark setting
            palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#fcfcfc"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#e1e1e1"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#777777"))
            
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d7"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#a0a0a0"))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor("#e1e1e1"))

        app_inst.setPalette(palette)

    def toggle_digits_visibility(self, current_text):
        is_anime = self.profile_types.get(current_text, "Western") == "Anime"
        self.digits_label.setVisible(is_anime)
        self.digits_spinbox.setVisible(is_anime)
        
        # Keep image widgets visible only for Anime profiles
        self.img_download_checkbox.setVisible(is_anime)
        self.img_choose_btn.setVisible(is_anime)
        
        # Synchronize the Absolute Numbering container visibility state
        self.abs_container.setVisible(is_anime)

    def toggle_img_button_state(self, state):
        self.img_choose_btn.setEnabled(self.img_download_checkbox.isChecked())

    def open_image_picker_dialog(self):
        self.statusBar().showMessage("Image picker selection dialog window requested.")

    def apply_user_filters(self, title_text):
        import re
        # Fetch active user rules from settings_config (with master toggle override check)
        is_all = self.settings_config.get('enable_all', True)
        cfg_part = is_all or self.settings_config.get('remove_part', True)
        cfg_slash = is_all or self.settings_config.get('convert_slash', True)
        cfg_fw = is_all or self.settings_config.get('fullwidth_chars', True)
        cfg_strip = is_all or self.settings_config.get('remove_illegal', True)
        cfg_lower = is_all or self.settings_config.get('lowercase', True)

        # 1. Clean out "Part" string labels when followed by an integer index, remove trailing commas before numbers, and remove parentheses around standalone numbers
        if cfg_part:
            # Handle ", Part 1" -> " 1" or ", part 2" -> " 2"
            title_text = re.sub(r',\s*part\s+(\d+)\b', r' \1', title_text, flags=re.IGNORECASE)
            # Handle standard remaining "part 1" labels
            title_text = re.sub(r'\bpart\s+(\d+)\b', r'\1', title_text, flags=re.IGNORECASE)
            # Handle ", 1" -> " 1" trailing numbers preceding a comma
            title_text = re.sub(r',\s*(\d+)\b', r' \1', title_text)
            # Remove parentheses around standalone numbers
            title_text = re.sub(r'\s*\((\d+)\)', r' \1', title_text)
            # Clean up any accidental double spaces introduced by the substitutions
            title_text = re.sub(r'\s+', ' ', title_text).strip()

        # 2. Swap standard slashes for the safe division variant
        if cfg_slash:
            title_text = title_text.replace('/', '∕')

        # 3. Handle shell-safe full-width punctuation transformations
        if cfg_fw:
            title_text = title_text.replace('?', '？').replace(';', '；')

        # 4. Strip out remaining unsafe character entities for Windows paths
        if cfg_strip:
            strip_chars = r'[\\:*\"<>|]' if cfg_fw else r'[\\:*\"<>|?;]'
            title_text = re.sub(strip_chars, '', title_text)

        # 5. Handle global casing preferences
        if cfg_lower:
            title_text = title_text.lower()

        return title_text

    def save_profile_config_directly(self, value):
        import json
        self.settings_config['profile'] = value
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings_config, f, indent=4)
        except Exception:
            pass

    def save_absolute_config_directly(self):
        import json
        self.settings_config['use_absolute'] = self.abs_checkbox.isChecked()
        self.settings_config['abs_start_num'] = self.abs_start_spinbox.value()
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings_config, f, indent=4)
        except Exception:
            pass
            
    def closeEvent(self, event):
        import json
        # Save maximized status trace
        self.settings_config['window_maximized'] = self.isMaximized()
        
        # Only preserve normal bounds coordinates if window isn't currently maximized
        if not self.isMaximized():
            geom = self.geometry()
            self.settings_config['window_x'] = geom.x()
            self.settings_config['window_y'] = geom.y()
            self.settings_config['window_w'] = geom.width()
            self.settings_config['window_h'] = geom.height()

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings_config, f, indent=4)
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EpListCleanUI()
    window.show()
    sys.exit(app.exec())