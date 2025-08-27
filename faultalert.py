import win32com.client
import time
import requests

# ✅ Path to your OpenDSS file
dss_file = r"C:\Users\gulla\Desktop\grid\p2\ieee13_p2p_microgrid.dss"

# ✅ n8n test webhook URL
n8n_webhook_url = "https://rakesh37.app.n8n.cloud/webhook-test/c6675df0-92c1-4be0-9d7e-a8d5332500c5"

# ✅ Initialize OpenDSS
dss = win32com.client.Dispatch("OpenDSSEngine.DSS")
dss.Start(0)

# ✅ Get Text and Circuit Interfaces
dss_text = dss.Text
dss_circuit = dss.ActiveCircuit

# ✅ Load the DSS file
dss_text.Command = f"Redirect {dss_file}"
print("🔌 Power system model loaded.")

# ✅ Ask user if fault should be applied
apply_fault = input("❓ Do you want to apply fault at House 1? (yes/no): ").strip().lower()

if apply_fault == 'yes':
    print("⚡ Applying fault at House 1...")

    # ✅ Apply a fault near House 1 (example at bus H1bus)
    dss_text.Command = "New Fault.f1 bus1=H1bus phases=1 r=0.0001"
    dss_text.Command = "Solve"

    print("🚨 Fault applied at House 1!")

    # ✅ Simulated backup check (customize as needed)
    backup_available = ['House2', 'House3']
    alert_msg = (
        "⚠️ Fault detected at House 1!\n"
        "🔎 Checking available backup options...\n"
        f"✅ House1 can be supplied by: {', '.join(backup_available)}"
    )
    print(alert_msg)

    # ✅ Send alert to n8n test webhook
    try:
        response = requests.post(n8n_webhook_url, json={
            "status": "fault",
            "house": "House1",
            "backup_sources": backup_available,
            "message": alert_msg
        })
        if response.status_code == 200:
            print("📤 Alert sent to n8n successfully.")
        else:
            print(f"⚠️ Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending to n8n: {e}")

else:
    print("✅ No fault applied. System running normally.")
