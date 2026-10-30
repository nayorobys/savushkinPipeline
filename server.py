import os
import re
import time

input_filename = os.path.join("Right_2", "result_codes.log")
output_filenames = [
    os.path.join("Right_2", "column_1_codes.txt"),
    os.path.join("Right_2", "column_2_codes.txt"),
    os.path.join("Right_2", "column_3_codes.txt"),
    os.path.join("Right_2", "column_4_codes.txt")
]

def process_log_file():
    columns_data = [[], [], [], []]
    
    if not os.path.exists(input_filename):
        return

    # Читаем исходный лог
    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            if '|' in line:
                line_clean = line.split('|')[0]
            else:
                line_clean = line
            
            line_clean = re.sub(r'<0x[0-9A-Fa-f]+>', '', line_clean).strip()
            
            if '?' in line_clean:
                parts = line_clean.split('?')
                
                if len(parts) == 4:
                    for i in range(4):
                        columns_data[i].append(parts[i].strip())
                        
    for i in range(4):
        with open(output_filenames[i], "w", encoding="utf-8") as out_file:
            out_file.write("\n".join(columns_data[i]) + "\n")
            
    print("Изменения ДОБ")

if __name__ == "__main__":
    last_mtime = None
    
    try:
        while True:
            if os.path.exists(input_filename):
                current_mtime = os.path.getmtime(input_filename)
                
                if last_mtime is None or current_mtime != last_mtime:
                    process_log_file()
                    last_mtime = current_mtime
            else:
                print(f"Ожидание появления файла", end="\r")
                last_mtime = None
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nКонец")