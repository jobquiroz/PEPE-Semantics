from flask import Flask, request, jsonify
import os
from pathlib import Path
from pepe_semantics import config
from pepe_semantics.inference import InferenceModel
from pepe_semantics.model.index import GIFIndex

app = Flask(__name__)

_INDEX = GIFIndex.load(Path(config.INDEX_DIR))
#_INDEX = GIFIndex.load(Path('/app/src/pepe_semantics/index/pepe_index/'))

_MODEL = InferenceModel(Path(config.BERTWEET_WEIGHTS_PATHS[1]))
#_MODEL = InferenceModel(Path('/app/src/pepe_semantics/model/bertweet_weights.pth'))

def get_giphy_links(input_text, k = 5):
    """Get's giphy_id to the closest gif found"""
    text_emb = _MODEL.embed_text(input_text)
    return _INDEX.get_giphy_links(text_emb, k=k)

@app.route("/predict", methods=["POST"])
def predict():
    """Takes a POST request with a key of \"text\" and the text to be classified."""
    data_dict = request.get_json()
    text = data_dict["text"]
    return jsonify({"result": str(get_giphy_links(text, k = 5))})

@app.route("/")
def hello_world():
    return "Pepe semantics" # Continuous Deployment"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))