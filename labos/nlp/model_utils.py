import torch
from torch import nn


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
    label_mapping = {
        0: "Meuble | Aménagement int | Décoration",
        1: "Électroménager  | Ustensiles",
        2: "Multimédia (son,TV)",
    }
    model.eval()

    with torch.inference_mode():
        X = torch.tensor([input]).type(torch.float32)
        y_logits = model(X)
        y_softmax = torch.softmax(y_logits, dim=1)
        y_pred = y_softmax.argmax(dim=1)

        result = y_softmax.detach().numpy()
        class_prediction = label_mapping[y_pred.detach().numpy()[0]]

        print("result", result)
        print("class_prediction =>", class_prediction)
