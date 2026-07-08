# ==============================================================================
# SCRIPT: NetSkrabb.py
# VERSION: 2026.07.08__09.13.08
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
APP_VERSION = "2026.07.08__09.13.08"

class FilterDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filters")
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

        # 2. Pipeline Ordered Checkboxes (Synchronized with the contextual order of operations flow)
        self.chk_remove_part = QCheckBox("Enable Part/Volume/Chapter Marker Stripping Pass")
        self.chk_convert_roman = QCheckBox("Enable Contextual Roman Numeral to Arabic Conversion")
        self.chk_remove_time = QCheckBox("Enable Running Time Duration Eraser Pass")
        self.chk_convert_slash = QCheckBox("Convert Forward Slash to Division Slash (∕)")
        self.chk_fullwidth_chars = QCheckBox("Use Legal Full-width Variants (？ and ；)")
        self.chk_remove_illegal = QCheckBox("Remove Remaining Windows Illegal Characters")
        self.chk_lowercase = QCheckBox("Lowercase Mode")

        # Helper function to generate clean description labels for examples
        def make_example_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #888888; margin-left: 20px; font-size: 11px;")
            return lbl

        lbl_part_ex = make_example_label("Example: \"Part Two\" or \"(Part 1 & 2)\" becomes \"2\" or \"1 & 2\"")
        lbl_roman_ex = make_example_label("Example: Converts \"Chapter II\" ➜ \"2\" (Standalone numerals skipped.)")
        lbl_time_ex = make_example_label("Example: \"Movie Title (120 min)\" becomes \"Movie Title\"")
        lbl_slash_ex = make_example_label("Example: Allows \"/\" to display visually as \"∕\" without breaking folder trees")
        lbl_fw_ex = make_example_label("Example: Converts standard \"?\" and \";\" to safe \"？\" and \"；\" for shells like PowerShell")
        lbl_illegal_ex = make_example_label("Example: Strips raw \\ / : * ? \" < > | characters, and removes the standard legal ;")
        lbl_lower_ex = make_example_label("Example: Forces all final text output characters into lowercase format")

        # Grouping sub-checkboxes for easy macro loop operations
        self.sub_checkboxes = [
            self.chk_remove_part,
            self.chk_convert_roman,
            self.chk_remove_time,
            self.chk_convert_slash,
            self.chk_fullwidth_chars,
            self.chk_remove_illegal,
            self.chk_lowercase
        ]

        # Grouping labels to match up with the disable/enable interlocking toggles
        self.example_labels = [lbl_part_ex, lbl_roman_ex, lbl_time_ex, lbl_slash_ex, lbl_fw_ex, lbl_illegal_ex, lbl_lower_ex]

        # Alternating layouts step-by-step down the display widget stack
        layout.addWidget(self.chk_remove_part)
        layout.addWidget(lbl_part_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_convert_roman)
        layout.addWidget(lbl_roman_ex)
        layout.addSpacing(4)
        
        layout.addWidget(self.chk_remove_time)
        layout.addWidget(lbl_time_ex)
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
        self.chk_remove_time.setChecked(settings.get('remove_time', True))
        self.chk_convert_roman.setChecked(settings.get('convert_roman', True))
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
            if checked:
                chk.setChecked(True)
            else:
                # If master is unchecked, turn off all filters except the Windows safe file name filter
                if chk == self.chk_remove_illegal:
                    chk.setChecked(True)
                else:
                    chk.setChecked(False)
        for lbl in self.example_labels:
            lbl.setDisabled(checked)

    def get_settings(self):
        return {
            'enable_all': self.chk_enable_all.isChecked(),
            'remove_part': self.chk_remove_part.isChecked(),
            'remove_time': self.chk_remove_time.isChecked(),
            'convert_roman': self.chk_convert_roman.isChecked(),
            'convert_slash': self.chk_convert_slash.isChecked(),
            'fullwidth_chars': self.chk_fullwidth_chars.isChecked(),
            'remove_illegal': self.chk_remove_illegal.isChecked(),
            'lowercase': self.chk_lowercase.isChecked()
        }

