import os
from datetime import datetime
from google.cloud import texttospeech

class GoogleTTS:
  def __init__(self,text_list,audio_file_name="test"):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.dir_path}/creds/service-account-file.json"
    self.text_list = text_list
    lang = "en-US"

    print("Saving post as audio file...")
    self.audio = []
    self.total_chars = 0
    for i,text in enumerate(self.text_list):
      self.total_chars += len(text)
      client = texttospeech.TextToSpeechClient()

      synthesis_input = texttospeech.SynthesisInput(text=text)
      voice = texttospeech.VoiceSelectionParams(language_code=lang,name=lang+"-Wavenet-G",ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
      audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)

      res = client.synthesize_speech(input=synthesis_input,voice=voice,audio_config=audio_config)
      self.audio.append(res.audio_content)

    self.save_audio_file(res_binary=self.audio,file_name=audio_file_name)
    self.save_char_count()

  def save_audio_file(self,res_binary,file_name):
    audio_file_path = f"{self.dir_path}/temp/{file_name}.opus"
    with open(audio_file_path, "wb") as audio_file:
      for binary in res_binary:
        audio_file.write(binary)

  def save_char_count(self):
    current_month = datetime.now().month
    info = None

    with open(f"{self.dir_path}/char_count.txt", "r") as f:
      txt = f.read()
      info = [int(n) for n in txt.split(",")]
      if info[0] != current_month:
        info = [current_month,0]
      info[1] += self.total_chars

    print(f"Month: {info[0]}, Char: {info[1]}")

    with open(f"{self.dir_path}/char_count.txt", "w") as f:
      info = [str(n) for n in info]
      f.write(",".join(info))
