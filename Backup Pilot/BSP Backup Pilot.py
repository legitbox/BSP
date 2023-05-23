import PySimpleGUI as sg
import time

def say_hello():
    print("Hello, world!")

class TimerGUI:
    def __init__(self):
        self.layout = [
            [sg.Text("Set timer in minutes:"), sg.Input(key="-MINUTES-", size=(10, 1))],
            [sg.Button("Start"), sg.Button("Stop")],
            [sg.Text("Timer: ", key="-TIMER-")]
        ]
        self.window = sg.Window("Timer", self.layout, finalize=True)
        self.active = False
        self.start_time = 0
        self.minutes = 0

    def start_timer(self):
        minutes = int(self.window["-MINUTES-"].get())
        if minutes <= 0:
            sg.popup("Please enter a valid number of minutes.")
            return

        self.active = True
        self.start_time = time.time()
        self.minutes = minutes
        self.update_timer()  # Start updating the timer immediately

    def stop_timer(self):
        self.active = False

    def update_timer(self):
        if self.active:
            elapsed_time = int(time.time() - self.start_time)
            remaining_seconds = self.minutes * 60 - elapsed_time

            if remaining_seconds > 0:
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                self.window["-TIMER-"].update(f"{minutes}:{seconds:02}")
            else:
                self.window.write_event_value('-UPDATE-', "Initiating backup")
                say_hello()
                self.active = False

        if self.active:
            self.window.write_event_value('-UPDATE-', "")  # Trigger event to update timer again
            self.window.refresh()  # Refresh the window to process the event

    def run(self):
        while True:
            event, _ = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break

            if event == "Start":
                if not self.active:
                    self.start_timer()

            if event == "Stop":
                if self.active:
                    self.stop_timer()
                    self.window["-TIMER-"].update('')

            if event == "-UPDATE-":
                self.window.refresh()  # Refresh the window to update the timer
                self.update_timer()

        self.window.close()

if __name__ == "__main__":
    timer_gui = TimerGUI()
    timer_gui.run()
