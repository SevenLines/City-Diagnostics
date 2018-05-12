import os
import re
import shutil

PATH = "e:\\2018_City\\05\\"

regexp = re.compile(r"(.*?)_(zaezd.*)")
files = os.listdir(PATH)


def main():
    for file in files:
        match = regexp.match(file)
        if match:
            road_name = match[1].replace(" ", "_").capitalize()
            os.makedirs(os.path.join(PATH, road_name), exist_ok=True)


if __name__ == '__main__':
    main()