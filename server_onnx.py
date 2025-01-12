import numpy as np
from fastapi import FastAPI
from onnxruntime import SessionOptions, GraphOptimizationLevel, InferenceSession
from transformers import AutoTokenizer, BatchEncoding, TensorType

app = FastAPI()
options = SessionOptions()
options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL
model = InferenceSession("./onnx_models/model-optimized.onnx", options, providers=["CUDAExecutionProvider"])
tokenizer = AutoTokenizer.from_pretrained("philschmid/MiniLM-L6-H384-uncased-sst2")


@app.get("/predict")
def predict(query: str):
    encode_dict: BatchEncoding = tokenizer(
        text=query,
        max_length=128,
        truncation=True,
        return_token_type_ids=False,
        return_tensors=TensorType.NUMPY,
    )
    result: np.ndarray = model.run(None, dict(encode_dict))[0]
    return result.tolist()
