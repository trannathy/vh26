import pickle, numpy as np
import litserve as ls

class RandomForestAPI(ls.LitAPI):
    def setup(self, device):
        # load the model saved in above step during training
        with open("model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def decode_request(self, request):
        x = np.asarray(request["input"])
        x = np.expand_dims(x, 0)
        return x

    def predict(self, x):
        return self.model.predict(x)

    def encode_response(self, output):
        return {"class_idx": int(output)}

if __name__ == "__main__":
    api = RandomForestAPI()
    server = ls.LitServer(api)
    server.run(port=8000)