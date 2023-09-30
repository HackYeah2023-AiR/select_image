from flask import Flask, request, jsonify
import utils

app = Flask(__name__)


@app.route("/select_image", methods=["POST"])
def process_data():
    try:
        data = request.get_json()
        input_image_id = data.get("WildAnimalId")

        if input_image_id is None:
            return (
                jsonify({"error": f"Invaild input data - {input_image_id}"}),
                400,
            )

        result = utils.process_images(input_image_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
