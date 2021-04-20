import random


def GetInt(minValue: int, maxValue: int) -> int:
    return random.randint(minValue, maxValue)


def GetBool() -> bool:
    return True if random.randint(0, 1) == 1 else False


def GetFloat(minValue: float, maxValue: float) -> float:
    return random.uniform(minValue, maxValue)


def ReduceInt(value, amount, minValue):
    return max(value - amount, minValue)


def RandomBoolArray(size):
    return [bool(random.getrandbits(1)) for _ in range(size)]
