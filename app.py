from flask import Flask, jsonify, render_template, send_file
import os
import json
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/version.json')
def get_version():
    try:
        with open('version.txt', 'r') as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = "1.0"  # Версия по умолчанию, если файл не найден
    
    version_data = {
        "version": version
    }
    return jsonify(version_data)

@app.route('/download/rclient.exe')
def download_rclient():
    # Путь к файлу Rclient
    file_path = os.path.join(app.root_path, 'static', 'DDNet.exe')
    return send_file(file_path, as_attachment=True)

@app.route('/history')
def history():
    folder = os.path.join(app.root_path, 'static', 'clients_history')
    versions = []
    for fname in os.listdir(folder):
        if fname.endswith('.exe'):
            # Извлекаем версию из имени файла, например DDNet-1.4.1.exe -> 1.4.1
            parts = fname.rsplit('-', 1)
            if len(parts) == 2 and parts[1].endswith('.exe'):
                version = parts[1][:-4]
            else:
                version = fname
            # Получаем дату изменения файла
            fpath = os.path.join(folder, fname)
            mtime = os.path.getmtime(fpath)
            date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            versions.append({
                'version': version,
                'date': date,
                'filename': fname
            })
    # Сортируем по версии или дате (по дате по убыванию)
    versions.sort(key=lambda v: v['date'], reverse=True)
    return render_template('history.html', versions=versions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084) 
