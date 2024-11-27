import json
import os.path
import sys
import time

import source_data


def create_json(lines, file):
    context = source_data.sample_event_list

    for i in range(len(lines)):
        if not lines[i].startswith("SpawnObject("):
            lines[i] = ""

    context.get('m_Event').append(source_data.sample_static_objects)

    i = 0
    for line in lines:
        if line.startswith("SpawnObject("):
            splited_line = line.split('"')
            context.get("m_Event")[0]["StaticObjects"].append(dict(source_data.sample_mapping_data))
            context.get("m_Event")[0]["StaticObjects"][i]["Classname"] = splited_line[1]
            context.get("m_Event")[0]["StaticObjects"][i]["Position"] = [round(float(i), 2) for i in splited_line[3].split()]
            context.get("m_Event")[0]["StaticObjects"][i]["Orientation"] = [round(float(i), 2) for i in splited_line[5].split()]
            i += 1

    with open(f"Target/{file}.json".replace(".txt", ""), "w", encoding="UTF-8") as json_file:
        json.dump(context, json_file, indent=4)


def reformat_files(files_list: list):
    for file in files_list:
        with open(f"Source/{file}", "r") as mapping_file:
            lines = mapping_file.readlines()
            create_json(lines, file)
    print("Success")
    time.sleep(3)


if __name__ == '__main__':
    if not os.path.exists("Source"):
        os.mkdir("Source")
    if not os.path.exists("Target"):
        os.mkdir("Target")

    source_files = os.listdir("Source")

    if len(source_files) == 0:
        print("Положите экспортированные файлы маппинга в папку Source и запустите повторно программу")
        time.sleep(3)
        sys.exit()
    else:
        reformat_files(source_files)


