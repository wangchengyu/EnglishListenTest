import os
import time
import yaml
import sys
import random

from google.cloud import texttospeech

# module_path = os.path.dirname(__file__)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = module_path + "/*.json"
client = texttospeech.TextToSpeechClient()

ZH = "zh-CN"
EN = "en-GB"

def getAudioFromApi(msg, lang="zh-CN", audio_file=""):
    synthesis_input = texttospeech.SynthesisInput(text=msg)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang, 
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    if audio_file == "":
        audio_file = "./audio/" + msg + ".mp3"

    with open(audio_file, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "{0}"'.format(audio_file))
        
        
def say(msg, lang="zh-cn"):
    #os.system("say " + msg)
    
    audio_file = "./audio/" + msg + ".mp3"
               
    if not os.path.isfile(audio_file):
        getAudioFromApi(msg, lang, audio_file)
        
    print("play file: \"{0}\"".format(audio_file))
    os.system("play -q \"{0}\" ".format(audio_file))
    
def getDataFromYaml():
    file_name = "dict.yaml"
    stream = open(file_name, 'r')
    
    return yaml.safe_load(stream)


def getChapterSay(chapter):
    chapters = chapter.split("-")
    
    result = "小学" + chapters[0] + "年级"
    result += ["上学期", "下学期"][int(chapters[1])]
    result += "第" + chapters[2] + "模块"
    
    return result

    
def examine(chapter):
    # 数据
    data = getDataFromYaml()
    
    test = {}
    
    if chapter == "all":
        test = data
    else:
        test[chapter] = data[chapter]
            
    print(test)
    
    # 提示语
    say("现在开始听力考试", ZH)
    
    for chapter in test:
    
        say(getChapterSay(chapter), ZH)
        
        time.sleep(2)
        
        # 随机排序
        random.shuffle(test[chapter])

        for item in test[chapter]:
            item = item.split("|")
            
            w = item[0].strip()
            c = item[1].strip()
            
            say(w, EN)
            time.sleep(1)
            say(c, ZH)
            time.sleep(1)
            say(w, EN)
            time.sleep(1)

    time.sleep(1)
    say("听力考试结束") #，不及格没有饭吃")

if len(sys.argv) == 1:
    sys.argv.append("all")

if __name__ == "__main__":
    examine(sys.argv[1])