#!/usr/bin/env python3

from datetime import datetime
from enum import Enum
import time
import os

"""
Name:           dlenhart/clock
Description:    python clock for the terminal
Author:         Drew D. Lenhart
Repository:     https://github.com/dlenhart/clock
"""


class ANSICodes(Enum):
    """ANSI Colors and other codes"""

    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    CURSOR_TOP_LEFT = '\033[H'
    CLEAR_SCREEN_FROM_CURSOR = '\033[J'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'


class ClockEmoji(Enum):
    """Clock unicode characters"""

    ONE_O_CLOCK = '\U0001F550'
    ONE_THIRTY = '\U0001F55C'
    TWO_O_CLOCK = '\U0001F551'
    THREE_O_CLOCK = '\U0001F552'
    FOUR_O_CLOCK = '\U0001F553'
    FIVE_O_CLOCK = '\U0001F554'
    SIX_O_CLOCK = '\U0001F555'
    SEVEN_O_CLOCK = '\U0001F556'
    EIGHT_O_CLOCK = '\U0001F557'
    NINE_O_CLOCK = '\U0001F558'
    TEN_O_CLOCK = '\U0001F559'
    ELEVEN_O_CLOCK = '\U0001F55A'
    TWELVE_O_CLOCK = '\U0001F55B'


class Clock:
    """Console display time"""

    _color = None

    def __init__(self, color: str = ANSICodes.MAGENTA.value):
        self._color = self._select_color(color)

    def display(self, display_seconds: bool = True, center: bool = True) -> None:
        """Console time, hours, minutes and seconds"""

        try:
            while True:
                hours, minutes, seconds = Clock._parse_date_time()
                clock_icon = self._get_clock_icon(hours)

                current_time = Clock._format_time(
                    hours, minutes, seconds, display_seconds, self._parse_am_pm(), clock_icon
                )

                self._set_terminal()
                self._write(f""
                            f"{self._color}"
                            f"{self._center_text(current_time) if center else current_time}"
                            f"{ANSICodes.RESET.value}"
                            )

                time.sleep(1)
        except KeyboardInterrupt:
            exit_message = "Exiting clock..."

            self._set_terminal()
            self._write(f""
                        f"{self._color}"
                        f"{self._center_text(exit_message) if center else exit_message}"
                        f"{ANSICodes.RESET.value}"
                        )
            self._write(ANSICodes.SHOW_CURSOR.value)
        finally:
            exit(0)

    @staticmethod
    def _set_terminal() -> None:
        Clock._write(f""
                     f"{ANSICodes.CURSOR_TOP_LEFT.value}"
                     f"{ANSICodes.CLEAR_SCREEN_FROM_CURSOR.value}"
                     f"{ANSICodes.HIDE_CURSOR.value}"
                     )

    @staticmethod
    def _write(message: str = '') -> None:
        """Print to the console"""

        print(f'{message}')

    @staticmethod
    def _parse_date_time():
        """Extract and parse date time"""

        current_date_time = str(datetime.now()).split()
        split_time = current_date_time[1].split(".")[0]
        parsed_time = split_time.split(":")

        hours = parsed_time[0] or '00'
        minutes = parsed_time[1] or '00'
        seconds = parsed_time[2] or '00'

        return hours, minutes, seconds

    @staticmethod
    def _parse_am_pm() -> str:
        """Extract AM or PM"""

        now = datetime.now()
        return now.strftime("%p")

    @staticmethod
    def _get_clock_icon(hours) -> Enum:
        """Get clock icon based on time"""

        match int(hours):
            case 1 | 13:
                return ClockEmoji.ONE_O_CLOCK
            case 2 | 14:
                return ClockEmoji.TWO_O_CLOCK
            case 3 | 15:
                return ClockEmoji.THREE_O_CLOCK
            case 4 | 16:
                return ClockEmoji.FOUR_O_CLOCK
            case 5 | 17:
                return ClockEmoji.FIVE_O_CLOCK
            case 6 | 18:
                return ClockEmoji.SIX_O_CLOCK
            case 7 | 19:
                return ClockEmoji.SEVEN_O_CLOCK
            case 8 | 20:
                return ClockEmoji.EIGHT_O_CLOCK
            case 9 | 21:
                return ClockEmoji.NINE_O_CLOCK
            case 10 | 22:
                return ClockEmoji.TEN_O_CLOCK
            case 11 | 23:
                return ClockEmoji.ELEVEN_O_CLOCK
            case _:
                return ClockEmoji.TWELVE_O_CLOCK

    @staticmethod
    def _select_color(color: str) -> str:
        """Dynamically select the color"""

        if color:
            func = getattr(ANSICodes, color.upper())
            return func.value

        return ANSICodes.WHITE.value

    @staticmethod
    def _center_text(text: str) -> str:
        terminal_size = os.get_terminal_size()
        return text.center(terminal_size.columns)

    @staticmethod
    def _format_time(hours: str, minutes: str, seconds: str, display_seconds: bool, am_pm: str, icon: Enum) -> str:
        """Format time output"""

        dsp_sec = f":{seconds}" if display_seconds else ""
        return f"{icon.value} {hours}:{minutes}" + dsp_sec + f" {am_pm}"


if __name__ == "__main__":
    Clock('BRIGHT_MAGENTA').display(display_seconds=True, center=True)
