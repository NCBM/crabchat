class MessageType:
    T_TEXT = 1


class Message:
    def __init__(self, mtype, data=None):
        self.mtype = mtype
        self.data = data

    def split(self, bufsize: int = 1024):
        for i in range(len(self.data) // bufsize):
            yield self.data[i * bufsize, i * bufsize + bufsize]
        return self.data[len(self.data) // bufsize:]

    def _presend(self, bufsize: int = 1024):
        yield chr(self.mtype)
        yield from self.split(bufsize)
        yield b"\0" * 1024


class TextMessage(Message):
    def __init__(self, text=""):
        super().__init__(MessageType.T_TEXT, text.encode("utf-8"))

    def get_text(self):
        return self.data.decode("utf-8")

    def set_text(self, text):
        self.data = text.encode("utf-8")
