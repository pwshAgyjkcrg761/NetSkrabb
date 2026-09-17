# <img src="NetSkrabb_internal/icons/NetSkrabb-icon.png" width="32" height="32"> NETSKRABB™ <img src="NetSkrabb_internal/icons/NetSkrabb-icon.png" width="32" height="32">
**A high-performance metadata scraper and filename formatter designed for media library standardization.**

---

![NetSkrabb Dark Mode Main Interface](images/NetSkrabb-py_main.png)

## Overview
NetSkrabb™ is a specialized utility designed to bridge the gap between web-based episode databases and local file system organization. It surgically scrapes metadata from major sources—specifically **MyAnimeList.net**, **epguides.com**, **Wikipedia.org**, and **ThePosterDB.com**—to generate clean, Windows-compliant filenames.

**Primary Environment:** Developed and tested on **Python 3.14.5** using the **PyQt6** framework. It is designed for users who require precise control over their media naming conventions without the overhead of heavy library management suites.

### The Scraper Engine
The utility utilizes a multi-profile parsing engine that adapts to the structural nuances of different web databases.

Key operational features include:
1. **Consolidated Site Profiles:** Seamlessly switches logic between Anime-centric (MAL) and Western TV (epguides/Wiki) formats, with specialized asset fetching for ThePosterDB.
2. **Surgical Filter Pipeline:** Implements a multi-stage string transformation pass that handles Roman numeral conversion, part/volume marker stripping, forward-slash sanitization, and contextual character replacement.
3. **Automated Cover Art Downloader:** The engine scans for high-resolution CDN assets across supported profiles, allowing users to select and save posters as `folder.jpg` (or series-specific titles) with optional high-quality JPG conversion.
4. **Absolute Numbering:** Provides a sequence override for anime series, allowing users to re-index episode numbers starting from a custom integer (e.g., for multi-season continuous numbering).

### Security & Precision
NetSkrabb™ operates with a "local-first" philosophy. No data is sent to third-party APIs; the script fetches raw HTML directly and parses it locally. The "Safe-Character" protocol ensures that visual punctuation (like `?` and `/`) is converted to safe Unicode variants (`？` and `∕`) to maintain folder tree integrity and PowerShell compatibility.

---

## Feature Reference

| Option | Description |
| :--- | :--- |
| **Min Digits** | Controls leading-zero padding for episode numbers (e.g., `01` vs `001`). |
| **Global Filters** | A master override that enables/disables the entire cleaning pipeline, including Roman numeral translation and illegal character stripping. |
| **Profile Auto-Detection** | Automatically switches the active scraper profile based on the domain detected in a pasted URL. |
| **Image Picker** | A thumbnail-based gallery with **Shift+Click** (range) and **Ctrl+Click** (toggle) support for batch selecting series posters. |
| **Theme Engine** | Supports Dark, Light, and System-synced UI modes via a custom QPalette implementation. |

---

## Assets & Licensing
This software is released under the **GNU General Public License v3**.

### Icon Credits
* **File:** `NetSkrabb-icon.png`
    * **Asset:** Crab SVG Vector
    * **Author:** JoyPixels
    * **Source:** <a href="https://www.svgrepo.com/svg/401352/crab" target="_blank">https://www.svgrepo.com/svg/401352/crab</a>
    * **License:** <a href="https://git.disroot.org/pwshAgyjkcrg761/NetSkrabb/src/branch/main/NetSkrabb_internal/icons/LICENSE" target="_blank">MIT License</a>
    * **Modifications:** Converted to PNG and color-adjusted for NetSkrabb branding.
      
*  **File:** `mars-url-icon.svg`
    * **Asset:** Mars SVG Vector
    * **Author:** Good Stuff No Nonsense
    * **Source:** <a href="https://www.svgrepo.com/svg/440497/mars" target="_blank">https://www.svgrepo.com/svg/440497/mars</a>
    * **License:** <a href="https://git.disroot.org/pwshAgyjkcrg761/NetSkrabb/src/branch/main/NetSkrabb_internal/icons/url_icons/LICENSE" target="_blank">CC Attribution License</a>
    * **Modifications:** Optimized metadata and formatting for application integration.

---

## Dependencies
* **OS:** Microsoft Windows 10 / 11.
* **Python:** 3.14.5+ (Recommended).
* **PyQt6:** Required for the Graphical User Interface.
* **Beautiful Soup 4:** Required for HTML table parsing on Wikipedia and epguides profiles.

## Support & Maintenance
**This repository is provided "as-is" for archival purposes.** The author is not actively looking for feedback, feature requests, or bug reports. The issue tracker is disabled.

## Disclaimer
*NetSkrabb™ is a tool for metadata management. The author is not responsible for the content of the pages scraped or any legal implications arising from the use of third-party website data. Always respect the robots.txt and terms of service of the host websites.*

---
> **Document Control**<br>
> *This document is up-to-date with the following version of NetSkrabb™.*<br>
> *2026.07.11__06.32.12*