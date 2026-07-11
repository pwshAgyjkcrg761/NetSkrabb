# ==============================================================================
# SCRIPT: NetSkrabb.py
# VERSION: 2026.07.11__06.32.12
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
import os
import ctypes
import json
import urllib.request
from PyQt6.QtWidgets import (QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QPlainTextEdit, QMenuBar, QStatusBar)
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QComboBox, QDialog, QCheckBox, QDialogButtonBox, QFrame

# Easily maintainable application metadata configuration
APP_VERSION = "2026.07.11__06.32.12"

class NetSkrabb(QMainWindow):
    # Consolidated headers for consistent browser fingerprinting
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1'
    }

    @staticmethod
    def get_dynamic_headers(url):
        """Returns a copy of HEADERS with a Referer matched to the target domain."""
        headers = NetSkrabb.HEADERS.copy()
        low_url = url.lower()
        
        if "myanimelist.net" in low_url:
            headers['Referer'] = "https://myanimelist.net/"
        elif "wikipedia.org" in low_url:
            headers['Referer'] = "https://www.wikipedia.org/"
        elif "epguides.com" in low_url:
            headers['Referer'] = "https://epguides.com/"
        elif "theposterdb.com" in low_url:
            headers['Referer'] = "https://theposterdb.com/"
        elif "duckduckgo.com" in low_url:
            headers['Referer'] = "https://duckduckgo.com/"
            
        return headers

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
        self.chk_remove_illegal.setStyleSheet("QCheckBox { color: #ff4444; } QCheckBox:disabled { color: #888888; }")
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
        lbl_illegal_ex = make_example_label("Example: Strips raw \\ / : * ? \" < > | characters, and removes the standard legal ;\n* Note: This filter is critical for generating valid Windows file system names.")
        lbl_illegal_ex.setStyleSheet("color: #ff4444; margin-left: 20px; font-size: 11px;")
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

        self.clear_cache_btn = QPushButton("Clear Image Cache")
        layout.addWidget(self.clear_cache_btn)

        self.chk_convert_jpg = QCheckBox("Convert Images to JPG (Enabled by default)")
        self.chk_convert_jpg.setChecked(parent.app_config.get('convert_to_jpg', True))
        self.chk_convert_jpg.toggled.connect(lambda checked: parent.update_config_key('convert_to_jpg', checked))
        layout.addWidget(self.chk_convert_jpg)
        
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
        container_layout.setContentsMargins(0, 0, 8, 0)
        
        if not results:
            no_res = QLabel("No results found.")
            no_res.setStyleSheet("color: #888888; font-style: italic;")
            container_layout.addWidget(no_res)
        else:
            for item in results:
                row_layout = QHBoxLayout()
                # Increase row padding and vertical breathing room
                row_layout.setContentsMargins(0, 8, 0, 8)
                row_layout.setSpacing(12)
                
                # Format text: Title + Extra Info (Year/Type/etc.)
                info_text = item['title']
                if item.get('extra'):
                    info_text += f" ({item['extra']})"
                
                txt_label = QLabel(info_text)
                txt_label.setWordWrap(True)
                txt_label.setStyleSheet("font-size: 13px; font-weight: 500;")
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

