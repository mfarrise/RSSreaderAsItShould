# 📰 CoryFlow — RSS News Ticker

A lightweight Python desktop app that displays RSS feeds as a scrolling news ribbon at the bottom of your screen — inspired by TV news tickers.

Built as part of a personal learning project.

---

## ✨ Features

* 📡 Live RSS feed parsing
* 🧵 Smooth horizontal scrolling ticker
* 🖱️ Interactive controls (mouse + keyboard)
* 🧩 Minimal, distraction-free UI
* ⚙️ adding feeds via JSON (GUI editor coming later)

---

## 🧑‍💻 Controls

| Action           | Behavior               |
| ---------------- | ---------------------- |
| **Double click** | Open news link         |
| **Right click**  | Open settings          |
| **Left click**   | Pause / resume ticker  |
| **Mouse scroll** | Adjust scrolling speed |
| **Drag**         | Move ticker position   |
| **Esc**          | Close application      |

---

## ⚙️ Configuration

Feeds are currently added manually via JSON.

* On first run, configuration files will be generated automatically.
* If you don’t see any JSON files yet — just run the app once.

Example:

```json
 [
    "https://example.com/feed",
    "https://another-feed.com/rss"
  ]

```

> GUI-based feed management is planned for a future update.

---

## 🚀 Getting Started

1. Clone the repository
2. Run the application
3. Edit the generated JSON file to add your feeds
4. Restart the app

---

## 📌 Notes

* Some RSS feeds include HTML formatting in descriptions (e.g., `<br>` tags). These are cleaned internally for display.
* Performance and features will evolve as the project grows.

---

## 🧠 Purpose

This project is part of a broader effort to:

* Learn Python GUI development
* Work with RSS parsing and real-time UI updates
* Build reusable components for future projects

---

## 🔮 Planned Improvements

* GUI for managing RSS feeds
* Better text formatting and truncation
* Theme customization
* Multi-line ticker support

---

Enjoy your personal news ribbon 👌

