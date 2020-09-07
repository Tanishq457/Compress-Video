import sys, os, shutil
from os.path import basename

import smtplib


from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import filetype

from compress import combineFramesAndSaveVideo, compressFrames


def send_mail(
    send_from, send_to, subject, text, files=None, server="smtp.gmail.com:587"
):
    msg = MIMEMultipart()
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    username = 'new.user.19283'
    password = os.environ.get('PASSWORD', None)
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.send_message(msg=msg, from_addr=send_from, to_addrs=send_to)
    # server.sendmail(send_from, send_to, msg)
    server.quit()


app = Flask(__name__)

UPLOAD_FOLDER = "."
SENDER_EMAIL = "new.user.19283@gmail.com"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

'''Home Page of Application'''
@app.route("/")
def upload_file():
    return render_template("home.html")


'''Upload point of Application'''
@app.route("/upload", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":

        if "file" not in request.files:
            return "No file part"
        f = request.files["file"]
        if f.filename == "":
            return "No selected file"

        ratio = int(request.form['ratio'])
        print('The ratio is: ' + str(ratio), file=sys.stderr)
        print('The ratio is: ' + str(request.form), file=sys.stderr)
        
        if(type(int(ratio)) != type(1) or int(ratio) not in range(1,100)):
            print('Error: Invalid ratio given', file=sys.stderr)
            return 'Error: Invalid ratio given'
        
        TO_EMAIL = request.form['name']

        fileName = secure_filename(f.filename)

        f.save(fileName)
        if not filetype.video_match("./" + fileName):
            print('Error: Not a video file', file=sys.stderr)
            return "Given file is not a video file. Please give a video file."
        output = compressFrames(fileName, ratio)
        print("output: " + str(output), file=sys.stderr)
        if output is None:
            shutil.rmtree("./temp")
            print('Error: Output is None', file=sys.stderr)
            return "Error"
        width, height, fps = output
        fileName2 = combineFramesAndSaveVideo(fileName, width, height, fps)

        send_mail(SENDER_EMAIL, TO_EMAIL, f"Compressed Video by {ratio}", "Here is the video", [fileName2])
        os.remove(fileName)
        os.remove(fileName2)
        return "File Emailed Successfully"
    return "No File/Email given"


if __name__ == "__main__":
    app.run(port=4000, threaded=True, debug=True)
