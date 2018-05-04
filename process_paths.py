import os
import re
import shutil

PATH = "e:\\2018_City\\03\\"

regexp = re.compile(r"(.*?)_(zaezd.*)")
files = os.listdir(PATH)

for file in files:
    match = regexp.match(file)
    if match:
        road_name = match[1].replace(" ", "_").capitalize()
        os.makedirs(os.path.join(PATH, road_name), exist_ok=True)
        # print(file, road_name, match[2])
        # shutil.move(os.path.join(PATH, file), os.path.join(PATH, road_name, match[2]))