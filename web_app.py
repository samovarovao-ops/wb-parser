import os
import io
import csv
from flask import Flask, render_template, request, send_file
from wb_parser import search_wildberries, extract_products, save_to_csv

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    query = ""
    error = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query:
            error = "Введите поисковый запрос"
        else:
            try:
                data = search_wildberries(query)
                products = extract_products(data)
            except Exception as e:
                error = f"Ошибка: {e}"

    return render_template("index.html", products=products, query=query, error=error)


@app.route("/download")
def download():
    query = request.args.get("query", "")
    if not query:
        return "Нет данных", 404

    try:
        data = search_wildberries(query)
        products = extract_products(data)
        if not products:
            return "Товары не найдены", 404
    except Exception:
        return "Ошибка при поиске", 500

    # Генерируем CSV в памяти
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "brand", "price", "rating", "reviews"])
    writer.writeheader()
    writer.writerows(products)
    output.seek(0)

    mem = io.BytesIO()
    mem.write(output.getvalue().encode("utf-8-sig"))
    mem.seek(0)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in query)
    return send_file(
        mem,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"wb_{safe_name}.csv"
    )


if __name__ == "__main__":
    print("Сервер запущен: http://localhost:8080")
    app.run(debug=True, host="0.0.0.0", port=8080)
