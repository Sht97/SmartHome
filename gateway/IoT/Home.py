import ExternalComm
import InternalComm


class Home:
    def __init__(self):
        print("New Home created")
        self.lookout = False
        self.flag = True
        self.light = False

    def toggle_lookout(self):
        self.lookout = not self.lookout
        print("new lookout state to " + format(self.lookout))
        ExternalComm.ExternalComm.send_status(format(self.lookout))
        if self.lookout:
            InternalComm.ThingsComm.send_conf("pir_conf", "1")
        else:
            InternalComm.ThingsComm.send_conf("pir_conf", "0")
        return self.lookout

    def toggle_light(self):
        self.light = not self.light
        print("new light state to " + format(self.light))
        ExternalComm.ExternalComm.send_light(format(self.light))
        if self.light:
            InternalComm.ThingsComm.send_conf("light", "1")
        else:
            InternalComm.ThingsComm.send_conf("light", "0")
        return self.light

    def get_lookout(self):
        return self.lookout

    def get_light(self):
        return self.light

    def end_program(self):
        self.flag = False

    def is_ended(self):
        return self.flag
