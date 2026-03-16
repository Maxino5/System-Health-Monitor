import psutil
import smtplib
import time
import os
from email.message import EmailMessage

# --- CONFIGURATION ---
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 80.0
DISK_THRESHOLD = 90.0
BATTERY_THRESHOLD = 20.0  # Alert if below 20% and not charging
CHECK_INTERVAL = 3600    # 3600 seconds = 1 hour
FLAG_FILE = "first_run_completed.txt"

# Email Settings
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "receiver_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def send_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_system_stats():
    # Battery Check
    battery = psutil.sensors_battery()
    bat_percent = battery.percent if battery else "N/A"
    is_plugged = battery.power_plugged if battery else True
    
    stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "battery": bat_percent,
        "plugged": is_plugged
    }
    return stats

def monitor():
    first_run = not os.path.exists(FLAG_FILE)
    
    while True:
        stats = get_system_stats()
        is_healthy = True
        issues = []

        # Validation Logic
        if stats["cpu"] > CPU_THRESHOLD:
            is_healthy = False
            issues.append(f"High CPU: {stats['cpu']}%")
        
        if stats["mem"] > MEM_THRESHOLD:
            is_healthy = False
            issues.append(f"High Memory: {stats['mem']}%")

        if stats["battery"] != "N/A" and stats["battery"] < BATTERY_THRESHOLD and not stats["plugged"]:
            is_healthy = False
            issues.append(f"Low Battery: {stats['battery']}% (Not Charging)")

        status_str = "HEALTHY" if is_healthy else "UNHEALTHY"
        report = (
            f"Status: {status_str}\n"
            f"CPU: {stats['cpu']}%\n"
            f"Memory: {stats['mem']}%\n"
            f"Disk: {stats['disk']}%\n"
            f"Battery: {stats['battery']}%"
        )

        # Logic for sending email
        if first_run:
            subject = f"System Startup Report - {status_str}"
            send_alert(subject, report)
            # Create the flag file so we know first run is over
            with open(FLAG_FILE, "w") as f:
                f.write("completed")
            first_run = False 
        elif not is_healthy:
            send_alert("⚠️ System Health Alert: UNHEALTHY", report + "\n\nIssues:\n" + "\n".join(issues))

        print(f"Check completed at {time.ctime()}. Status: {status_str}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()