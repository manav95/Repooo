from flask import Flask, jsonify
from flask import request
from werkzeug import secure_filename
import os
import subprocess
from livereload import Server, shell
import ffmpy
from PIL import Image
import io
app = Flask(__name__)

@app.route("/vokaturiAnalysis", methods=['POST'])
def runVokaturi():
    if request.method == 'POST':
      directory = os.getcwd()
      vidData = request.files['file']
      os.remove(directory + '/audiodata/'+request.form['audio_filename'])
      vidFile = open(directory + '/videodata/'+secure_filename(request.form['video_filename']), 'wb')
      vidFile.writelines(vidData.readlines())
      vidFile.close()
      ff = ffmpy.FFmpeg(inputs={directory + '/videodata/'+secure_filename(request.form['video_filename']):None}, outputs={directory + '/audiodata/'+request.form['audio_filename']:'-ac 1'})
      ff.run()
      filname = directory + '/audiodata/' + secure_filename(request.form['audio_filename'])
      proc = subprocess.Popen("python " + directory + "/vokaturi/examples/measure_wav_mac.py " + filname, shell=True, stdout=subprocess.PIPE)
      script_response = proc.stdout.read()
      print(script_response)
      
      command="python video-framework/video_another_emotion.py -v "+'/videodata/'+secure_filename(request.form['video_filename'])
      print(command)
      os.system(command)
      command2="python video-framework/cluster_chinese.py -d " + os.getcwd() + "/video-framework/Results/Extracted_frames/Extracted_faces/"
      print(command2)
      os.system(command2)
      os.system("cp video-framework/face_emotion_data_analysis.py Results")
      print("Clustering Done")
      os.system("python3 video-framework/face_emotion_data_analysis.py")

      imageData = Image.open('plot.png')
      buffer = io.BytesIO(imageData)
      jsonDict = {"imageData": buffer, "script": script_response}
      print(buffer)
      
      return jsonify(jsonDict)


if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
    server.watch('/Views/*')
    app.run(debug=True)   