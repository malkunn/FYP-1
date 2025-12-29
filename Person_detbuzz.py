import serial
import time
import matplotlib.pyplot as plt

# --------- CONFIGURATION ---------
COM_PORT = 'COM3'      # CHANGE if needed
BAUD_RATE = 9600       # MUST match Arduino
MAX_POINTS = 200
# --------------------------------

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino reset

distance_data = []
buzzer_data = []
time_data = []

start_time = time.time()

plt.ion()
fig, ax = plt.subplots()

line_dist, = ax.plot([], [], 'b-', label="Distance (cm)")
line_buzz, = ax.plot([], [], 'r--', label="Buzzer (0/1)")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Distance / Buzzer State")
ax.set_title("Ultrasonic Distance & Buzzer State vs Time")
ax.legend()
ax.grid(True)

while True:
    try:
        line_data = ser.readline().decode().strip()

        # Expect format: distance,buzzer
        if "," in line_data:
            distance_str, buzzer_str = line_data.split(",")

            if distance_str.isdigit() and buzzer_str.isdigit():
                distance = int(distance_str)
                buzzer = int(buzzer_str)

                current_time = time.time() - start_time

                distance_data.append(distance)
                buzzer_data.append(buzzer * 100)  # scale for visibility
                time_data.append(current_time)

                # Keep fixed window
                distance_data = distance_data[-MAX_POINTS:]
                buzzer_data = buzzer_data[-MAX_POINTS:]
                time_data = time_data[-MAX_POINTS:]

                line_dist.set_xdata(time_data)
                line_dist.set_ydata(distance_data)

                line_buzz.set_xdata(time_data)
                line_buzz.set_ydata(buzzer_data)

                ax.relim()
                ax.autoscale_view()

                plt.pause(0.05)

    except KeyboardInterrupt:
        print("Stopped by user")
        break

ser.close()

