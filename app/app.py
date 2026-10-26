"""Local-only identity request preview. No directory operations or credentials."""

import re
import unicodedata

from flask import Flask, render_template, request

app = Flask(__name__)
app.config.update(
    MAX_CONTENT_LENGTH=4096,
    MAX_FORM_MEMORY_SIZE=4096,
    MAX_FORM_PARTS=8,
    TRUSTED_HOSTS=["localhost", "127.0.0.1", "[::1]"],
)


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


def valid_name(value):
    return (
        1 <= len(value) <= 80
        and any(char.isalpha() for char in value)
        and all(char.isalpha() or char in " '-" for char in value)
    )


def username_part(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_value.lower())


@app.route("/", methods=["GET", "POST"])
def criar_usuario():
    if request.method == "GET":
        return render_template("index.html")

    first = request.form.get("nome", "").strip()
    last = request.form.get("sobrenome", "").strip()
    employee_id = request.form.get("id_colaborador", "").strip()
    first_part, last_part = username_part(first), username_part(last)
    if (
        not valid_name(first)
        or not valid_name(last)
        or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", employee_id)
        or not first_part
        or not last_part
    ):
        return render_template("index.html", error="Enter valid demo names and an ID."), 400

    username = f"{first_part}.{last_part}"
    return render_template(
        "preview.html",
        first=first,
        last=last,
        employee_id=employee_id,
        username=username,
        email=f"{username}@example.invalid" if "criar_email" in request.form else None,
    )
