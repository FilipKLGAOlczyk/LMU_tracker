# -*- coding: utf-8 -*-
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
    # Zamieniamy na int, aby pozbyć się ułamków przed formatowaniem
    seconds_int = int(seconds % 60) 
    milliseconds = int(round((seconds % 1) * 1000))
    # Teraz zadziała poprawny format: "Minuty:Sekundy:Milisekundy"
    return f"{minutes}:{seconds_int:02d}:{milliseconds:03d}"

def save_player_data_to_json(driver, track, car, best_average_five):
    formatted_time = format_time_to_string(best_average_five)
    
    # 1. Nazywamy to new_record, żeby nie pomieszać z całą bazą
    new_record = {
        'name': driver,  # Zmieniłem na 'name', bo tak masz w React w pliku leaderboard.jsx
        'track': track,
        'car': car,
        'avg_five': formatted_time # Zmieniłem na 'avg_five', bo tak masz w Reaccie
    }

    # Główna struktura bazy
    data = {"player_data": []}
    
    # 2. Sprawdzamy, czy plik ISTNIEJE (bez 'not')
    if os.path.exists(JSON_FILEPATH):
        with open(JSON_FILEPATH, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                pass
    
    # Dodajemy nowy rekord do bazy
    data["player_data"].append(new_record)

    with open(JSON_FILEPATH, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Zapisano dane do pliku JSON: {JSON_FILEPATH}")

def track_game_data():
    global current_lap_number, is_current_lap_valid, best_average_five
    
    print("Oczekiwanie na uruchomienie Le Mans Ultimate...")
    
    try:
        sim_info = api.SimInfo() # Poprawione wywołanie klasy z pliku lmu_data.py
        print("Połączono z telemetrią LMU!")
    except FileNotFoundError:
        print("Nie wykryto włączonej gry. Uruchom skrypt, gdy gra będzie działać.")
        return

    while True:
        try:
            telemetry = sim_info.LMUData.telemetry
            scoring = sim_info.LMUData.scoring
            
            player_idx = telemetry.playerVehicleIdx
            
            if not telemetry.playerHasVehicle:
                time.sleep(1)
                continue

            player_telem = telemetry.telemInfo[player_idx]
            player_scoring = scoring.vehScoringInfo[player_idx]

            if player_telem.mLapInvalidated or player_scoring.mInPits:
                is_current_lap_valid = False

            laps_completed = player_scoring.mTotalLaps
            
            if laps_completed > current_lap_number:
                last_lap_time = player_scoring.mLastLapTime
                
                if current_lap_number > 0 and last_lap_time > 0:
                    if is_current_lap_valid:
                        print(f"Czyste okrążenie: {last_lap_time:.3f} s")
                        driver_name = player_scoring.mDriverName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        car_name = player_scoring.mVehicleName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        track_name = scoring.scoringInfo.mTrackName.decode('windows-1252', errors='ignore').split('\x00')[0]
                        
                        # 3. Uporządkowana kolejność wysyłania argumentów
                        process_new_lap(last_lap_time, driver_name, track_name, car_name)
                    else:
                        print(f"Okrążenie nieważne: {last_lap_time:.3f} s. Reset serii.")
                        last_lap_times.clear()
                
                current_lap_number = laps_completed
                is_current_lap_valid = True
                
        except Exception:
            pass
            
        time.sleep(0.05)

# Odbiera parametry w tej samej kolejności, w której zostały wysłane
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