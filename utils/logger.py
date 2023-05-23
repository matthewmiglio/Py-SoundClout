import os
import time
from functools import wraps
from queue import Queue


class Logger:
    """Handles creating and reading logs"""

    def __init__(self, queue=None, timed=True):
        """Logger init"""

        self.queue: Queue[dict[str, str | int]] = Queue() if queue is None else queue

        self.driver_1_plays = 0
        self.driver_2_plays = 0
        self.driver_3_plays = 0
        self.driver_4_plays = 0
        self.driver_5_plays = 0
        self.driver_6_plays = 0
        self.driver_7_plays = 0
        self.driver_8_plays = 0
        self.driver_9_plays = 0
        self.driver_10_plays = 0
        self.driver_11_plays = 0
        self.driver_12_plays = 0
        self.driver_13_plays = 0
        self.driver_14_plays = 0
        self.driver_15_plays = 0

        self.driver_1_state = "idle"
        self.driver_2_state = "idle"
        self.driver_3_state = "idle"
        self.driver_4_state = "idle"
        self.driver_5_state = "idle"
        self.driver_6_state = "idle"
        self.driver_7_state = "idle"
        self.driver_8_state = "idle"
        self.driver_9_state = "idle"
        self.driver_10_state = "idle"
        self.driver_11_state = "idle"
        self.driver_12_state = "idle"
        self.driver_13_state = "idle"
        self.driver_14_state = "idle"
        self.driver_15_state = "idle"

        self.start_time = time.time()

    def _update_queue(self):
        """updates the queue with a dictionary of mutable statistics"""
        if self.queue is None:
            return

        statistics: dict[str, str | int] = {
            # "time_since_start": self.calc_time_since_start(),
            # "current_state": self.current_state,
        }
        self.queue.put(statistics)

    @staticmethod
    def _updates_queue(func):
        """decorator to specify functions which update the queue with statistics"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._update_queue()  # pylint: disable=protected-access
            return result

        return wrapper

    @_updates_queue
    def error(self, message: str):
        """logs an error"""
        self.errored = True
        self.status = f"Error: {message}"
        print(f"Error: {message}")

    @_updates_queue
    def log(self, message=""):
        """add message to log

        Args:
            message (str): message to add
            state (str): state of the program during the message
        """


        d1_string = f"Driver 1: |{self.driver_1_plays} plays |{self.driver_1_state}|\n"
        d2_string = f"Driver 2: |{self.driver_2_plays} plays |{self.driver_2_state}|\n"
        d3_string = f"Driver 3: |{self.driver_3_plays} plays |{self.driver_3_state}|\n"
        d4_string = f"Driver 4: |{self.driver_4_plays} plays |{self.driver_4_state}|\n"
        d5_string = f"Driver 5: |{self.driver_5_plays} plays |{self.driver_5_state}|\n"

        info_string = d1_string + d2_string + d3_string + d4_string + d5_string



        time_string = f"[{self.make_timestamp()}]\n"
        # info_string = f"[{self.driver_1_plays}][{self.driver_2_plays}][{self.driver_3_plays}][{self.driver_4_plays}][{self.driver_5_plays}]"

        print('________________\n\n'+time_string + info_string + message)

    @_updates_queue
    def update_driver_state(self, driver_index, new_state):
        if driver_index == 0:
            self.driver_1_state = new_state
        elif driver_index == 1:
            self.driver_2_state = new_state
        elif driver_index == 2:
            self.driver_3_state = new_state
        elif driver_index == 3:
            self.driver_4_state = new_state
        elif driver_index == 4:
            self.driver_5_state = new_state
        elif driver_index == 5:
            self.driver_6_state = new_state
        elif driver_index == 6:
            self.driver_7_state = new_state
        elif driver_index == 7:
            self.driver_8_state = new_state
        elif driver_index == 8:
            self.driver_9_state = new_state
        elif driver_index == 9:
            self.driver_10_state = new_state
        elif driver_index == 10:
            self.driver_11_state = new_state
        elif driver_index == 11:
            self.driver_12_state = new_state
        elif driver_index == 12:
            self.driver_13_state = new_state
        elif driver_index == 13:
            self.driver_14_state = new_state
        elif driver_index == 14:
            self.driver_15_state = new_state

    @_updates_queue
    def add_play(self, driver_number):
        if driver_number == 0:
            self.driver_1_plays += 1
        elif driver_number == 1:
            self.driver_2_plays += 1
        elif driver_number == 2:
            self.driver_3_plays += 1
        elif driver_number == 3:
            self.driver_4_plays += 1
        elif driver_number == 4:
            self.driver_5_plays += 1
        elif driver_number == 5:
            self.driver_6_plays += 1
        elif driver_number == 6:
            self.driver_7_plays += 1
        elif driver_number == 7:
            self.driver_8_plays += 1
        elif driver_number == 8:
            self.driver_9_plays += 1
        elif driver_number == 9:
            self.driver_10_plays += 1
        elif driver_number == 10:
            self.driver_11_plays += 1
        elif driver_number == 11:
            self.driver_12_plays += 1
        elif driver_number == 12:
            self.driver_13_plays += 1
        elif driver_number == 13:
            self.driver_14_plays += 1
        elif driver_number == 14:
            self.driver_15_plays += 1

    def calc_time_since_start(self) -> str:
        if self.start_time is not None:
            hours, remainder = divmod(time.time() - self.start_time, 3600)
            minutes, seconds = divmod(remainder, 60)
        else:
            hours, minutes, seconds = 0, 0, 0
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def make_timestamp(self):
        """creates a time stamp for log output

        Returns:
            str: log time stamp
        """
        output_time = time.time() - self.start_time
        output_time = int(output_time)

        time_str = str(self.convert_int_to_time(output_time))

        output_string = time_str

        return output_string

    def convert_int_to_time(self, seconds):
        """convert epoch to time

        Args:
            seconds (int): epoch time in int

        Returns:
            str: human readable time
        """
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)
