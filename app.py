from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# 質問読み込み
with open("questions.json", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/")
def index():
    return redirect(url_for("question", qid="start"))

@app.route("/question/<qid>", methods=["GET", "POST"])
def question(qid):
    if request.method == "POST":
        next_qid = request.form.get("next")
        return redirect(url_for("question", qid=next_qid))

    current = questions.get(qid)

    if not current:
        return "質問が見つかりません", 404

    if "result" in current:
        # resultが指定された場合はテンプレートへメッセージを渡す
        result_message = current["result"]
        return render_template("result.html", result_message=result_message)

    return render_template("question.html", qid=qid, question=current["question"], options=current["options"])

if __name__ == "__main__":
    app.run(debug=True)
