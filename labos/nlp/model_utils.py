import torch
from torch import nn

label_mapping = {
    0: "Meubles",
    1: "Électroménager",
    2: "Multimédia",
    3: "Exterieur",
    4: "Papeterie",
    5: "Téléphone",
    6: "Informatique",
    7: "Grande distribution",
    8: "Bricolage",
    9: "Culture",
    10: "Mode",
    11: "Sport",
    12: "Bébé",
    13: "Bien être",
    14: "Véhicule",
    15: "Jouets",
}


class PageClassifierMultiLabel(nn.Module):
    def __init__(self, input_features, output_features):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(in_features=input_features, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=output_features),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.linear_layer_stack(x)


class PageClassifier(nn.Module):
    def __init__(self, input_features, output_features):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(
                in_features=input_features, out_features=128, dtype=torch.float32
            ),
            nn.ReLU(),
            nn.Linear(
                in_features=128, out_features=output_features, dtype=torch.float32
            ),
        )

    def forward(self, x):
        return self.linear_layer_stack(x)


def predict(model, input: list[int]):
    model.eval()

    with torch.inference_mode():
        X = torch.tensor([input]).type(torch.float32)
        y_logits = model(X)
        y_softmax = torch.softmax(y_logits, dim=1)
        y_pred = y_softmax.argmax(dim=1)

        result = y_softmax.detach().numpy()
        prediction = y_pred.detach().numpy()[0]
        class_prediction = label_mapping[prediction]

        print("result", result)
        print("class_prediction =>", class_prediction)

    return int(prediction)


def predict_multi_class(model, input: list[int]) -> str:
    model.eval()

    with torch.inference_mode():
        X = torch.tensor([input]).type(torch.float32)
        y_logits = model(X)
        y_pred = torch.sigmoid(y_logits)

        result = ""
        for i in range(16):

            if y_pred[0][i] >= 0.5:
                result += "| " + label_mapping[i]

    return result


def predict_multi_class_raw(model, input: list[int]):
    model.eval()

    with torch.inference_mode():
        X = torch.tensor([input]).type(torch.float32)
        y_logits = model(X)
        y_pred = torch.sigmoid(y_logits)

        result = []
        for i in range(16):

            if y_pred[0][i] >= 0.5:
                result.append(i)

        if len(result) == 0:
            y_pred_bis = torch.softmax(y_logits, dim=1).argmax(dim=1)
            result = [int(y_pred_bis.detach().numpy()[0])]

    return result
