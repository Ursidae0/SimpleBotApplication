import numpy as np
from Constants import STEP_LENGTH,MULTIPLIER

def getValues() -> np.ndarray:
    valueArray = np.zeros(STEP_LENGTH)
    valueArray[0] = 10
    valueArray = valueArray[0] * MULTIPLIER ** np.arange(STEP_LENGTH)
    roundData(valueArray)
    return valueArray

def roundData(data: np.ndarray):
    data[:] = np.floor(data)