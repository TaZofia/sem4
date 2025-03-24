import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import confusion_matrix
import numpy as np
import cv2
import os
from PIL import Image

transform = transforms.Compose([
    transforms.ToTensor(),  
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja z średnią 0.5 i odchyleniem standardowym 0.5
])

train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

current_folder = os.getcwd()
root_dir = os.path.join(current_folder, "lista1\\numbers")


class CustomMNISTDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        :param root_dir: Ścieżka do głównego folderu z danymi.
        :param transform: Opcjonalne transformacje (np. normalizacja, zmiana rozmiaru)
        """
        self.root_dir = root_dir
        self.transform = transform
        self.img_paths = []
        self.labels = []
        
        # Ładowanie obrazów i etykiet
        for label in range(10):  # Cyfry od 0 do 9
            label_dir = os.path.join(root_dir, str(label))
            for img_name in os.listdir(label_dir):
                if img_name.endswith(".jpg"): 
                    img_path = os.path.join(label_dir, img_name)
                    self.img_paths.append(img_path)
                    self.labels.append(label)

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        label = self.labels[idx]
        
        # Wczytanie obrazu
        image = Image.open(img_path).convert("L")  # Przekonwertuj do skali szarości (L)
        
        # Zastosowanie transformacji, jeśli są podane
        if self.transform:
            image = self.transform(image)
        
        # Zwracamy obraz oraz etykietę
        return image, label



dataset = CustomMNISTDataset(root_dir=root_dir, transform=transform)

dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Sprawdzanie pierwszego batcha
for images, labels in dataloader:
    print(images.shape)  # Tensor z obrazami
    print(labels)        # Tensor z etykietami
    break

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Warstwa wejściowa - ukryta (784 wejścia -> 128 neuronów)
        self.fc1 = nn.Linear(28*28, 128)
        # Warstwa ukryta - wyjście (128 neuronów -> 10 cyfr (klas))
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Aktywacja ReLU
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


model = SimpleNN()

# Funkcja kosztu
criterion = nn.CrossEntropyLoss()

# Aktualizowanie wag i bias żeby zmniejszyć funkcję kosztu
optimizer = optim.SGD(model.parameters(), lr=0.01)

epochs = 5 

for epoch in range(epochs):
    model.train()  # Tryb treningowy
    running_loss = 0.0

    # Pętla po partiach
    for images, labels in train_loader:

        images = images.view(-1, 28*28) # Obraz przekształcamy na wektor
        
        optimizer.zero_grad()    # Zerowanie gradientów, w PyTorch się kumulują
        outputs = model(images)
        
        
        loss = criterion(outputs, labels)    # Obliczanie straty - porównanie przewidywań z rzeczywistymi etykietami
        loss.backward()                      # Backpropagation
        
        # Optymalizacja
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f"Epoka {epoch+1}/{epochs}, Strata: {running_loss/len(train_loader)}")    # Straty na epokę

# Testowanie modelu
model.eval()  # tryb testowy

pred = []
real_labels = []

with torch.no_grad():  # Wyłączenie obliczania gradientów
    for images, labels in dataloader:
        images = images.view(-1, 28*28)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        pred.append(predicted)
        real_labels.append(labels)


# Zmieniamy listy na tensor
pred = torch.cat(pred, dim=0)
real_labels = torch.cat(real_labels, dim=0)

print("---Prawdziwe: ", real_labels)
print("Przewidziane: ", pred)