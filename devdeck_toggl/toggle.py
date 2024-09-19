"""Toggl basic Toggle control for DevDeck."""
import time
import threading
from datetime import datetime

from toggl import api

from devdeck_core.controls.deck_control import DeckControl


class Toggle(DeckControl):
    def __init__(self, key_no, **kwargs):
        super().__init__(key_no, **kwargs)
        self.thread = None
        self.stopped = threading.Event()
        self.lock = threading.Lock()
    
    def initialize(self):
        self.thread = threading.Thread(target=self._update_display_loop)
        self.thread.start()

    @property
    def task_entry(self):
        """running time entry."""
        return api.TimeEntry.objects.current()

    def _worked(self, entry):
        """time worked today in seconds."""
        day_start = datetime.today().replace(hour=0, minute=0, microsecond=0)
        worked = sum(
            (
                e.duration
                for e in api.TimeEntry.objects.all_from_reports(start=day_start)
            )
        )
        if entry:
            worked += int(time.time()) + entry.duration
        return worked

    def pressed(self):
        current = self.task_entry
        if current is None:
            current = api.TimeEntry.objects.all(order="desc")[0]
            current.continue_and_save()
        else:
            current.stop_and_save()
        self._update_display()

    def _update_display_loop(self):
        while True:
            self._update_display()
            if self.stopped.wait(60):
                return

    def _update_display(self):
        with self.lock:
            with self.deck_context() as context:
                entry = self.task_entry
                worked = self._worked(entry)
                hours = worked // 3600
                minutes = (worked % 3600) // 60
                running = entry is not None
                state = "working" if running else "off"
                color = "orange" if running else "white"

                with context.renderer() as r:
                    r.text(f"{hours:02}:{minutes:02}")\
                        .color(color) \
                        .center_horizontally() \
                        .center_vertically(-100) \
                        .font_size(150) \
                        .end()
                    r.text(state) \
                        .color(color) \
                        .center_horizontally() \
                        .center_vertically(100) \
                        .font_size(100) \
                        .end()

    def dispose(self):
        self.stopped.set()
        if self.thread:
            self.thread.join()
