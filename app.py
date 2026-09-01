import time

from tracker_api.pyLMUSharedMemory import lmu_data as api

last_lap_times = []
best_average_five = None

def check_connection():
    while True:
        time.sleep(1)


def get_last_lap_time():
    if(api.mLapInvalidated or api.mLapTime == 0):
        return None
    else:
        return api.mLastLapTime

def update_lap_times():
    last_lap_time = get_last_lap_time()
    if last_lap_time is not None:
        if len(last_lap_times) >= 5:
            last_lap_times.pop(0)
        last_lap_times.append(last_lap_time)

def avg_five_laps():
    if len(last_lap_times) == 0:
        return None
    average_five = sum(last_lap_times[-5:]) / min(len(last_lap_times), 5)
    if best_average_five is None or average_five < best_average_five:
        best_average_five = average_five
    return average_five
