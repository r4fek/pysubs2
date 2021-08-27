import re
from xml.etree import ElementTree as ET

from .formatbase import FormatBase
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .time import timestamp_to_ms

TIMESTAMP = re.compile(r"(\d{1,2}):(\d{2}):(\d{2}):(\d{2,3})")


def timestamp_str_to_ms(t):
    return timestamp_to_ms(TIMESTAMP.match(t).groups())


class XMLFormat(FormatBase):
    """
    Implementation of XML subtitle pseudo-format
    """
    @classmethod
    def guess_format(cls, text):
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if text.startswith("<?xml"):
            return "xml"

    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        parser = ET.XMLParser(encoding=kwargs["encoding"])
        et = ET.parse(fp, parser=parser).getroot()
        events = []

        for el in et.find("Font").findall("Subtitle"):
            text = ""
            for e in el:
                line = ''.join(e.itertext())
                for f in e.findall("Font"):
                    if f.text is not None:
                        line = line.replace(f.text, "<i>" + f.text + "</i>")
                text += line + "\n"

            start = timestamp_str_to_ms(el.attrib["TimeIn"])
            end = timestamp_str_to_ms(el.attrib["TimeOut"])
            events.append(SSAEvent(start=start, end=end, text=text))

        subs.events = events
