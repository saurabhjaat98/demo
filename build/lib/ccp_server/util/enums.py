from enum import Enum


class Status(int, Enum):
    ACTIVE = 1
    INACTIVE = 0
    DELETED = -1


class Disk_Config(str, Enum):
    MANUAL = 'MANUAL'
    AUTO = 'AUTO'


class InstanceActionEnum(str, Enum):
    STOP = 'STOP'
    START = 'START'
    REBOOT = 'REBOOT'
    REBUILD = 'REBUILD'
    RESIZE = 'RESIZE'
    RESUME = 'RESUME'
    PAUSE = 'PAUSE'
    UNPAUSE = 'UNPAUSE'


class InstanceRebootType(str, Enum):
    SOFT = 'SOFT'
    HARD = 'HARD'


class VolumeActionEnum(str, Enum):
    ATTACH = 'ATTACH'
    DETACH = 'DETACH'
