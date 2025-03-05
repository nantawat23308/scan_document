from datetime import datetime, timedelta

def get_now_ymdhms():
    return format_datetime_ymdhms(datetime.now())

def format_datetime_ymdhms(dt: datetime) -> str:
    return dt.strftime('%Y%m%d-%H%M%S')

class TimeTracker:
    def __init__(self, identifier=None, start=False, logger=None):
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._identifier = identifier if identifier else ""

        if start:
            self.start()

    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifer = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value
        self._end_time = None
        self._duration = None

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value
        if self._start_time and self._end_time:
            self._duration = self._end_time - self._start_time
        else:
            self._duration = None

    @property
    def duration(self):
        return self._duration

    @property
    def start_time_formatted(self):
        return self._format_datetime(self._start_time)

    @property
    def end_time_formatted(self):
        return self._format_datetime(self._end_time)

    @property
    def duration_formatted(self):
        return self._format_duration(self._duration)

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        self.end_time = datetime.now()

    def _format_datetime(self, dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] if dt else None

    def _format_duration(self, duration):
        if duration:
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int(duration.microseconds / 1000)
            return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'
        return None