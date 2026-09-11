"""ULTRON application entry point."""

import sys


sys.coinit_flags = 2

import os


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from life_pulse import pulse_boot


if __name__ == "__main__":
    pulse_boot()
