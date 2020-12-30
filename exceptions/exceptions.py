class ShipNotFoundError(Exception):
    pass


class SGPError(Exception):
    pass


class PacketFormatError(SGPError):
    pass


class PacketTimingError(SGPError):
    pass


class ReceiveInterruptedError(SGPError):
    pass


class ReceiveTimedOutError(SGPError):
    pass
