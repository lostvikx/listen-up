import os
from google.cloud import texttospeech

class GoogleTTS:
  def __init__(self,text,audio_file_name="test"):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.dir_path}/creds/service-account-file.json"
    self.text = text
    lang = "en-US"

    print("Saving post as audio file...")
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=self.text)
    voice = texttospeech.VoiceSelectionParams(language_code=lang,name=lang+"-Wavenet-G",ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)

    res = client.synthesize_speech(input=synthesis_input,voice=voice,audio_config=audio_config)

    self.save_audio_file(res_binary=res.audio_content,file_name=audio_file_name)

  def save_audio_file(self,res_binary,file_name):
    audio_file_path = f"{self.dir_path}/temp/{file_name}.opus"
    with open(audio_file_path, "wb") as audio_file:
      audio_file.write(res_binary)
