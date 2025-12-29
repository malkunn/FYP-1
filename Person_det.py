import serial
import time
import matplotlib.pyplot as plt

# --------- CONFIGURATION ---------
COM_PORT = 'COM3'      # CHANGE if needed
BAUD_RATE = 9600
MAX_POINTS = 200       # number of points shown on graph
# --------------------------------

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino reset

distance_data = []
time_data = []

start_time = time.time()

plt.ion()  # interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')

ax.set_xlabel("Time (s)")
ax.set_ylabel("Distance (cm)")
ax.set_title("Ultrasonic Distance vs Time")

while True:
    try:
        line_data = ser.readline().decode().strip()

        if line_data.isdigit():
            distance = int(line_data)
            current_time = time.time() - start_time

            distance_data.append(distance)
            time_data.append(current_time)

            # keep graph size fixed
            distance_data = distance_data[-MAX_POINTS:]
            time_data = time_data[-MAX_POINTS:]

            line.set_xdata(time_data)
            line.set_ydata(distance_data)

            ax.relim()
            ax.autoscale_view()

            plt.pause(0.05)

    except KeyboardInterrupt:
        print("Stopped by user")
        break

ser.close()

