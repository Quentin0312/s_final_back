# TODO: Delete

import torch
from torch import nn


class PageClassifierMultiLabel(nn.Module):
    def __init__(self, input_features, output_features):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(input_features, 128),
            nn.ReLU(),
            nn.Linear(128, output_features),
            nn.Sigmoid(),  # Sigmoid activation for multi-label classification
        )

    def forward(self, x):
        return self.linear_layer_stack(x)


def train_multi_label(model, criterion, optimizer, inputs, labels, epochs=100):
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item()}")


def predict_multi_label(model, input):
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
    model.eval()
    with torch.no_grad():
        X = torch.tensor([input]).type(torch.float32)
        outputs = model(X)
        probabilities = outputs.squeeze().numpy()
        predicted_classes = [
            label_mapping[i] for i, prob in enumerate(probabilities) if prob > 0.5
        ]  # Thresholding at 0.5 for binary classification
        print("Probabilities:", probabilities)
        print("Predicted classes:", predicted_classes)
    return predicted_classes


# Example usage
input_size = 20  # Example input size
output_size = 16  # Example number of classes
model_multi_label = PageClassifierMultiLabel(input_size, output_size)
criterion_multi_label = (
    nn.BCELoss()
)  # Binary Cross Entropy Loss for multi-label classification
optimizer_multi_label = torch.optim.SGD(model_multi_label.parameters(), lr=0.01)

# Example training data (you need to replace this with your actual data)
inputs = torch.randn(100, input_size)  # Example input tensor
labels = torch.randint(0, 2, (100, output_size)).float()  # Example labels (binary)
train_multi_label(
    model_multi_label, criterion_multi_label, optimizer_multi_label, inputs, labels
)

# Example prediction
# fmt: off
input_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]  # Example input data
# fmt: on
prediction_multi_label = predict_multi_label(model_multi_label, input_data)

print(prediction_multi_label)
