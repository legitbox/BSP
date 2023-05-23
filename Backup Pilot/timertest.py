import PySimpleGUI as sg
import threading
import time

def say_hello():
    print("Hello, world!")

def start_timer(minutes, active, window):
    while active[0]:
        seconds = minutes * 60
        while seconds > 0:
            if not active[0]:
                return
            window.write_event_value('-UPDATE-', f"{seconds // 60}:{seconds % 60:02}")
            time.sleep(1)
            seconds -= 1
        window.write_event_value('-UPDATE-', "Time's up!")
        say_hello()
        time.sleep(1)  # Wait for 1 second before starting the timer again

def timer_gui():
    layout = [
        [sg.Text("Set timer in minutes:"), sg.Input(key="-MINUTES-", size=(10, 1))],
        [sg.Button("Start"), sg.Button("Stop")],
        [sg.Text("Timer: ", key="-TIMER-")]
    ]

    window = sg.Window("Timer", layout, finalize=True)
    active = [False]

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == "Start":
            if not active[0]:
                try:
                    minutes = int(values["-MINUTES-"])
                    if minutes > 0:
                        active[0] = True
                        timer_thread = threading.Thread(target=start_timer, args=(minutes, active, window))
                        timer_thread.daemon = True
                        timer_thread.start()
                    else:
                        sg.popup("Please enter a valid number of minutes.")
                except ValueError:
                    sg.popup("Please enter a valid number of minutes.")

        if event == "Stop":
            if active[0]:
                active[0] = False
                window['-TIMER-'].update('')
                time.sleep(1)  # Wait for the timer thread to complete
                continue

        if event == "-UPDATE-":
            window['-TIMER-'].update(values[event])

    window.close()

if __name__ == "__main__":
    timer_gui()
