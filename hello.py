from flask import Flask, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename, redirect

from Crossword import Crossword, read_dictionary, file_len

app = Flask(__name__)
cross = Crossword()
string_dictionary = None


def write_to_file(solved_array):
    f = open("solved1.txt", "w", encoding='utf8')
    for row in solved_array:
        for field in row:
            f.write(field)
        f.write('\n')
    f.close()


def fill_file_from_date(txt_file):
    with open(txt_file) as f:
        x = len(f.readline()) - 1
        y = file_len(txt_file)

        if 10 <= x <= 30:
            if 10 <= y <= 30:
                T = [["0"] * x for _ in range(y)]
    with open(txt_file) as f:
        index_i = 0
        for line in f:
            index_j = 0
            for sign in line:
                if sign != "\n":
                    T[index_i][index_j] = sign
                index_j += 1
            index_i += 1

    if 10 <= x <= 30:
        if 10 <= y <= 30:
            solved = [["0"] * x for _ in range(y)]
            cross.init_from_data(x, y, T, solved)


@app.route("/solve", methods=["POST", "GET"])
def solve():
    if request.method == "POST":
        cross.get_word_size_list_x()
        cross.get_word_size_list_y()
        t = cross.get_t()
        cross.solve_puzzle(string_dictionary, t, 0, 10)
        return render_template("solved.html", temp=cross.solved)
        return redirect(url_for("solved.html"))
    return render_template("solve.html")


@app.route("/solved", methods=["POST", "GET"])
def upload():
    write_to_file(cross.solved)
    return send_file("solved.txt", as_attachment=True)


@app.route("/", methods=["POST", "GET"])
def prep():
    if request.method == "POST":
        cross_file = request.files['crossword']
        cross_file.save(cross_file.filename)
        dict = request.files['dict']
        dict.save(dict.filename)
        dict_filename = secure_filename(dict.filename)
        cross_filename = secure_filename(cross_file.filename)
        if request.form['flag'] == "txt":
            cross.init_from_file(cross_filename)
        else:
            fill_file_from_date(cross_filename)
        global string_dictionary
        string_dictionary = read_dictionary(dict_filename)
        return redirect("solve")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