class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.resize(300, 150)
        
        layout = QVBoxLayout(self)
        
        self.clear_history_btn = QPushButton("Clear URL History")
        layout.addWidget(self.clear_history_btn)
        
        layout.addStretch()
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        


class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        """
        results: List of dictionaries containing:
                 {'title': '...', 'url': '...', 'extra': '... (e.g. Year/Type)'}
        """
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setModal(True)
        self.resize(550, 400)
        self.selected_url = None
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        label = QLabel("Select a result to load its episode data:")
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)
        
        # Plain text display area using a layout containing clean rows
        from PyQt6.QtWidgets import QScrollArea, QFrame
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        if not results:
            no_res = QLabel("No results found.")
            no_res.setStyleSheet("color: #888888; font-style: italic;")
            container_layout.addWidget(no_res)
        else:
            for item in results:
                row_layout = QHBoxLayout()
                row_layout.setSpacing(10)
                # Left, Top, Right, Bottom margins for the interactive rows. 
                # Setting right margin to 10 matching the spacing between buttons.
                row_layout.setContentsMargins(0, 0, 10, 0)
                
                # Format text: Title + Extra Info (Year/Type/etc.)
                info_text = item['title']
                if item.get('extra'):
                    info_text += f" ({item['extra']})"
                
                txt_label = QLabel(info_text)
                txt_label.setWordWrap(True)
                row_layout.addWidget(txt_label, 1)
                
                # Web Browser Link
                browser_btn = QPushButton("🌐 Open")
                browser_btn.setFixedWidth(65)
                browser_btn.setToolTip("View page in external browser")
                from PyQt6.QtGui import QDesktopServices
                from PyQt6.QtCore import QUrl
                browser_btn.clicked.connect(lambda checked, url=item['url']: QDesktopServices.openUrl(QUrl(url)))
                row_layout.addWidget(browser_btn)
                
                # Select Button
                select_btn = QPushButton("Select")
                select_btn.setFixedWidth(75)
                select_btn.setStyleSheet("font-weight: bold;")
                select_btn.clicked.connect(lambda checked, url=item['url']: self.accept_selection(url))
                row_layout.addWidget(select_btn)
                
                container_layout.addLayout(row_layout)
                
                # Minimal clean text divider line
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setStyleSheet("color: #444444;")
                container_layout.addWidget(line)
                
        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Close cancel dialog row
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept_selection(self, url):
        self.selected_url = url
        self.accept()

class EpListCleanUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"NetSkrabb v{APP_VERSION}")
        import json
        import os

        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NetSkrabb.config.json")
        
        # Baseline fallback defaults
        default_settings = {
            'enable_all': True,
            'remove_part': False,
            'remove_time': False,
            'convert_roman': False,
            'convert_slash': False,
            'fullwidth_chars': False,
            'remove_illegal': True,
            'lowercase': False,
            'min_digits': 2,
            'theme': 'System',
            'profile': 'MyAnimeList.net',
            'url_history': []
        }

        # Try to load existing configuration, otherwise use defaults
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.app_config = json.load(f)
            except Exception:
                self.app_config = default_settings
        else:
            self.app_config = default_settings

        # Manage Window Sizing and Coordinates Geometry
        default_width = 700
        default_height = 600

        if 'window_x' in self.app_config and 'window_y' in self.app_config:
            # Restore saved size and desktop space coordinates
            self.setGeometry(
                self.app_config['window_x'],
                self.app_config['window_y'],
                self.app_config.get('window_w', default_width),
                self.app_config.get('window_h', default_height)
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
        if self.app_config.get('window_maximized', False):
            self.showMaximized()
        
        # Apply the configured theme engine stylesheet rules on launch
        self.apply_theme_stylesheet(self.app_config.get('theme', 'System'))

        self.init_ui()

        # Populate history list from configuration storage array safely
        history_list = self.app_config.get('url_history', [])
        self.url_input.clear()
        self.url_input.addItems(history_list)
        if history_list:
            self.url_input.setCurrentText(history_list[0])
        else:
            self.url_input.setCurrentText("")

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
        self.url_input = QComboBox()
        self.url_input.setEditable(True)
        self.url_input.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.url_input.lineEdit().setPlaceholderText("Paste webpage URL here...")
        from PyQt6.QtWidgets import QSizePolicy
        self.url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.fetch_btn = QPushButton("Fetch Text")
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.fetch_btn)
        main_layout.addLayout(url_layout)

        # Connect enter key press in URL field to fetch functionality
        self.url_input.lineEdit().returnPressed.connect(self.placeholder_fetch)

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
        self.digits_spinbox.setValue(self.app_config.get('min_digits', 2))
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
        saved_profile = self.app_config.get('profile', 'MyAnimeList.net')
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
        self.abs_checkbox.setChecked(self.app_config.get('use_absolute', False))
        
        self.abs_start_label = QLabel("Start Number:")
        self.abs_start_spinbox = QSpinBox()
        self.abs_start_spinbox.setRange(1, 9999)
        self.abs_start_spinbox.setValue(self.app_config.get('abs_start_num', 1))
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

        # Redundant returnPressed connection removed to prevent double-fetching execution loops

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
        filters_action = QAction("&Filters", self)
        filters_action.setStatusTip("Configure global string filter pipelines")
        filters_action.triggered.connect(self.open_filters_dialog)
        tools_menu.addAction(filters_action)
        
        prefs_action = QAction("&Preferences", self)
        prefs_action.setStatusTip("Configure application preferences")
        prefs_action.triggered.connect(self.open_preferences_dialog)
        tools_menu.addAction(prefs_action)
        
        # Theme Sub-Menu
        theme_menu = tools_menu.addMenu("&Theme")
        
        from PyQt6.QtGui import QActionGroup
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)
        
        current_theme = self.app_config.get('theme', 'System')
        
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
        
        url = self.url_input.currentText().strip()
        if not url:
            self.statusBar().showMessage("Please provide a URL to fetch.")
            return

        selected_profile = self.profile_dropdown.currentText()
        
        # Check if the input is a search query rather than a direct URL
        is_search_query = not (url.startswith("http://") or url.startswith("https://"))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
        }

        if is_search_query:
            if selected_profile == "MyAnimeList.net":
                self.statusBar().showMessage(f"Searching MyAnimeList for: {url}...")
                QApplication.processEvents()
                try:
                    import urllib.parse
                    query_encoded = urllib.parse.quote(url)
                    # Swapping to your provided high-level search route
                    search_url = f"https://myanimelist.net/search/all?q={query_encoded}"
                    
                    req_search = urllib.request.Request(search_url, headers=headers)
                    with urllib.request.urlopen(req_search, timeout=10) as resp:
                        search_html = resp.read().decode('utf-8', errors='ignore')
                    
                    # Isolate the Anime search results container block
                    anime_section = search_html
                    if '<h2 id="anime">' in search_html:
                        anime_section = search_html.split('<h2 id="anime">')[1]
                        if '<h2 id=' in anime_section:
                            anime_section = anime_section.split('<h2 id=')[0]

                    # Multi-line insensitive scan to catch all valid anime reference links
                    search_pattern = r'href="(https://myanimelist\.net/anime/(\d+)/[^"]*)"[^>]*>([\s\S]*?)</a>'
                    matches = re.findall(search_pattern, anime_section)
                    
                    results = []
                    seen_urls = set()
                    for full_url, anime_id, raw_title in matches:
                        # Omit video previews or empty tracking strings
                        if "/video" in full_url:
                            continue
                            
                        import html
                        clean_title = re.sub(r'<[^>]+>', '', raw_title)
                        clean_title = html.unescape(clean_title).strip()
                        
                        # Filter out decorative text elements or empty links to keep results clean
                        if not clean_title or clean_title.lower() in ["add", "cmpl", "add to list", "modify", "edit"]:
                            continue
                            
                        if full_url not in seen_urls:
                            seen_urls.add(full_url)
                            
                            # Grab contextual info from the neighboring string chunk
                            chunk = anime_section.split(full_url)[-1][:800]
                            info_match = re.search(r'href="https://myanimelist\.net/topanime\.php\?type=[^>]*>([^<]+)</a>\s*(?:\(([^)]+)\))?', chunk)
                            if info_match:
                                show_type = info_match.group(1).strip()
                                ep_count = f" ({info_match.group(2).strip()})" if info_match.group(2) else ""
                                extra_info = f"{show_type}{ep_count}"
                            else:
                                extra_info = "Anime"
                                
                            results.append({'title': clean_title, 'url': full_url, 'extra': extra_info})
                    
                    # Launch the text-only selection modal window
                    dialog = SearchResultDialog(results[:15], self)
                    if dialog.exec() and dialog.selected_url:
                        url = dialog.selected_url
                        self.url_input.setCurrentText(url)
                    else:
                        self.statusBar().showMessage("Search canceled.")
                        return
                except Exception as e:
                    self.statusBar().showMessage(f"Search failed: {str(e)}")
                    return
            else:
                self.statusBar().showMessage(f"Search queries not yet configured for {selected_profile}.")
                return

        # Global UI update to show progress immediately for all profiles
        self.statusBar().showMessage(f"Fetching data from {selected_profile}...")
        QApplication.processEvents()

        # Persist URL to history
        if url not in self.app_config.get('url_history', []):
            self.app_config['url_history'] = [url] + self.app_config.get('url_history', [])[:9]
            import json
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.app_config, f, indent=4)
            except Exception:
                pass

        # Automatically redirect main series entries to their respective episode sub-pages
        if selected_profile == "MyAnimeList.net" and url:
            # Check if it's a main title URL but doesn't already end with /episode or /episode/
            if "/anime/" in url and not re.search(r'/episode(?:/\d+)?/?$', url):
                # Clean up any trailing query parameters or trailing slashes first
                base_url = url.split('?')[0].rstrip('/')
                url = f"{base_url}/episode"
        
        elif selected_profile == "Wikipedia.org" and url:
            # If it's a main series page, resolve it to the standard "List of... episodes" directory first
            if "wikipedia.org/wiki/" in url.lower() and "list_of_" not in url.lower() and "_episodes" not in url.lower():
                self.statusBar().showMessage("Main series page detected. Locating episode list link...")
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=5) as response:
                        html_text = response.read().decode('utf-8', errors='ignore')
                    
                    list_match = re.search(r'href="(?://en\.wikipedia\.org)?(/wiki/List_of_[^"]+_episodes[^"]*)"', html_text, re.IGNORECASE)
                    if list_match:
                        url = f"https://en.wikipedia.org{list_match.group(1)}"
                        self.url_input.setText(url)
                except urllib.error.HTTPError as e:
                    self.input_text.setPlainText(f"[HTTP ERROR {e.code}]: Failed reaching main page resolve.\nURL: {url}\nReason: {e.reason}")
                    self.statusBar().showMessage(f"HTTP Error: {e.code}")
                    return
                except Exception as e:
                    import traceback
                    self.input_text.setPlainText(f"[ERROR]:\n{str(e)}\n\n{traceback.format_exc()}")
                    pass

            # Detect nested sub-page links from an episode directory list page
            if "list_of_" in url.lower():
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=5) as response:
                        html_text = response.read().decode('utf-8', errors='ignore')
                    
                    # Capture sequential season breakdowns like "List_of_The_Simpsons_episodes_(seasons_1–20)"
                    split_links = re.findall(r'href="(?://en\.wikipedia\.org)?(/wiki/List_of_[^"]+_episodes_\([^)]+\))"', html_text, re.IGNORECASE)
                    if split_links:
                        seen = set()
                        unique_splits = []
                        import urllib.parse
                        for link in split_links:
                            # Strip off any stray domain names accidentally captured by match variants
                            path_only = link.replace('https://en.wikipedia.org', '').replace('http://en.wikipedia.org', '')
                            # Ensure the partial path always starts with a leading slash
                            if not path_only.startswith('/'):
                                path_only = '/' + path_only
                            
                            # Clean and preserve structural entities like colons, parentheses, and slashes
                            encoded_path = urllib.parse.quote(path_only, safe='/:()–')
                            full_link = f"https://en.wikipedia.org{encoded_path}"
                            if full_link not in seen:
                                seen.add(full_link)
                                unique_splits.append(full_link)
                        
                        self._wikipedia_sub_urls = unique_splits
                    else:
                        self._wikipedia_sub_urls = [url]
                except Exception:
                    self._wikipedia_sub_urls = [url]
            else:
                self._wikipedia_sub_urls = [url]
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

        if selected_profile == "Wikipedia.org":
            self.statusBar().showMessage("Fetching data from Wikipedia.org...")
            try:
                import urllib.request
                from bs4 import BeautifulSoup
                import html

                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_text = response.read().decode('utf-8', errors='ignore')

                soup = BeautifulSoup(html_text, 'html.parser')
                episodes_found = []

                episodes_found = []
                target_urls = getattr(self, '_wikipedia_sub_urls', [url])
                
                # Clear temporary tracking property after pulling it
                if hasattr(self, '_wikipedia_sub_urls'):
                    delattr(self, '_wikipedia_sub_urls')

                import urllib.parse
                for target_url in target_urls:
                    # Use the URL directly to prevent destructive double-encoding of special characters
                    safe_target_url = target_url

                    req = urllib.request.Request(safe_target_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        html_text = response.read().decode('utf-8', errors='ignore')

                    # Normalize HTML line breaks to a single space to avoid smushing adjacent text strings
                    html_text = re.sub(r'<br\s*/?>', ' ', html_text, flags=re.IGNORECASE)

                    # Ensure standard padding around structural text blocks like small tags or closed anchors to prevent words running together
                    html_text = re.sub(r'<\/?(?:small|a|b|i|span)[^>]*>', ' ', html_text, flags=re.IGNORECASE)

                    soup = BeautifulSoup(html_text, 'html.parser')

                    # Find all tables on the page (supports main series page tables and "List of..." tables)
                    tables = soup.find_all('table', class_=lambda c: c and ('wikitable' in c or 'episode_list' in c))
                    
                    if not tables:
                        tables = soup.find_all('table')

                    for table in tables:
                        # Look for standard headers to make sure it's a table with titles
                        headers_text = [th.get_text(strip=True).lower() for th in table.find_all('th')]
                        if not any('title' in h or 'episode' in h for h in headers_text):
                            pass

                        # Check if there is a heading preceding this table indicating the season
                        current_season = 1
                        prev_element = table.find_previous(['h2', 'h3', 'span'])
                        while prev_element:
                            heading_text = prev_element.get_text(strip=True)
                            season_match = re.search(r'(?:Season|Series)\s+(\d+)', heading_text, re.IGNORECASE)
                            if season_match:
                                current_season = int(season_match.group(1))
                                break
                            prev_element = prev_element.find_previous(['h2', 'h3', 'span'])

                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all(['td', 'th'])
                            if not cells:
                                continue

                            row_data = []
                            for cell in cells:
                                txt = cell.get_text(strip=True)
                                txt = re.sub(r'\[\d+\]', '', txt)
                                row_data.append(txt)

                            # Purge Wikipedia reference citation links from the title cell completely
                            if row.find('td', class_='summary'):
                                title_td = row.find('td', class_='summary')
                                for sup in title_td.find_all('sup', class_=lambda c: c and ('reference' in c or 'mw-ref' in c)):
                                    sup.decompose()
                                for sup in title_td.find_all('sup'):
                                    sup.decompose()
                                ep_title = title_td.get_text(strip=True)
                            else:
                                ep_title = None
                                for cell in cells:
                                    # Copy the cell to perform test stripping without altering the source layout array
                                    from bs4 import BeautifulSoup
                                    test_cell = BeautifulSoup(str(cell), 'html.parser')
                                    for sup in test_cell.find_all('sup'):
                                        sup.decompose()
                                    rd = test_cell.get_text(strip=True)
                                    if (rd.startswith('"') and rd.endswith('"')) or (rd.startswith('“') and rd.endswith('”')):
                                        ep_title = rd
                                        break

                            if ep_title:
                                if (ep_title.startswith('"') and ep_title.endswith('"')) or (ep_title.startswith('“') and ep_title.endswith('”')):
                                    ep_title = ep_title[1:-1].strip()

                                # Wikipedia tables typically have two numeric columns early on
                                digits = [rd for rd in row_data if rd.isdigit()]
                                
                                ep_num = int(digits[0]) if digits else 1
                                if len(digits) >= 2:
                                    ep_num = int(digits[1])

                                if ep_title and not ep_title.isdigit():
                                    episodes_found.append(f"1. {current_season}-{ep_num} 00 AAA 00 {ep_title}")

                if episodes_found:
                    self.input_text.setPlainText('\n'.join(episodes_found))
                    self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} titles from Wikipedia.")
                else:
                    self.input_text.setPlainText("No valid episode titles could be identified from the Wikipedia tables.")
                    self.statusBar().showMessage("Fetch complete, but no matching table columns found.")
                return
            except Exception as e:
                self.statusBar().showMessage(f"Error fetching from Wikipedia: {str(e)}")
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
                for line in raw_text.splitlines():
                    line_str = line.strip()
                    match = re.match(r'^\d+\.\s+(\d+)-(\d+)\s+\d{2}\s+[A-Za-z]{3}\s+\d{2}\s+(.+)$', line_str)
                    if match:
                        cleaned_episodes.append(
                            format_western_episode(int(match.group(1)), int(match.group(2)), match.group(3))
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

    def load_source_file(self):
        import os
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Source Text File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.statusBar().showMessage("Loading and processing source data...")
            QApplication.processEvents()
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.input_text.setPlainText(content)
                self.statusBar().showMessage(f"Successfully loaded file: {os.path.basename(file_path)}")
            except Exception as e:
                self.statusBar().showMessage(f"Failed to load file: {str(e)}")

    # Redundant load_wiki_url_data removed to prevent double-fetching execution loops

    def open_filters_dialog(self):
        dialog = FilterDialog(self.app_config, self)
        if dialog.exec():
            import json
            self.app_config = dialog.get_settings()
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.app_config, f, indent=4)
                self.statusBar().showMessage("Filters successfully saved to config file.")
            except Exception as e:
                self.statusBar().showMessage(f"Filters saved in memory, but failed to write to disk: {str(e)}")

    def open_preferences_dialog(self):
        dialog = PreferencesDialog(self)
        dialog.clear_history_btn.clicked.connect(self.clear_url_history)
        dialog.exec()

    def clear_url_history(self):
        self.app_config['url_history'] = []
        self.url_input.clear()
        import json
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
            self.statusBar().showMessage("URL history cleared.")
        except Exception:
            pass

    def open_about_dialog(self):
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtCore import Qt
        
        about_text = (
            f"<b>NetSkrabb v{APP_VERSION}</b><br>"
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
        msg_box.setWindowTitle("About NetSkrabb")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(about_text)
        msg_box.exec()

    def handle_theme_change(self):
        import json
        selected_action = self.theme_group.checkedAction()
        if not selected_action:
            return
            
        theme_mode = selected_action.text()
        self.app_config['theme'] = theme_mode
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
            self.apply_theme_stylesheet(theme_mode)
            self.statusBar().showMessage(f"Theme changed to {theme_mode}")
        except Exception:
            pass

    

    def save_digits_config_directly(self, value):
        import json
        self.app_config['min_digits'] = value
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
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

    def _roman_to_arabic(self, match):
        roman = match.group(0).upper()
        roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value
        return str(total)

    def apply_user_filters(self, title_text):
        import re
        # Fetch active user rules from settings_config (with master toggle override check)
        is_all = self.app_config.get('enable_all', True)
        cfg_part = is_all or self.app_config.get('remove_part', True)
        cfg_time = is_all or self.app_config.get('remove_time', True)
        cfg_roman = is_all or self.app_config.get('convert_roman', True)
        cfg_slash = is_all or self.app_config.get('convert_slash', True)
        cfg_fw = is_all or self.app_config.get('fullwidth_chars', True)
        cfg_strip = is_all or self.app_config.get('remove_illegal', True)
        cfg_lower = is_all or self.app_config.get('lowercase', True)

        # 1. Combined Contextual Marker Pipeline (Processes numbers only when bound to structural words)
        if cfg_part or cfg_roman:
            def parse_marker_content(match):
                marker = match.group(1)
                content = match.group(2).strip()
                
                # Setup helper translations for written numbers
                word_to_num = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'}
                
                # Check for written phrase patterns first
                for word, num in word_to_num.items():
                    content = re.sub(r'\b' + word + r'\b', num, content, flags=re.IGNORECASE)
                
                # If Roman numerals toggle is active, find and translate them contextually
                if cfg_roman:
                    roman_pattern = r'\b(?=[MDCLXVI]+\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})\b'
                    content = re.sub(roman_pattern, self._roman_to_arabic, content, flags=re.IGNORECASE)
                
                # If Part stripping toggle is active, return only the transformed content numbers
                if cfg_part:
                    return f" {content}"
                
                # Otherwise, keep the original marker prefix word intact
                return f"{marker} {content}"

            # Step A: Match marker words enclosing joined ampersand segments inside parentheses
            title_text = re.sub(r'\(\s*(parts?|chapters?|chs?\.?|volumes?|vol\.?)\s+([^)]+)\)', parse_marker_content, title_text, flags=re.IGNORECASE)
            
            # Step B: Match sequential markers trailing behind standard text punctuation indicators
            marker_regex = r'\b(parts?|chapters?|chs?\.?|volumes?|vol\.?)\s+([\w\d\s&–\-]+)\b'
            title_text = re.sub(marker_regex, parse_marker_content, title_text, flags=re.IGNORECASE)

            # Step C: General trailing number structural cleanups
            if cfg_part:
                title_text = re.sub(r',\s*(\d+)\b', r' \1', title_text)
                title_text = re.sub(r'\s*\((\d+)\)', r' \1', title_text)
                title_text = re.sub(r',\s*(\d+\s*&\s*\d+)', r' \1', title_text)
                
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

        # Final Cleanup Crew: Collapse any multi-space clusters down to a single clean space
        title_text = re.sub(r'\s+', ' ', title_text).strip()

        return title_text

    def save_profile_config_directly(self, value):
        import json
        self.app_config['profile'] = value
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
        except Exception:
            pass

    def save_absolute_config_directly(self):
        import json
        self.app_config['use_absolute'] = self.abs_checkbox.isChecked()
        self.app_config['abs_start_num'] = self.abs_start_spinbox.value()
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
        except Exception:
            pass
            
    def closeEvent(self, event):
        import json
        # Save maximized status trace
        self.app_config['window_maximized'] = self.isMaximized()
        
        # Only preserve normal bounds coordinates if window isn't currently maximized
        if not self.isMaximized():
            geom = self.geometry()
            self.app_config['window_x'] = geom.x()
            self.app_config['window_y'] = geom.y()
            self.app_config['window_w'] = geom.width()
            self.app_config['window_h'] = geom.height()

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, indent=4)
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EpListCleanUI()
    window.show()
    sys.exit(app.exec())