class ImagePickerDialog(QDialog):
    def __init__(self, image_urls, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Cover Image")
        self.setModal(True)
        self.resize(800, 600)
        self.selected_urls = []
        self.last_selected_index = None
        self.image_urls = image_urls
        self.image_buttons = [] # Initialize here to ensure attribute exists for loader
        
        layout = QVBoxLayout(self)
        from PyQt6.QtWidgets import QScrollArea, QGridLayout
        from PyQt6.QtCore import Qt, QTimer
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(10)
        
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Select Cover")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # Horizontal layout for metadata info and buttons
        bottom_layout = QHBoxLayout()
        self.info_label = QLabel("Select an image to see large version details...")
        self.info_label.setStyleSheet("color: #888888; font-style: italic;")
        bottom_layout.addWidget(self.info_label, 1)
        bottom_layout.addWidget(self.button_box)
        layout.addLayout(bottom_layout)

        # Trigger the image loader only after the dialog window is fully visible
        QTimer.singleShot(100, self.load_images_sequentially)

    def load_images_sequentially(self):
        from PyQt6.QtGui import QPixmap, QIcon
        from PyQt6.QtCore import Qt
        import urllib.request
        
        row, col = 0, 0
        is_dev = any(arg in sys.argv for arg in ["-DevDebug", "-Dev", "-DBG"])
        if is_dev: print(f"[DevDebug] Picker starting load for {len(self.image_urls)} URLs.")
        for url in self.image_urls:
            # Check if this icon is already in the parent's cache
            if url in self.parent().thumbnail_cache:
                # Retrieve icon and tooltip metadata from cache
                cached_icon, cached_tooltip = self.parent().thumbnail_cache[url]
                btn = QPushButton()
                btn.setIcon(cached_icon)
                # Ensure cached icons follow the same 140x200 scaling constraints
                btn.setIconSize(cached_icon.actualSize(QPixmap(140, 200).size()))
                btn.setFixedSize(150, 210)
                btn.setToolTip("Click to select and view metadata")
                btn.setProperty("img_url", url)
                btn.setProperty("tpdb_id", self.parent().tpdb_id_map.get(url))
                btn.clicked.connect(lambda checked, b=btn: self.handle_selection_ui(b))
                self.image_buttons.append(btn)
                self.grid.addWidget(btn, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
                continue

            if is_dev: print(f"[DevDebug] Trying to load: {url}")
            try:
                if url.endswith('/view'):
                    p_id = url.split('/')[-2]
                    cache_fn = f"{p_id}_view.jpg"
                else:
                    cache_fn = url.split('/')[-1].split('?')[0]
                cache_path = os.path.join(self.parent().cache_dir, cache_fn)
                
                if os.path.exists(cache_path):
                    if is_dev: print(f"[DevDebug] Loading thumb from cache: {cache_fn}")
                    with open(cache_path, 'rb') as f:
                        data = f.read()
                else:
                    if is_dev: print(f"[DevDebug] Downloading thumb: {url}")
                    req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
                    with urllib.request.urlopen(req, timeout=5) as response:
                        data = response.read()
                    with open(cache_path, 'wb') as f:
                        f.write(data)
                
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    btn = QPushButton()
                    # Wrap the pixmap in a QIcon to satisfy PyQt6 requirement
                    icon = QIcon(pixmap)
                    btn.setIcon(icon)
                    btn.setIconSize(pixmap.size().scaled(140, 200, Qt.AspectRatioMode.KeepAspectRatio))
                    btn.setFixedSize(150, 210)
                    btn.setToolTip("Click to select and view metadata")
                    btn.setProperty("img_url", url)
                    btn.setProperty("tpdb_id", self.parent().tpdb_id_map.get(url))
                    btn.clicked.connect(lambda checked, b=btn: self.handle_selection_ui(b))
                    self.image_buttons.append(btn)
                    
                    # Store icon and tooltip metadata in persistent cache
                    self.parent().thumbnail_cache[url] = (icon, btn.toolTip())
                    
                    self.grid.addWidget(btn, row, col)
                    col += 1
                    if col > 3:
                        col = 0
                        row += 1
                
                QApplication.processEvents()
            except Exception as e:
                if is_dev: print(f"[DevDebug] Error loading {url}: {e}")
                continue

    def handle_selection_ui(self, clicked_btn):
        from PyQt6.QtWidgets import QDialogButtonBox
        from PyQt6.QtGui import QPixmap
        import urllib.request
        import os

        from PyQt6.QtCore import Qt
        modifiers = QApplication.keyboardModifiers()
        curr_idx = self.image_buttons.index(clicked_btn)

        # 1. Determine Selection Set based on keyboard modifiers
        if modifiers == Qt.KeyboardModifier.ShiftModifier and self.last_selected_index is not None:
            start = min(self.last_selected_index, curr_idx)
            end = max(self.last_selected_index, curr_idx)
            # Add range to current selection
            new_urls = [self.image_buttons[i].property("img_url") for i in range(start, end + 1)]
            for url in new_urls:
                if url not in self.selected_urls: self.selected_urls.append(url)
        elif modifiers == Qt.KeyboardModifier.ControlModifier:
            url = clicked_btn.property("img_url")
            if url in self.selected_urls:
                self.selected_urls.remove(url)
            else:
                self.selected_urls.append(url)
        else:
            # Single select
            self.selected_urls = [clicked_btn.property("img_url")]

        self.last_selected_index = curr_idx

        # 2. Visual highlighting & State Update
        from PyQt6.QtGui import QPixmap
        import urllib.request
        import os

        # 2. Visual highlighting
        for btn in self.image_buttons:
            if btn.property("img_url") in self.selected_urls:
                btn.setStyleSheet("border: 3px solid #007acc; border-radius: 5px; padding: 2px;")
            else:
                btn.setStyleSheet("border: none; padding: 2px;")

        # 3. Status and Metadata Update
        count = len(self.selected_urls)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(count > 0)

        if count == 1:
            target_url = self.selected_urls[0]
            tpdb_id = clicked_btn.property("tpdb_id") # Use the clicked button's context
            
            # Metadata upgrade logic for single selection
            if tpdb_id:
                target_url = f"https://theposterdb.com/api/assets/{tpdb_id}/view"
            elif "cdn.myanimelist.net" in target_url:
                base, ext = os.path.splitext(target_url)
                if not base.endswith('l'): target_url = f"{base}l{ext}"
            
            self.info_label.setText("Checking high-res details...")
            self.info_label.setStyleSheet("color: #007acc; font-style: italic;")
            QApplication.processEvents()

            if target_url.endswith('/view'):
                p_id = target_url.split('/')[-2]
                cache_fn = f"{p_id}_view.jpg"
            else:
                cache_fn = target_url.split('/')[-1].split('?')[0]
            cache_path = os.path.join(self.parent().cache_dir, cache_fn)

            try:
                if os.path.exists(cache_path):
                    with open(cache_path, 'rb') as f: l_data = f.read()
                else:
                    req = urllib.request.Request(target_url, headers=NetSkrabb.get_dynamic_headers(target_url))
                    with urllib.request.urlopen(req, timeout=5) as resp: l_data = resp.read()
                    with open(cache_path, 'wb') as f: f.write(l_data)
                
                pix = QPixmap()
                if pix.loadFromData(l_data):
                    size_kb = len(l_data) / 1024
                    self.info_label.setText(f"Large Version: {pix.width()}x{pix.height()} | {size_kb:.1f} KB")
                    self.info_label.setStyleSheet("color: #28a745; font-weight: bold;")
                else:
                    self.info_label.setText("1 image selected (Metadata error).")
            except Exception:
                self.info_label.setText("1 image selected (Metadata unavailable).")
        else:
            self.info_label.setText(f"Selected: {count} items")
            self.info_label.setStyleSheet("color: #007acc; font-weight: bold;" if count > 0 else "color: #888888;")

class EpListCleanUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"NetSkrabb v{APP_VERSION}")
        
        # Define and create internal directory structure
        script_dir = os.path.dirname(os.path.abspath(__file__))
        internal_dir = os.path.join(script_dir, "NetSkrabb_internal")
        icons_dir = os.path.join(internal_dir, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        self.url_icons_dir = os.path.join(internal_dir, "url_icons_downloaded")
        os.makedirs(self.url_icons_dir, exist_ok=True)
        # Check for and download any missing site-specific icons
        self.sync_site_icons()
        self.cache_dir = os.path.join(internal_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        # Set Window Icon and fix Windows Taskbar grouping
        icon_path = os.path.join(icons_dir, "NetSkrabb-icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            if sys.platform == 'win32':
                try:
                    myappid = 'pwshAgyjkcrg761.netskrabb.main.v1'
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                except Exception:
                    pass
        

        self.config_path = os.path.join(internal_dir, "NetSkrabb.config.json")
        
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
            'url_history': [],
            'convert_to_jpg': True,
            'download_cover_image': False,
            'last_save_path': ''
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

        # Runtime Metadata for Image Handling
        self.scraped_images = []
        self.scraped_title = "Series"
        self.selected_image_url = None
        self.thumbnail_cache = {} # Key: URL, Value: QIcon
        self.tpdb_id_map = {} # Key: Thumb URL, Value: Poster ID

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
        script_dir = os.path.dirname(os.path.abspath(__file__))
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
        # Mars Icon Slot (SVG)
        self.url_icon = QLabel()
        self.url_icon.setFixedSize(20, 20)
        self.url_icon.setScaledContents(True)
        icon_svg_path = os.path.join(script_dir, "NetSkrabb_internal", "icons", "url_icon", "mars-url-icon.svg")
        if os.path.exists(icon_svg_path):
            from PyQt6.QtGui import QPixmap
            self.url_icon.setPixmap(QPixmap(icon_svg_path))
        
        self.url_input = QComboBox()
        self.url_input.setEditable(True)
        self.url_input.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.url_input.lineEdit().setPlaceholderText("Paste webpage URL here...")
        from PyQt6.QtWidgets import QSizePolicy
        self.url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        

        url_layout.addWidget(self.url_icon)
        url_layout.addSpacing(8)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # Connect enter key press in URL field to fetch functionality
        self.url_input.lineEdit().returnPressed.connect(self.trigger_data_load)
        # Enable auto-switching of profiles based on pasted/typed URLs
        self.url_input.editTextChanged.connect(self.auto_detect_profile)

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
        self.img_download_checkbox.setChecked(self.app_config.get('download_cover_image', False))
        self.img_download_checkbox.stateChanged.connect(self.toggle_img_button_state)
        self.image_layout.addWidget(self.img_download_checkbox)
        
        self.img_choose_btn = QPushButton("Choose Cover...", self)
        self.img_choose_btn.setEnabled(self.img_download_checkbox.isChecked())
        self.img_choose_btn.clicked.connect(self.open_image_picker_dialog)
        self.image_layout.addWidget(self.img_choose_btn)
        
        main_layout.addLayout(self.image_layout)

        # Progress bar for batch operations
        from PyQt6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                height: 18px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007acc;
            }
        """)
        main_layout.addWidget(self.progress_bar)

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

        # Monitor text changes to drive Smart Button states
        self.input_text.textChanged.connect(self.update_button_states)
        self.output_text.textChanged.connect(self.update_button_states)

        # 6. Quick Action Row (Clear & Copy)
        copy_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.clicked.connect(self.clear_fields)
        copy_layout.addWidget(self.clear_btn)
        
        copy_layout.addStretch()  # Pushes button to the right side
        self.save_btn = QPushButton("Save Text...")
        self.save_btn.setMinimumWidth(100)
        self.save_btn.clicked.connect(self.save_output_to_file)
        copy_layout.addWidget(self.save_btn)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setMinimumWidth(150)
        copy_layout.addWidget(self.copy_btn)
        
        main_layout.addLayout(copy_layout)

        # 7. Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

        # Redundant returnPressed connection removed to prevent double-fetching execution loops

        # Connect button placeholders to verify layout interaction later
        
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
        manual_action = QAction("&Manual", self)
        manual_action.setStatusTip("Show the user manual and usage guide")
        manual_action.triggered.connect(self.open_manual_dialog)
        
        help_menu.addAction(manual_action)
        help_menu.addAction(about_action)

    def trigger_data_load(self):
        import urllib.request
        import re
        
        url = self.url_input.currentText().strip()
        if not url:
            self.statusBar().showMessage("Please provide a URL or search query.")
            return

        # Reset image metadata for new fetch session
        self.scraped_images = []
        self.scraped_title = "Series"
        self.selected_image_urls = []

        self.add_to_history(url)

        selected_profile = self.profile_dropdown.currentText()
        
        # Handle ThePosterDB specifically for image-only scraping
        if "theposterdb.com" in url.lower():
            if selected_profile == "MyAnimeList.net":
                self.statusBar().showMessage("ThePosterDB URLs are not supported with the MyAnimeList profile.")
                return
            if "/set/" not in url.lower():
                self.statusBar().showMessage("ThePosterDB URLs must be a 'Set' link (contain /set/).")
                return
            self.statusBar().showMessage("Loading posters from ThePosterDB...")
            QApplication.processEvents()
            try:
                import urllib.request
                import re
                req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html_text = resp.read().decode('utf-8', errors='ignore')
                
                # Truncate content to isolate the primary set and exclude unrelated sections
                stop_points = ['"font-weight-bold">More Posters For', '"font-weight-bold">Also Uploaded By', '"font-weight-bold">Additional Set']
                for point in stop_points:
                    idx = html_text.find(point)
                    if idx != -1:
                        html_text = html_text[:idx]

                # Pair all optimized variants within a poster block to their specific Poster ID
                # This isolates each 'hovereffect' block to ensure correct ID association
                poster_blocks = re.findall(r'<div class="hovereffect rounded-poster">([\s\S]+?)data-poster-id=\'(\d+)\'', html_text)
                
                unique_posters = []
                self.tpdb_id_map = {}
                for block_html, p_id in poster_blocks:
                    # Capture all URLs in the srcset for this specific poster
                    variants = re.findall(r'srcset="([^"]+)"', block_html)
                    if variants:
                        # Use the first variant (usually webp) as the thumbnail for the picker
                        primary_thumb = variants[0]
                        if primary_thumb not in unique_posters:
                            unique_posters.append(primary_thumb)
                            # Map every variant to the ID so the picker knows what to upgrade regardless of what it loads
                            for img_url in variants:
                                self.tpdb_id_map[img_url] = p_id
                
                if unique_posters:
                    self.scraped_images = unique_posters
                    self.selected_image_urls = [self.scraped_images[0]]
                    # Attempt to pull a series title from the page metadata
                    title_match = re.search(r'<title>(.*?)</title>', html_text, re.IGNORECASE)
                    if title_match:
                        self.scraped_title = title_match.group(1).split('|')[0].strip()
                    
                    self.statusBar().showMessage(f"Successfully loaded {len(unique_posters)} posters from ThePosterDB.")
                    return 
                else:
                    self.statusBar().showMessage("No valid posters found on that ThePosterDB page.")
                    return
            except Exception as e:
                self.statusBar().showMessage(f"ThePosterDB Error: {str(e)}")
                return
        
        # Check if the input is a search query rather than a direct URL
        is_search_query = not (url.startswith("http://") or url.startswith("https://"))
        
        # Reference the consolidated class-level headers
        headers = NetSkrabb.HEADERS

        if is_search_query:
            if selected_profile == "MyAnimeList.net":
                self.statusBar().showMessage(f"Searching MyAnimeList.net for: {url}...")
                QApplication.processEvents()
                try:
                    import urllib.parse
                    query_encoded = urllib.parse.quote(url)
                    search_url = f"https://myanimelist.net/search/all?q={query_encoded}"
                    
                    req_search = urllib.request.Request(search_url, headers=NetSkrabb.get_dynamic_headers(search_url))
                    with urllib.request.urlopen(req_search, timeout=10) as resp:
                        search_html = resp.read().decode('utf-8', errors='ignore')
                    
                    anime_section = search_html
                    if '<h2 id="anime">' in search_html:
                        anime_section = search_html.split('<h2 id="anime">')[1]
                        if '<h2 id=' in anime_section:
                            anime_section = anime_section.split('<h2 id=')[0]

                    search_pattern = r'href="(https://myanimelist\.net/anime/(\d+)/[^"]*)"[^>]*>([\s\S]*?)</a>'
                    matches = re.findall(search_pattern, anime_section)
                    
                    results = []
                    seen_urls = set()
                    for full_url, anime_id, raw_title in matches:
                        if "/video" in full_url:
                            continue
                            
                        import html
                        clean_title = re.sub(r'<[^>]+>', '', raw_title)
                        clean_title = html.unescape(clean_title).strip()
                        
                        if not clean_title or clean_title.lower() in ["add", "cmpl", "add to list", "modify", "edit"]:
                            continue
                            
                        if full_url not in seen_urls:
                            seen_urls.add(full_url)
                            
                            chunk = anime_section.split(full_url)[-1][:800]
                            info_match = re.search(r'href="https://myanimelist\.net/topanime\.php\?type=[^>]*>([^<]+)</a>\s*(?:\(([^)]+)\))?', chunk)
                            if info_match:
                                show_type = info_match.group(1).strip()
                                ep_count = f" ({info_match.group(2).strip()})" if info_match.group(2) else ""
                                extra_info = f"{show_type}{ep_count}"
                            else:
                                extra_info = "Anime"
                                
                            results.append({'title': clean_title, 'url': full_url, 'extra': extra_info})
                    
                    dialog = SearchResultDialog(results[:15], self)
                    if dialog.exec() and dialog.selected_url:
                        url = dialog.selected_url
                        self.add_to_history(url)
                    else:
                        self.statusBar().showMessage("Search canceled.")
                        return
                except Exception as e:
                    self.statusBar().showMessage(f"Search failed: {str(e)}")
                    return
            elif selected_profile == "epguides.com":
                self.statusBar().showMessage(f"Checking epguides.com direct link for: {url}...")
                QApplication.processEvents()
                import urllib.parse
                import urllib.error
                
                # Check if it's already a full URL
                if url.startswith("http://") or url.startswith("https://"):
                    direct_guess_url = url
                else:
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '', url)
                    direct_guess_url = f"https://epguides.com/{clean_name}/"
                
                try:
                    req_test = urllib.request.Request(direct_guess_url, headers=NetSkrabb.get_dynamic_headers(direct_guess_url))
                    with urllib.request.urlopen(req_test, timeout=7) as resp_test:
                        url = direct_guess_url
                        self.url_input.setCurrentText(url)
                except urllib.error.HTTPError as e:
                    if e.code == 404 and not (url.startswith("http://") or url.startswith("https://")):
                        self.statusBar().showMessage("Direct path hit 404. Performing resilient search...")
                        QApplication.processEvents()
                        try:
                            # Search via the standard layout querying with raw encoded search query string
                            query_encoded = urllib.parse.quote(f"{url} site:epguides.com")
                            ddg_url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
                            
                            req_ddg = urllib.request.Request(ddg_url, headers=NetSkrabb.get_dynamic_headers(ddg_url))
                            with urllib.request.urlopen(req_ddg, timeout=10) as resp_ddg:
                                ddg_html = resp_ddg.read().decode('utf-8', errors='ignore')
                            
                            # Parse any raw hyperlinks referencing epguides.com inside the search body
                            links = re.findall(r'href="([^"]+)"', ddg_html)
                            
                            results = []
                            seen_urls = set()
                            
                            # Scan for anchor blocks containing the link to pull the actual visual title text
                            result_blocks = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', ddg_html, re.IGNORECASE)
                            
                            for link, raw_anchor_text in result_blocks:
                                full_url = link
                                if "duckduckgo.com/l/?" in full_url:
                                    parsed_proxy = urllib.parse.urlparse(full_url)
                                    query_params = urllib.parse.parse_qs(parsed_proxy.query)
                                    if 'uddg' in query_params:
                                        full_url = query_params['uddg'][0]
                                
                                if "epguides.com" in full_url:
                                    path_parts = [p for p in urllib.parse.urlparse(full_url).path.split('/') if p]
                                    # Ensure the path is a show folder (e.g., contains more than just a root slash or common path)
                                    if len(path_parts) >= 1:
                                        slug = path_parts[0]
                                        # Blacklist structural pages and dynamic grid paths
                                        blacklist = ["menu", "common", "features", "index", "help", "about", "search", "html", "allshows", "grid", "current"]
                                        
                                        # Check if slug is a blocked keyword or if URL contains blacklisted paths
                                        if slug.lower() not in blacklist and "/grid/" not in full_url:
                                            clean_url = f"https://epguides.com/{slug}/"
                                            if clean_url not in seen_urls:
                                                seen_urls.add(clean_url)
                                                
                                                # Extract clear visual text
                                                import html
                                                clean_title = re.sub(r'<[^>]+>', '', raw_anchor_text)
                                                clean_title = html.unescape(clean_title).split('|')[0].replace("epguides.com", "").strip(" -–—")
                                                
                                                # If extraction failed or slug is better, use slug logic
                                                if not clean_title or len(clean_title) < 3:
                                                    clean_title = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', slug).replace('_', ' ').title()
                                                
                                                results.append({'title': clean_title, 'url': clean_url, 'extra': 'epguides.com'})
                            
                            if results:
                                dialog = SearchResultDialog(results[:15], self)
                                if dialog.exec() and dialog.selected_url:
                                    url = dialog.selected_url
                                    self.add_to_history(url)
                                else:
                                    self.statusBar().showMessage("Search canceled.")
                                    return
                            else:
                                self.statusBar().showMessage("No matching epguides.com links found.")
                                return
                        except Exception as search_err:
                            self.statusBar().showMessage(f"Search match routing failed: {str(search_err)}")
                            return
                    else:
                        self.statusBar().showMessage(f"Direct connection failed with HTTP code {e.code}")
                        return
                except Exception as e:
                    self.statusBar().showMessage(f"Direct check lookup failed: {str(e)}")
                    return
            elif selected_profile == "Wikipedia.org":
                self.statusBar().showMessage(f"Searching Wikipedia.org for: {url}...")
                QApplication.processEvents()
                import urllib.parse
                try:
                    # Append keywords to force search results toward episode lists and TV series
                    query_encoded = urllib.parse.quote(f"{url} site:en.wikipedia.org \"List of\" episodes television series")
                    search_url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
                    
                    req_search = urllib.request.Request(search_url, headers=NetSkrabb.get_dynamic_headers(search_url))
                    with urllib.request.urlopen(req_search, timeout=10) as resp:
                        search_html = resp.read().decode('utf-8', errors='ignore')
                    
                    # Extract link blocks and anchor text
                    result_blocks = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', search_html, re.IGNORECASE)
                    
                    results = []
                    seen_urls = set()
                    for link, raw_anchor in result_blocks:
                        full_url = link
                        if "duckduckgo.com/l/?" in full_url:
                            parsed_proxy = urllib.parse.urlparse(full_url)
                            query_params = urllib.parse.parse_qs(parsed_proxy.query)
                            if 'uddg' in query_params:
                                full_url = query_params['uddg'][0]
                        
                        # Only process English Wikipedia article links
                        if "en.wikipedia.org/wiki/" in full_url:
                            # Only accept URLs that follow the strict "List_of_..._episodes" pattern
                            if "List_of_" in full_url and "_episodes" in full_url.lower():
                                # Quick check to exclude Talk or Category pages that might match the string
                                if "/wiki/Talk:" in full_url or "/wiki/Category:" in full_url:
                                    continue

                                import html
                                clean_title = re.sub(r'<[^>]+>', '', raw_anchor)
                                clean_title = html.unescape(clean_title).split(" - Wikipedia")[0].strip()
                                
                                if full_url not in seen_urls:
                                    seen_urls.add(full_url)
                                    results.append({'title': clean_title, 'url': full_url, 'extra': 'Episode List'})
                    
                    if results:
                        dialog = SearchResultDialog(results[:15], self)
                        if dialog.exec() and dialog.selected_url:
                            url = dialog.selected_url
                            self.add_to_history(url)
                        else:
                            self.statusBar().showMessage("Search canceled.")
                            return
                    else:
                        self.statusBar().showMessage("No matching Wikipedia articles found.")
                        return
                except Exception as e:
                    self.statusBar().showMessage(f"Wikipedia search failed: {str(e)}")
                    return

        # Global UI update to show progress immediately for all profiles
        self.statusBar().showMessage(f"Loading data from {selected_profile}...")
        QApplication.processEvents()

        

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
                    # Reference class-level headers
                    headers = NetSkrabb.HEADERS
                    req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
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
                    # Reference class-level headers
                    headers = NetSkrabb.HEADERS
                    req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
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
                            
                            # Unquote first to handle already encoded characters, then quote safely to avoid double-encoding
                            clean_path = urllib.parse.unquote(path_only)
                            encoded_path = urllib.parse.quote(clean_path, safe='/:()–')
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
            self.statusBar().showMessage("Loading data from epguides.com...")
            try:
                # Reference class-level headers
                req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_text = response.read().decode('utf-8', errors='ignore')
                
                # Extract the maze export ID parameter embedded in the source html page
                maze_match = re.search(r'exportToCSVmaze\.asp\?maze=(\d+)', html_text, re.IGNORECASE)
                if not maze_match:
                    self.statusBar().showMessage("Could not locate CSV export ID on the epguides.com page.")
                    return
                
                maze_id = maze_match.group(1)
                csv_url = f"https://epguides.com/common/exportToCSVmaze.asp?maze={maze_id}"
                
                req_csv = urllib.request.Request(csv_url, headers=NetSkrabb.get_dynamic_headers(csv_url))
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
                    self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} episodes from epguides.com CSV.")
                else:
                    self.input_text.setPlainText("No valid episode rows could be parsed from the CSV stream.")
                return
            except Exception as e:
                self.statusBar().showMessage(f"Error fetching from epguides.com: {str(e)}")
                return

        if selected_profile == "Wikipedia.org":
            self.statusBar().showMessage("Loading data from Wikipedia.org...")
            try:
                import urllib.request
                from bs4 import BeautifulSoup
                import html

                # Reference class-level headers
                headers = NetSkrabb.HEADERS
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
                    # Parse the URL to isolate the path, unquote it to prevent double-encoding, then re-quote safely
                    import urllib.parse
                    parsed = urllib.parse.urlparse(target_url)
                    clean_path = urllib.parse.unquote(parsed.path)
                    safe_path = urllib.parse.quote(clean_path, safe='/:()–')
                    safe_target_url = urllib.parse.urlunparse(parsed._replace(path=safe_path))

                    req = urllib.request.Request(safe_target_url, headers=NetSkrabb.get_dynamic_headers(safe_target_url))
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
                    self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} titles from Wikipedia.org.")
                else:
                    self.input_text.setPlainText("No valid episode titles could be identified from the Wikipedia.org tables.")
                    self.statusBar().showMessage("Load complete, but no matching table columns found.")
                return
            except Exception as e:
                self.statusBar().showMessage(f"Error fetching from Wikipedia.org: {str(e)}")
                return

        self.statusBar().showMessage("Loading data from MyAnimeList.net...")
        
        try:
            from html.parser import HTMLParser
            import html

            class MALEpisodesParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.episodes = []
                    self.pagination_urls = set()
                    self.series_title = "Series"
                    self.image_urls = []
                    self.current_num = None
                    self.in_num_cell = False
                    self.in_title_cell = False
                    self.in_title_link = False
                    self.in_pagination = False
                    self.current_title_chunks = []

                def handle_starttag(self, tag, attrs):
                    attrs_dict = dict(attrs)
                    cls = attrs_dict.get('class', '')
                    
                    if tag == 'meta':
                        if attrs_dict.get('property') == 'og:image':
                            img = attrs_dict.get('content')
                            if img and img not in self.image_urls: self.image_urls.append(img)
                        elif attrs_dict.get('property') == 'og:title':
                            # Extract series title, stripping the MyAnimeList.net suffix
                            self.series_title = attrs_dict.get('content').split(' - ')[0].strip()

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

            # Reference class-level headers
            headers = NetSkrabb.HEADERS

            # Phase 1: Fetch the primary page link given in the UI
            import urllib.parse
            p = urllib.parse.urlsplit(url)
            url = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path), p.query, p.fragment))
            req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
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
                        self.statusBar().showMessage(f"Loading additional episodes from offset page...")
                        req_extra = urllib.request.Request(extra_url, headers=NetSkrabb.get_dynamic_headers(extra_url))
                        with urllib.request.urlopen(req_extra, timeout=10) as response_extra:
                            html_extra = response_extra.read().decode('utf-8', errors='ignore')
                        parser.feed(html_extra)
                    except Exception:
                        pass

            # Phase 3: Fetch the 'pictures' page to gather high-res posters for the picker
            try:
                base_url = url.split('/episode')[0]
                pics_url = f"{base_url.rstrip('/')}/pics"
                req_pics = urllib.request.Request(pics_url, headers=NetSkrabb.get_dynamic_headers(pics_url))
                if any(arg in sys.argv for arg in ["-DevDebug", "-Dev", "-DBG"]):
                    print(f"[DevDebug] Attempting to scrape pics from: {pics_url}")
                with urllib.request.urlopen(req_pics, timeout=5) as resp_pics:
                    html_pics = resp_pics.read().decode('utf-8', errors='ignore')
                    # Capture CDN URLs and de-duplicate by Filename (Image ID) to avoid JPG/WebP duplicates
                    # This regex targets the numeric ID immediately preceding the extension
                    pic_matches = re.findall(r'(https://cdn\.myanimelist\.net/images/anime/\d+/(\d+)[^"\'\s/]*\.(?:jpg|jpeg|png|webp))', html_pics)
                    id_map = {}
                    for p_url, p_id in pic_matches:
                        exclude = ['t.jpg', 'v.jpg', 'l.jpg', 't.png', 'v.png', 'l.png', 't.jpeg', 'v.jpeg', 'l.jpeg', 't.webp', 'v.webp', 'l.webp']
                        if not any(p_url.lower().endswith(x) for x in exclude):
                            # Keep the first unique ID found; format preference is handled during final save
                            if p_id not in id_map:
                                id_map[p_id] = p_url
                    
                    for final_url in id_map.values():
                        if final_url not in parser.image_urls: parser.image_urls.append(final_url)
            except Exception:
                pass

            # Global de-duplication: Prioritize JPG over WebP across all gathered URLs
            final_id_map = {}
            for url in parser.image_urls:
                # Extract the Image ID from the filename
                id_match = re.search(r'/(\d+)[^/]*\.(?:jpg|jpeg|png|webp)', url)
                if id_match:
                    p_id = id_match.group(1)
                    if p_id not in final_id_map:
                        final_id_map[p_id] = url
                else:
                    # Fallback for non-standard CDN paths
                    final_id_map[url] = url
            
            self.scraped_images = list(final_id_map.values())
            self.scraped_title = parser.series_title
            if self.scraped_images:
                self.selected_image_urls = [self.scraped_images[0]]

            # De-duplicate rows by episode number and format output text cleanly
            unique_episodes = {}
            for ep_num, full_title in parser.episodes:
                unique_episodes[ep_num] = full_title
                
            episodes_found = [f"{num} {unique_episodes[num]}" for num in sorted(unique_episodes.keys())]

            if episodes_found:
                self.input_text.setPlainText('\n'.join(episodes_found))
                self.statusBar().showMessage(f"Successfully scraped {len(episodes_found)} episodes from MyAnimeList.net.")
            else:
                self.input_text.setPlainText("No episodes could be found using the structural HTML parser.")
                self.statusBar().showMessage("Load complete, but no matching table rows found.")
                
        except Exception as e:
            self.statusBar().showMessage(f"Network error during fetch: {str(e)}")

    def placeholder_clean(self):
        import re
        raw_text = self.input_text.toPlainText()
        if not raw_text.strip():
            self.statusBar().showMessage("No text to clean.")
            return

        selected_profile = self.profile_dropdown.currentText()
        
        # Guard: Ensure cover is selected for Western profiles if download is enabled
        if self.img_download_checkbox.isChecked() and not getattr(self, 'selected_image_urls', []):
            if selected_profile in ["epguides.com", "Wikipedia.org"]:
                self.statusBar().showMessage("No Cover Selected")
                return

        # Trigger image download/conversion if the checkbox is active (All Profiles)
        saved_img = self.handle_image_download()

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
            self.output_text.setFocus()
            self.output_text.selectAll()
            status_msg = f"Successfully cleaned {len(cleaned_episodes)} episodes."
            if saved_img:
                status_msg += f" | Cover saved: {saved_img}"
            self.statusBar().showMessage(status_msg)
        else:
            self.statusBar().showMessage("Could not find any matching episode patterns.")

    def placeholder_copy(self):
        output_content = self.output_text.toPlainText()
        if not output_content.strip():
            return
            
        clipboard = QApplication.clipboard()
        clipboard.setText(output_content)
        
        from PyQt6.QtCore import QTimer
        self.copy_btn.setText("✔ Copied!")
        self.copy_btn.setEnabled(False)
        self.statusBar().showMessage("Cleaned text successfully copied to clipboard.")
        
        QTimer.singleShot(1500, self.reset_copy_button)

    def reset_copy_button(self):
        self.copy_btn.setText("Copy to Clipboard")
        # Ensure it stays enabled only if there is still content in the output box
        if self.output_text.toPlainText().strip():
            self.copy_btn.setEnabled(True)
    
    def update_button_states(self):
        # Dynamically enable/disable buttons based on whether text boxes are empty
        has_input = bool(self.input_text.toPlainText().strip())
        has_output = bool(self.output_text.toPlainText().strip())
        
        self.clean_btn.setEnabled(has_input)
        self.save_btn.setEnabled(has_output)
        # If the copy button is currently in its "Copied!" feedback state, don't force it back to enabled
        if self.copy_btn.text() == "Copy to Clipboard":
            self.copy_btn.setEnabled(has_output)
    
    def clear_fields(self):
        # Clear the visible text in the input area without wiping the history items
        self.url_input.setCurrentText("")
        self.input_text.clear()
        self.output_text.clear()
        self.statusBar().showMessage("Ready")
        
    def save_output_to_file(self):
        content = self.output_text.toPlainText()
        if not content.strip():
            self.statusBar().showMessage("No cleaned text to save.")
            return

        import re
        import os
        from PyQt6.QtWidgets import QFileDialog
        
        # Sanitize title for filename
        clean_title = re.sub(r'[\\/*?:"<>|]', '', self.scraped_title).strip()
        default_name = f"{clean_title}.txt" if clean_title else "Cleaned_Episodes.txt"

        start_path = self.app_config.get('last_save_path', '')
        initial_path = os.path.join(start_path, default_name)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Cleaned Text", initial_path, "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            self.update_config_key('last_save_path', os.path.dirname(file_path))
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.statusBar().showMessage(f"File saved: {os.path.basename(file_path)}")
            except Exception as e:
                self.statusBar().showMessage(f"Failed to save file: {str(e)}")

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
        dialog.clear_cache_btn.clicked.connect(self.clear_image_cache)
        dialog.exec()

    def clear_image_cache(self):
        import shutil
        try:
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir, exist_ok=True)
            self.statusBar().showMessage("Image cache folder cleared.")
        except Exception as e:
            self.statusBar().showMessage(f"Failed to clear cache: {e}")

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
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox
        from PyQt6.QtCore import Qt, QUrl
        import os

        dialog = QDialog(self)
        dialog.setWindowTitle("About NetSkrabb")
        dialog.resize(500, 500)
        layout = QVBoxLayout(dialog)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet("""
            QTextBrowser {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                line-height: 1.5;
                color: palette(text);
                background-color: palette(base);
                border: none;
                padding: 10px;
            }
            h2 { color: #007acc; margin-top: 0; }
            b { color: #007acc; }
            a { color: #007acc; text-decoration: none; }
        """)

        about_text = (
            f"<h2>NetSkrabb v{APP_VERSION}</h2>"
            f"Copyright (C) 2026 pwshAgyjkcrg761<br>"
            f"Licensed under GPLv3<br><br>"
            f"This program is free software: you can redistribute it and/or modify "
            f"it under the terms of the GNU General Public License as published by "
            f"the Free Software Foundation, either version 3 of the License, or "
            f"(at your option) any later version.<br><br>"
            f"This program is distributed in the hope that it will be useful, "
            f"but WITHOUT ANY WARRANTY; without even the implied warranty of "
            f"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            f"GNU General Public License for more details.<br><br>"
            f"<b>Icon Credits:</b><br>"
            f"'Crab' (NetSkrabb-icon.png, NetSkrabb-icon.svg ) by JoyPixels via <a href='https://www.svgrepo.com/svg/401352/crab'>SVGRepo</a>.<br>"
            f"Used under MIT License. Modified by pwshAgyjkcrg761 (Color/Format).<br><br>"
            f"'Mars' (mars-url-icon.svg) by Good Stuff No Nonsense via <a href='https://www.svgrepo.com/svg/440497/mars'>SVGRepo</a>.<br>"
            f"Used under Creative Commons Attribution. Modified by pwshAgyjkcrg761 (Metadata/Format).<br><br>"
            f"You should have received a copy of the GNU General Public License "
            f"along with this program. If not, see "
            f"<a href='https://www.gnu.org/licenses/gpl-3.0.html'>https://www.gnu.org/licenses/gpl-3.0.html</a>."
        )

        browser.setHtml(about_text)
        layout.addWidget(browser)

        # Standard button box with a custom Action button for the license file
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        license_btn = buttons.addButton("View Icon Licenses", QDialogButtonBox.ButtonRole.ActionRole)
        
        def view_license():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icons_dir = os.path.join(script_dir, "NetSkrabb_internal", "icons")
            if os.path.exists(icons_dir):
                os.startfile(icons_dir)
            else:
                self.statusBar().showMessage(f"Error: {icons_dir} not found.")

        license_btn.clicked.connect(view_license)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        dialog.exec()

    def open_manual_dialog(self):
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtCore import Qt
        
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("NetSkrabb Manual")
        dialog.resize(650, 550) # Constrain size to prevent taskbar overflow
        
        layout = QVBoxLayout(dialog)
        
        # Using QTextBrowser provides native scrollbars and handles HTML formatting
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet("""
            QTextBrowser {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 14px;
                line-height: 1.6;
                color: palette(text);
                background-color: palette(base);
                border: none;
                padding: 20px;
            }
            h1 { color: #007acc; font-size: 22px; margin-bottom: 0px; }
            h2 { color: #007acc; font-size: 18px; border-bottom: 1px solid #444; padding-bottom: 5px; margin-top: 25px; }
            b { color: #007acc; }
            .license-box { 
                background-color: rgba(128, 128, 128, 0.1); 
                border-left: 4px solid #007acc; 
                padding: 15px; 
                font-family: monospace; 
                font-size: 12px;
                margin: 15px 0;
            }
            .step-card {
                background-color: rgba(0, 122, 204, 0.05);
                border: 1px solid rgba(0, 122, 204, 0.2);
                border-radius: 6px;
                padding: 12px;
                margin-bottom: 10px;
            }
            code { 
                font-family: 'Consolas', monospace; 
                background-color: rgba(128, 128, 128, 0.2); 
                padding: 2px 5px; 
                border-radius: 3px; 
            }
            a { color: #007acc; text-decoration: none; }
        """)
        
        manual_text = (
            f"<h1>NetSkrabb.py v{APP_VERSION}</h1>"
            f"<p style='margin-top: 0;'>MANUAL & USAGE GUIDE | Copyright (C) 2026 pwshAgyjkcrg761</p>"
            
            f"<br>"

            f"<h2>OVERVIEW</h2>"
            f"<p>NetSkrabb is a high-performance metadata scraper and filename formatter designed to "
            f"standardize media libraries. It intelligently loads episode titles from major web "
            f"sources and processes them into Windows-legal file system names.</p>"

            f"<h2>DEPENDENCIES</h2>"
            f"<ul>"
            f"<li><b>OS:</b> Microsoft Windows 10 / 11.</li>"
            f"<li><b>Python:</b> Built with Python 3.14.5.</li>"
            f"<li><b>PyQt6:</b> Orchestrates the graphical user interface.</li>"
            f"<li><b>Beautiful Soup 4:</b> Powers the HTML parsing engine for Western profiles.</li>"
            f"</ul>"

            f"<h2>USAGE WORKFLOW</h2>"
            f"<div class='step-card'><b>1. URL / Search:</b> Enter a direct URL or type a series name in the URL box.</div>"
            f"<div class='step-card'><b>2. Profile:</b> Ensure the 'Site Profile' matches your target source.</div>"
            f"<div class='step-card'><b>3. Load:</b> Press Enter in the URL box to load raw metadata into the input area.</div>"
            f"<div class='step-card'><b>4. Clean:</b> Click 'CLEAN & FORMAT' to finalize the filename list.</div>"

            f"<h2>CORE FEATURES</h2>"
            f"<p><b>Site Profile:</b> Determines parsing logic. <b>MyAnimeList</b> handles Japanese animation, "
            f"while <b>epguides</b> and <b>Wikipedia</b> target Western television series. <b>ThePosterDB</b> is supported for direct poster gallery scraping.</p>"
            
            f"<p><b>Filters:</b> Access via <code>Tools > Filters</code>. This menu controls pipeline stages "
            f"including Roman numeral translation, marker stripping, forward-slash conversion, and Windows-illegal character sanitation.</p>"
            
            f"<p><b>Absolute Numbering:</b> (Anime Only) Overrides source numbering with a continuous "
            f"sequence starting from your defined integer.</p>"

            f"<p><b>Developer Flags:</b> Launch with <code>-DevDebug</code>, <code>-Dev</code>, or <code>-DBG</code> "
            f"to enable terminal logging of network requests and image metadata.</p>"

            f"<h2>NOTES</h2>"
            f"<ul>"
            f"<li><b>Cover Images:</b> Enable 'Download Cover Image' to save high-resolution "
            f"posters using standardized filenames for media servers.</li>"
            f"<li><b>Manual Overrides:</b> The top text box is fully editable. You can correct "
            f"source metadata manually before triggering the clean pass.</li>"
            f"</ul>"
            f"<hr><p style='text-align: center; color: #888888;'><small>Licensed under GPLv3. See the <b>About</b> section for full legal details.</small></p>"
        )
        
        browser.setHtml(manual_text)
        layout.addWidget(browser)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec()

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
        self.update_config_key('min_digits', value)

    def update_config_key(self, key, value):
        import json
        self.app_config[key] = value
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
        
        # Keep image widgets visible for all profiles to support manual poster sourcing
        self.img_download_checkbox.setVisible(True)
        self.img_choose_btn.setVisible(True)
        
        # Synchronize the Absolute Numbering container visibility state
        self.abs_container.setVisible(is_anime)

    def toggle_img_button_state(self, state):
        is_checked = self.img_download_checkbox.isChecked()
        self.img_choose_btn.setEnabled(is_checked)
        self.update_config_key('download_cover_image', is_checked)

    def open_image_picker_dialog(self):
        if not self.scraped_images:
            self.statusBar().showMessage("No images available. Please load a MyAnimeList.net URL first.")
            return
            
        self.statusBar().showMessage("Loading image gallery...")
        from PyQt6.QtCore import Qt
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        dialog = ImagePickerDialog(self.scraped_images, self)
        QApplication.restoreOverrideCursor()
        
        if dialog.exec():
            self.selected_image_urls = dialog.selected_urls
            count = len(self.selected_image_urls)
            self.statusBar().showMessage(f"Selected {count} image{'s' if count != 1 else ''} for download.")

    def handle_image_download(self):
        if not self.img_download_checkbox.isChecked() or not getattr(self, 'selected_image_urls', []):
            return

        from PyQt6.QtWidgets import QFileDialog
        from PyQt6.QtGui import QImage
        import os
        import urllib.request
        import re

        start_path = self.app_config.get('last_save_path', '')
        save_dir = QFileDialog.getExistingDirectory(self, "Select Destination Folder for Cover Image", start_path)
        if not save_dir:
            return
        self.update_config_key('last_save_path', save_dir)

        saved_files = []
        total = len(self.selected_image_urls)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(total > 1) 

        try:
            for i, url in enumerate(self.selected_image_urls):
                # Proactive Throttling: Pause after 10 items to avoid 429 Rate Limiting
                if i >= 10:
                    self.progress_bar.setFormat(f"Rate Limit Sleep... {i+1}/{total}")
                    import time
                    time.sleep(2.0)
                
                self.progress_bar.setFormat(f"Downloading Cover {i+1} of {total}...")
                try:
                    target_url = url
                    # 1. High-res upgrade logic
                    tpdb_id = self.tpdb_id_map.get(url)
                    if tpdb_id:
                        target_url = f"https://theposterdb.com/api/assets/{tpdb_id}/view"
                    elif "cdn.myanimelist.net" in target_url:
                        u_base, u_ext = os.path.splitext(target_url)
                        if not u_base.endswith('l'): target_url = f"{u_base}l{u_ext}"
                    
                    # 2. Determine file metadata
                    if target_url.endswith('/view'):
                        p_id = target_url.split('/')[-2]
                        orig_name, orig_ext = p_id, ".jpg"
                        cache_fn = f"{p_id}_view.jpg"
                    else:
                        orig_filename = target_url.split('/')[-1].split('?')[0]
                        orig_name, orig_ext = os.path.splitext(orig_filename)
                        cache_fn = orig_filename
                    
                    cache_path = os.path.join(self.cache_dir, cache_fn)
                    do_convert = self.app_config.get('convert_to_jpg', True)
                    is_already_jpg = orig_ext.lower() in ['.jpg', '.jpeg']
                    target_ext = ".jpg" if (do_convert and not is_already_jpg) else orig_ext
                    
                    clean_title = re.sub(r'[\\/*?:"<>|]', '', self.scraped_title).replace(' ', '_')
                    final_filename = f"{clean_title}-{orig_name}-folder{target_ext}"
                    save_path = os.path.join(save_dir, final_filename)

                    # 3. Fetch/Cache handling
                    if os.path.exists(cache_path):
                        with open(cache_path, 'rb') as f: image_data = f.read()
                    else:
                        req = urllib.request.Request(target_url, headers=NetSkrabb.get_dynamic_headers(target_url))
                        with urllib.request.urlopen(req, timeout=10) as resp: image_data = resp.read()
                        with open(cache_path, 'wb') as f: f.write(image_data)

                    # 4. Save and Conversion
                    if do_convert and not is_already_jpg:
                        img = QImage()
                        if img.loadFromData(image_data):
                            img.save(save_path, "JPG", 90)
                    else:
                        with open(save_path, 'wb') as f: f.write(image_data)
                    
                    saved_files.append(final_filename)
                except Exception as e:
                    if any(arg in sys.argv for arg in ["-DevDebug", "-Dev", "-DBG"]):
                        print(f"[DevDebug] Skip error on item {i+1}: {e}")
                    continue
                finally:
                    self.progress_bar.setValue(i + 1)
                    QApplication.processEvents()

            self.progress_bar.setVisible(False)
            return ", ".join(saved_files) if len(saved_files) <= 2 else f"{len(saved_files)} images"
        except Exception as global_e:
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage(f"Batch failed: {str(global_e)}")
            return None

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
    
    def auto_detect_profile(self, text):
        # Scan for domain fingerprints and update the profile dropdown automatically
        lower_text = text.lower()
        # Resolve icon paths across split directories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        mars_dir = os.path.join(base_dir, "NetSkrabb_internal", "icons", "url_icon")
        
        def set_url_pixmap(filename):
            from PyQt6.QtGui import QPixmap
            # Determine directory: Mars stays in icons, others in url_icons_downloaded
            target_dir = mars_dir if filename == "mars-url-icon.svg" else self.url_icons_dir
            p_path = os.path.join(target_dir, filename)
            
            if os.path.exists(p_path):
                self.url_icon.setPixmap(QPixmap(p_path))
            else:
                # Fallback to Mars if specific icon is missing or not yet downloaded
                fallback = os.path.join(mars_dir, "mars-url-icon.svg")
                if os.path.exists(fallback):
                    self.url_icon.setPixmap(QPixmap(fallback))

        # Default/Idle/Search state (Use Mars)
        # Permissive URL detection (checks for common protocol or domain dots)
        is_url = lower_text.startswith(("http", "www.")) or ("." in lower_text and "/" in lower_text)
        
        if not is_url or not lower_text.strip():
            set_url_pixmap("mars-url-icon.svg")
            return

        # Logic for Icons and Profile Auto-switching
        if "myanimelist.net" in lower_text:
            set_url_pixmap("mal.svg")
            self.profile_dropdown.setCurrentText("MyAnimeList.net")
        elif "wikipedia.org" in lower_text:
            set_url_pixmap("wiki.ico")
            self.profile_dropdown.setCurrentText("Wikipedia.org")
        elif "theposterdb.com" in lower_text:
            set_url_pixmap("tpdb.png")
            # Note: ThePosterDB has no dedicated text profile, stays on current
        elif "epguides.com" in lower_text:
            set_url_pixmap("epguides.ico")
            self.profile_dropdown.setCurrentText("epguides.com")
        else:
            set_url_pixmap("mars-url-icon.svg")
            
    def sync_site_icons(self):
        """Ensures site-specific favicons exist locally; downloads if missing."""
        icons = {
            "mal.svg": "https://cdn.myanimelist.net/images/favicon.svg",
            "wiki.ico": "https://www.wikipedia.org/static/favicon/wikipedia.ico",
            "tpdb.png": "https://theposterdb.com/images/logos/tpdb_icon.png",
            "epguides.ico": "https://epguides.com/favicon.ico"
        }
        for filename, url in icons.items():
            path = os.path.join(self.url_icons_dir, filename)
            # Remove empty or corrupt files from previous failed attempts
            if os.path.exists(path) and os.path.getsize(path) == 0:
                os.remove(path)

            if not os.path.exists(path):
                try:
                    # Use generic headers for the initial icon sync
                    req = urllib.request.Request(url, headers=NetSkrabb.get_dynamic_headers(url))
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        with open(path, 'wb') as f:
                            f.write(resp.read())
                except Exception:
                    pass
    
    def add_to_history(self, text):
        if not text:
            return
        
        history = self.app_config.get('url_history', [])
        if text in history:
            history.remove(text)
        history.insert(0, text)
        self.app_config['url_history'] = history[:10]
        
        self.url_input.blockSignals(True)
        self.url_input.clear()
        self.url_input.addItems(self.app_config['url_history'])
        self.url_input.setCurrentText(text)
        self.url_input.blockSignals(False)

        import json
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