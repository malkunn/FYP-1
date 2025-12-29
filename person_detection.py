import serial
import time
import matplotlib.pyplot as plt

# --------- CONFIGURATION ---------
COM_PORT = 'COM3'
BAUD_RATE = 9600
MAX_POINTS = 200
# --------------------------------

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

distance_data = []
buzzer_data = []
time_data = []

start_time = time.time()

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# --- Graph 1: Ultrasonic Distance vs Time ---
line_dist, = ax1.plot([], [], 'b-')
ax1.set_ylabel("Distance (cm)")
ax1.set_title("Ultrasonic Distance vs Time")
ax1.grid(True)

# --- Graph 2: Buzzer State vs Time ---
line_buzz, = ax2.plot([], [], 'r-')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Buzzer (0/1)")
ax2.set_title("Buzzer State vs Time (0=OFF, 1=ON)")
ax2.set_ylim(-0.2, 1.2)
ax2.grid(True)

while True:
    try:
        raw = ser.readline().decode(errors="ignore").strip()

        # Expect: distance,buzzer
        if "," in raw:
            parts = raw.split(",")

            if len(parts) == 2:
                d_str = parts[0].strip()
                b_str = parts[1].strip()

                if d_str.isdigit() and b_str in ("0", "1"):
                    distance = int(d_str)
                    buzzer = int(b_str)

                    t = time.time() - start_time

                    distance_data.append(distance)
                    buzzer_data.append(buzzer)
                    time_data.append(t)

                    # keep fixed window
                    distance_data = distance_data[-MAX_POINTS:]
                    buzzer_data = buzzer_data[-MAX_POINTS:]
                    time_data = time_data[-MAX_POINTS:]

                    # update distance plot
                    line_dist.set_xdata(time_data)
                    line_dist.set_ydata(distance_data)

                    # update buzzer plot
                    line_buzz.set_xdata(time_data)
                    line_buzz.set_ydata(buzzer_data)

                    # autoscale
                    ax1.relim()
                    ax1.autoscale_view()

                    ax2.relim()
                    ax2.autoscale_view(scalex=True, scaley=False)

                    plt.pause(0.05)

    except KeyboardInterrupt:
        print("Stopped")
        break

ser.close()

