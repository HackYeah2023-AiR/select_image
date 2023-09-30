from flask import Flask, request, jsonify
from yolomain import select_image

app = Flask(__name__)


# Endpoint do przetwarzania danych z żądania GET
@app.route("/select_image", methods=["POST"])
def process_data():
    try:
        data = request.get_json()
        input_image_name = data.get("InputImageName")

        if input_image_name is None:
            return (
                jsonify({"error": f"Invaild input data - {input_image_name}"}),
                400,
            )

        result = select_image(input_image_name)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
