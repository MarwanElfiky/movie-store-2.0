import os
from flask import Flask, render_template

app = Flask(__name__)


def read_web_files(folder_path=r"C:\Users\maroe\OneDrive\Desktop\NodeJS\WEB"):
    web_files_directory = folder_path
    web_files = os.listdir(web_files_directory)
    print(web_files)
    html_files = []
    css_files = []
    js_files = []
    for file in web_files:
        if file.endswith(".html"):
            html_files.append(file)
        if file.endswith(".css"):
            css_files.append(file)
        if file.endswith(".js"):
            js_files.append(file)

    print(html_files, css_files, js_files)
    return html_files, css_files, js_files


html, css, js = read_web_files()


@app.route("/")
def index():
    return render_template(html[-1])


if __name__ == '__main__':
    app.run(debug=True)

