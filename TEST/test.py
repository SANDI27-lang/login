import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import sys

# 音声認識（成功ならテキスト、失敗なら None を返す）
def recognize_speech(language="ja-JP"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("話してください...")
        # 環境ノイズの校正（短めに）
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # 無音が続いたら抜けるための timeout / 上限の phrase_time_limit を付与
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("音声入力が検出できませんでした（タイムアウト）")
            return None

    try:
        command = recognizer.recognize_google(audio, language=language)
        print("認識結果:", command)
        return command
    except sr.UnknownValueError:
        print("音声を認識できませんでした")
        return None
    except sr.RequestError as e:
        print(f"Google Speech Recognition サービスに接続できません: {e}")
        return None

def speak(text, lang="ja"):
    tts = gTTS(text=text, lang=lang)
    # 一時MP3に保存（Windows対策で close してから使う）
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    try:
        tts.save(temp_audio.name)
    finally:
        temp_audio.close()

    # pydub で再生（※ ffmpeg が必要）
    audio = AudioSegment.from_mp3(temp_audio.name)
    play(audio)

    # 後始末
    os.remove(temp_audio.name)

if __name__ == "__main__":
    print("音声アシスタントを開始します。（Ctrl+C で終了）")
    try:
        while True:
            command = recognize_speech(language="ja-JP")

            # 失敗（None）のときは次のループへ
            if not command:
                continue

            # 日本語は lower() の効果が薄いが、英字混在に備えて一応
            cmd = command.lower()

            if "こんにちは" in cmd:
                speak("こんにちは！何をしますか？", lang="ja")
            elif any(key in cmd for key in ["おなまえは", "お名前は", "あなたの名前"]):
                # 英語を混ぜたい場合は lang="en" に変える
                speak("私はあなたのボイスアシスタントです。", lang="ja")
            elif "終了" in cmd or "しゅうりょう" in cmd or "おわり" in cmd:
                speak("さようなら。", lang="ja")
                break
            else:
                # わからなかったときのフォールバック
                speak("すみません。もう一度お願いします。", lang="ja")

    except KeyboardInterrupt:
        print("\n終了します。")
        sys.exit(0)
