import pandas as pd
from datetime import datetime

def Depression_judgment(depression_log):
    all_score = 0

    # Summation
    for score in depression_log:
        all_score += score

    # Average
    all_score /= 3

    # Decision
    if all_score > 4.5:
        return 3
    elif all_score > 3.5:
        return 2
    else:
        return 1