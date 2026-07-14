# Deep Space RTT Calculator 🚀

**Description:**
Telegram bot for calculating radio signal round-trip time (RTT) in deep space communications. This tool visualizes communication latencies for different celestial bodies.

---

### Features
* **Real-time calculation:** Calculates signal delay based on custom distance input.
* **Pre-defined targets:** Quick presets for popular space missions and planets (Mars, Jupiter, Voyager-1).
* **User-friendly interface:** Intuitive Telegram UI built with `telebot`.

---

### Tech Stack
* **Language:** Python 3.10+
* **Core Library:** `telebot` (Asynchronous Telegram Bot API)
* **Physics:** Speed of light constant ($c \approx 3 \times 10^8 \text{ m/s}$) used for precise round-trip calculations.

---

### How to use & Examples
Start the bot and enter the distance or choose one of the built-in presets to see the RTT in action:
* **Mars:** RTT is approximately `25 min 1.02 secs`
* **Jupiter:** RTT is approximately `1 hour 26 min 28.26 secs`
* **Voyager-1:** RTT is approximately `1 day 21 hours 50 min`

---

### Architecture
* **Client side:** Telegram UI via BotFather API.
* **Backend:** Async polling core that handles user requests and computes light-travel time metrics.
