import torch
from torch import nn
from torch.utils.data import DataLoader
from lib.torch_models.dataset import Data
import numpy as np
import os

from lib.models_wrapper import ModelsWrapper

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Model(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out


class ModelDropout(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(ModelDropout, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out


class MultiClassClassifier(ModelsWrapper):
    def __init__(self, input_size=10, hidden_size=60, output_size=1):
        super().__init__()
        self.model = ModelDropout(input_size, hidden_size, output_size)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.model_state = 0

    def create_loader(self, input, label, batch_size=16, shuffle=True, num_workers=0):
        dataset = Data(input, label)
        train_loader = DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=shuffle,
                                  num_workers=num_workers)
        return train_loader

    def train(self, input, label, learning_rate=0.001, num_epoch=1000, batch_size=16):
        train_loader = self.create_loader(input, label, batch_size=batch_size)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = torch.nn.CrossEntropyLoss()
        loss = []
        for epoch in range(num_epoch):
            for X, Y in train_loader:
                # Forward pass
                optimizer.zero_grad()
                output = self.model(X)
                loss = criterion(output, Y)

                # Backward pass and optimization
                loss.backward()
                optimizer.step()
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{num_epoch}], Loss: {loss.item():.10f}')

        print(f'final losses: {loss.item():.4f}')

        self.save('multiclass_classification_model')

    def save(self, filename):
        path = os.path.join(os.path.dirname(os.getcwd()), os.path.join("models", f'{filename}.pth'))

        data = {
            "model_state": self.model.state_dict(),
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
        }
        torch.save(data, path)
        print(f'model saved at: {path}')

    def load(self, filename):
        path = os.path.join(os.path.dirname(os.getcwd()), os.path.join("models", f'{filename}.pth'))
        data = torch.load(path)

        self.input_size = data["input_size"]
        self.hidden_size = data["hidden_size"]
        self.output_size = data["output_size"]
        self.model_state = data["model_state"]

        self.model = Model(self.input_size, self.hidden_size, self.output_size)
        self.model.load_state_dict(self.model_state)

        print("model loaded from", path)

    def predict(self, emb):
        array = np.array(emb)
        output = self.model(torch.from_numpy(array))
        _, predicted = torch.max(output.data, 1)
        label = predicted.item()
        prob = output[0][predicted.item()].item()
        return {'label': label, 'prob': prob}
