from flask import Flask, render_template, redirect, url_for, request, session
import upnp_helper

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
    device = upnp_helper.get_device()
    media = upnp_helper.media(device=device)
    return render_template(
        template_name_or_list="home.html",
        type="media",
        media=media
    )

if __name__ == '__main__':
    app.run(debug=True)