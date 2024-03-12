from flask import Flask, render_template, redirect, url_for, request, session, Response
import upnp_helper
import subprocess

app = Flask(__name__)
app.secret_key = "Karuppasamy22"

@app.route('/')
def home():
    return render_template(
        template_name_or_list="home.html",
        type="home"
    )

@app.route('/search_devices/')
def search_devices():
    devices = upnp_helper.discover()
    return render_template(
        template_name_or_list="home.html",
        type="search_devices",
        devices=devices
    )

@app.route('/select_media/')
def select_media():
    device_address = request.args.get('device_address')
    device_response = request.args.get('device_response')
    session["device_address"] = device_address
    session["device_response"] = device_response
    return redirect(url_for('media'))

@app.route('/media/')
def media():
    id = request.args.get("id")
    device = upnp_helper.get_device()
    media = upnp_helper.media(device,id)
    return render_template(
        template_name_or_list="home.html",
        type="media",
        media=media
    )

@app.route('/stream_video/')
def stream_video():
    # Use requests library to get the MKV file stream
    mkv_url = request.args.get("mkv_url")
    ffmpeg_command = [
        'ffmpeg',
        '-i', mkv_url,
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov',
        '-vcodec', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-vsync', 'vfr',
        # '-an',  # Disable audio
        'pipe:1'  # Output to stdout
    ]

    # Start FFmpeg process
    subprocess.Popen(["vlc",mkv_url])
    # Create a response with the generator function
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)