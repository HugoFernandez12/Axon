class Buffer:
    def __init__(self, size):
        self.storage = ""
        self.size = size

    @staticmethod
    def create_frame(text):
        text = chr(2) + text + chr(3)
        return text

    def add_frame(self, text):
        if (len(self.storage) + len(text)) <= self.size:
            self.storage = self.storage + text
        else:
            self.storage = ""

    def extract_frame(self):
        message = ""
        delete_control = 0

        for x in range(0, len(self.storage)):
            if self.storage[x] == chr(2):
                frame_control = x
                for y in range(frame_control + 1, len(self.storage)):
                    if self.storage[y] == chr(2):
                        frame_control = y
                    elif self.storage[y] == chr(3):
                        delete_control = y
                        for z in range(frame_control + 1, y):
                            message = message + self.storage[z]
                        break
                break

        if delete_control != 0:
            self.storage = self.storage[delete_control + 1:len(self.storage)]

        return message
