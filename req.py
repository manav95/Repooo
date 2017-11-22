import requests

files = {'file': open('angryWhiteGuy.mp4', 'rb')}
r = requests.post('http://127.0.0.1:5500/vokaturiAnalysis', data={'video_filename': 'angryWhiteGuy.mp4', 'audio_filename': 'angryWhiteGuy.wav'}, files=files)
print(r)