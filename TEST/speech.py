import speech_recognition as sr

# Recognizerを作成
r = sr.Recognizer()

# マイクから音声を取得
with sr.Microphone() as source:
    print("話してください...")
    r.adjust_for_ambient_noise(source)  # 雑音対策
    audio = r.listen(source)

# 音声をテキストに変換（日本語指定）
try:
    text = r.recognize_google(audio, language="ja-JP")
    print("認識結果:", text)
except sr.UnknownValueError:
    print("音声を認識できませんでした")
except sr.RequestError as e:
    print(f"Google Speech Recognition サービスに接続できません: {e}")
