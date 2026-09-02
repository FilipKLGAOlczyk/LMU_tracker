import time

import json
import os

from tracker_api.pyLMUSharedMemory import lmu_data as api

JSON_FILEPATH = './data/player_data.json'

last_lap_times = []
best_average_five = None

current_lap_number = 0
is_current_lap_valid = True

def format_time_to_string(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    milliseconds = int(round(seconds % 1 * 1000))
    return f"{minutes}:{seconds:.3f}.{milliseconds:03d}"

def save_player_data_to_json(driver,track,car,best_average_five):
    formatted_time = format_time_to_string(best_average_five)
    data = {
        'driver': driver,
        'track': track,
        'car': car,
        'best_average_five': formatted_time
    }

    data={"player_data": []}
    if not os.path.exists(JSON_FILEPATH):
        with open(JSON_FILEPATH, 'r', encoding = 'utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                pass
    
    data["player_data"].append(data)

    with open(JSON_FILEPATH, 'w', encoding = 'utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Zapisano dane do pliku JSON: {JSON_FILEPATH}")

def track_game_data():
    global current_lap_number, is_current_lap_valid, best_average_five
    
    print("Oczekiwanie na uruchomienie Le Mans Ultimate...")
    
    # Inicjalizacja połączenia z pamięcią gry
    try:
        sim_info = api.LMUData.SimInfo()
        print("Połączono z telemetrią LMU!")
    except FileNotFoundError:
        print("Nie wykryto włączonej gry. Uruchom skrypt, gdy gra będzie działać.")
        return

    while True:
        try:
            # Pobranie głównych bloków danych
            telemetry = sim_info.LMUData.telemetry
            scoring = sim_info.LMUData.scoring
            
            # Pobranie indeksu gracza, aby wyciągnąć dane jego auta, a nie AI
            player_idx = telemetry.playerVehicleIdx
            
            if not telemetry.playerHasVehicle:
                time.sleep(1)
                continue

            # Konkretne dane naszego pojazdu
            player_telem = telemetry.telemInfo[player_idx]
            player_scoring = scoring.vehScoringInfo[player_idx]

            # 1. Śledzenie limitów toru NA BIEŻĄCO
            # Jeśli w dowolnym momencie okrążenia flaga zmieni się na True lub gracz zjedzie do pitu
            if player_telem.mLapInvalidated or player_scoring.mInPits:
                is_current_lap_valid = False

            # 2. Wykrywanie momentu przejechania linii mety
            laps_completed = player_scoring.mTotalLaps
            
            if laps_completed > current_lap_number:
                last_lap_time = player_scoring.mLastLapTime
                
                # Ignorujemy pierwsze wyjazdowe okrążenie
                if current_lap_number > 0 and last_lap_time > 0:
                    if is_current_lap_valid:
                        print(f"Czyste okrążenie: {last_lap_time:.3f} s")
                        driver_name = player_scoring.mDriverName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        car_name = player_scoring.mVehicleName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        track_name = scoring.scoringInfo.mTrackName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        process_new_lap(driver_name, track_name, car_name, last_lap_time)
                    else:
                        print(f"Okrążenie nieważne: {last_lap_time:.3f} s. Reset serii.")
                        last_lap_times.clear()
                
                # Przygotowanie zmiennych na nowe okrążenie
                current_lap_number = laps_completed
                is_current_lap_valid = True
                
        except Exception as e:
            pass # Gra mogła zostać wyłączona lub ładuje się tor
            
        # Sprawdzamy dane 20 razy na sekundę, żeby nie przegapić ułamka sekundy, gdy flaga track limits miga
        time.sleep(0.05)

def process_new_lap(lap_time, driver_name, track_name, car_name):
    global best_average_five
    
    last_lap_times.append(lap_time)
    
    if len(last_lap_times) > 5:
        last_lap_times.pop(0)

    if len(last_lap_times) == 5:
        average_five = sum(last_lap_times) / 5.0
        print(f"Średnia z 5 ostatnich kółek: {average_five:.3f} s")
        
        if best_average_five is None or average_five < best_average_five:
            best_average_five = average_five
            print(f"NOWY REKORD ŚREDNIEJ: {best_average_five:.3f} s!")
            save_player_data_to_json(driver_name, track_name, car_name, best_average_five)

if __name__ == "__main__":
    track_game_data()
