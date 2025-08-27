import win32com.client
import matplotlib.pyplot as plt
import pandas as pd
import time

# ================== OpenDSS Initialization ==================
try:
    dss_obj = win32com.client.Dispatch("OpenDSSEngine.DSS")
    if not dss_obj.Start("0"):
        print("Error: OpenDSS engine did not start.")
        exit()
except Exception as e:
    print(f"Failed to create OpenDSS COM object. Ensure OpenDSS is installed and registered. Error: {e}")
    exit()

dss_text = dss_obj.Text
dss_circuit = dss_obj.ActiveCircuit
dss_solution = dss_circuit.Solution

# Compile DSS File (update your path here)
dss_file_path = r"C:\Users\gulla\Desktop\grid\p2\tap_changer_circuit.dss"
dss_text.Command = f'Compile "{dss_file_path}"'

if dss_circuit.NumBuses == 0:
    print("Error: Circuit did not load correctly. Check the DSS file path.")
    exit()

# ================== Voltage Analysis Function ==================
def analyze_bus_voltages(bus_name, vmag_angle, v_base_kv):
    """
    Analyze voltages for all phases of a bus.
    Returns list of tuples: (bus, phase, V_mag, angle, pu, status)
    """
    phase_data = []
    base_volts = v_base_kv * 1000  # convert kV → V

    for i in range(0, len(vmag_angle), 2):
        v_mag = vmag_angle[i]
        v_ang = vmag_angle[i + 1]

        if base_volts > 0:
            v_pu = v_mag / base_volts
            if v_pu < 0.95:
                status = "⚠️ Undervoltage"
            elif v_pu > 1.05:
                status = "⚠️ Overvoltage"
            else:
                status = "✅ Normal"
        else:
            v_pu = None
            status = "Base not found"

        phase = (i // 2) + 1
        phase_data.append((bus_name, phase, v_mag, v_ang, v_pu, status))

    return phase_data

# ================== Simulation Function ==================
def run_simulation(transaction_kwh):
    print("=" * 70)
    print(f"💡 Simulating transaction of {transaction_kwh} kWh...")

    # Add load increase for heavy transaction
    if transaction_kwh > 10:
        dss_circuit.Loads.Name = "house1"
        dss_circuit.Loads.kW *= 3.5
        print("  -> High demand detected, load increased.")
    else:
        print("  -> Normal transaction, no extra load applied.")

    # Disable RegControl and solve
    dss_text.Command = "RegControl.Reg1.Enabled=No"
    dss_solution.Solve()

    before_data = []
    for bus_name in dss_circuit.AllBusNames:
        dss_circuit.SetActiveBus(bus_name)
        vmag_angle = dss_circuit.ActiveBus.VMagAngle
        v_base_kv = dss_circuit.ActiveBus.kVBase
        before_data.extend(analyze_bus_voltages(bus_name, vmag_angle, v_base_kv))

    # Enable RegControl and solve
    dss_text.Command = "RegControl.Reg1.Enabled=Yes"
    dss_solution.Solve()

    after_data = []
    for bus_name in dss_circuit.AllBusNames:
        dss_circuit.SetActiveBus(bus_name)
        vmag_angle = dss_circuit.ActiveBus.VMagAngle
        v_base_kv = dss_circuit.ActiveBus.kVBase
        after_data.extend(analyze_bus_voltages(bus_name, vmag_angle, v_base_kv))

    # Convert results to DataFrames
    df_before = pd.DataFrame(before_data, columns=["Bus", "Phase", "V_mag(V)", "Angle(deg)", "V_pu", "Status"])
    df_after = pd.DataFrame(after_data, columns=["Bus", "Phase", "V_mag(V)", "Angle(deg)", "V_pu", "Status"])

    # Get Tap Position
    dss_circuit.RegControls.Name = "Reg1"
    tap_position = dss_circuit.RegControls.TapNumber
    print(f"\n🔁 Tap Changer final position: {tap_position}")

    # Plot Voltage Profiles (per-unit)
    plt.figure(figsize=(12, 6))
    plt.plot(df_before["Bus"] + " P" + df_before["Phase"].astype(str), df_before["V_pu"],
             marker='o', label="Before Tap Changer")
    plt.plot(df_after["Bus"] + " P" + df_after["Phase"].astype(str), df_after["V_pu"],
             marker='s', label="After Tap Changer")
    plt.axhline(0.95, color='r', linestyle='--', alpha=0.7)
    plt.axhline(1.05, color='r', linestyle='--', alpha=0.7)
    plt.ylabel("Voltage (p.u.)", fontsize=12)
    plt.title(f"Voltage Profile for {transaction_kwh} kWh Transaction", fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return df_before, df_after

# ================== Main Execution ==================
if __name__ == "__main__":
    results = {}
    for kwh_value in [1, 3, 11]:
        df_b, df_a = run_simulation(kwh_value)
        results[kwh_value] = (df_b, df_a)
        time.sleep(1)

    # Optionally save results
    with pd.ExcelWriter("voltage_results.xlsx") as writer:
        for kwh, (df_b, df_a) in results.items():
            df_b.to_excel(writer, sheet_name=f"{kwh}kWh_Before", index=False)
            df_a.to_excel(writer, sheet_name=f"{kwh}kWh_After", index=False)

    print("\n✅ Simulation completed. Results saved to voltage_results.xlsx")
