import re

from .formatbase import FormatBase
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .time import timestamp_to_ms

TIMESTAMP = re.compile(r"(\d{1,2}):(\d{2}):(\d{2}):(\d{2,3})")
TIME_LINE = re.compile(r'\d{4} \d{1,2}:\d{1,2}:\d{1,2}:\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}:\d{1,2}')


def timestamp_str_to_ms(t):
    return timestamp_to_ms(TIMESTAMP.match(t).groups())


class RtfFormat(FormatBase):
    @classmethod
    def guess_format(cls, text):
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if re.match(TIME_LINE, text.strip().split("\n")[0]):
            return "rtf"

    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        text = ""
        time, start, end = None, None, None
        events = []

        for line in fp:
            if not line:
                continue
            elif re.match(TIME_LINE, line):
                if time is not None:
                    events.append(SSAEvent(start=start, end=end, text=text))
                    text = ""
                time = line.split(" ")
                start = timestamp_str_to_ms(time[1])
                end = timestamp_str_to_ms(time[2])
            else:
                text += line + "\n"

        events.append(SSAEvent(start=start, end=end, text=text))
        subs.events = events
