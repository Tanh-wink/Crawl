import os
from tqdm import tqdm

work_dir = os.getcwd()
project_dir = os.path.split(work_dir)[0]


def get_data():
    idioms = []
    with open(project_dir + "/data/hydcd_idioms.txt", "r", encoding="utf-8") as fin:
        for line in fin.readlines():
            idioms.append(eval(line.strip()))
    return idioms


def synonym_process(idiom):
    if idiom.get("近义词", 0) != 0:
        synonym = idiom.get("近义词").strip()
        if synonym == "":
            synonyms = []
        else:
            synonyms = synonym.split("、")
    else:
        synonyms = []
    return synonyms


def antonym_process(idiom):
    if idiom.get("反义词", 0) != 0:
        antonym = idiom.get("反义词").strip()
        if antonym == "":
            antonyms = []
        else:
            antonyms = antonym.split("、")
    else:
        antonyms = []
    return antonyms


def story_process(idiom):
    if idiom.get("故事", 0) != 0:
        story = idiom.get("故事").strip()
    else:
        story = ""
    return story


def english_process(idiom):
    if idiom.get("英文", 0) != 0:
        english = idiom.get("英文").strip()
    else:
        english = ""
    return english

def idiom_clean(idioms):
    new_data = []
    tk = tqdm(idioms)
    for cur in tk:
        try:
            idiom = cur["成语"].split(" ")[0]
            meaning = cur["解释"].strip()
            pinyin = " ".join([item for item in cur["拼音"].split(" ") if item != "" ])
            source = cur["出处"].strip()
            example = cur["举例造句"].strip()
            synonym = synonym_process(cur)
            antonym = antonym_process(cur)
            story = story_process(cur)
            english = english_process(cur)

            new_data.append({
                "idiom": idiom,
                "pinyin": pinyin,
                "meaning": meaning,
                "source": source,
                "example": example,
                "synonym": synonym,
                "antonym": antonym,
                "story": story,
                "english": english
            })
        except:
            print()
    return new_data


if __name__ == '__main__':
    idioms = get_data()

    print(len(idioms))
    idioms = idiom_clean(idioms)
    with open(project_dir + "/data/hydcd_idioms_clean.txt", "w", encoding="utf-8") as fout:
        for idiom in idioms:
            fout.write(str(idiom) + "\n")
