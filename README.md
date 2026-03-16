# System Health Monitor & Alerter 🖥️⚠️

A Python utility designed to monitor your computer's hardware resources in the background and send email notifications if performance thresholds are breached.

## ✨ Features
* **Real-time Metrics:** Monitors CPU usage, RAM consumption, Disk space, and Battery percentage.
* **Smart Alerting Logic:** * **First Run:** Sends a full status report (Healthy or Unhealthy) to confirm the script is working.
    * **Subsequent Checks:** Only sends an email if the system is "Unhealthy" (thresholds exceeded).
* **Battery Intelligence:** Alerts you if the battery drops below 20% while the charger is unplugged.
* **Hourly Automation:** Runs every 60 minutes via a persistent loop.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/system-health-monitor.git](https://github.com/YOUR_USERNAME/system-health-monitor.git)
   cd system-health-monitor
