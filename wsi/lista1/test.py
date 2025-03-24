import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import confusion_matrix
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

# Przekształcenia danych
transform = transforms.Compose([
    transforms.ToTensor(),  
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja z średnią 0.5 i odchyleniem standardowym 0.5
])

# Ładowanie danych MNIST
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# Dane ładowane w partiach po 64
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# Definicja prostej sieci neuronowej
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

# Inicjalizacja modelu
model = SimpleNN()

# Funkcja kosztu
criterion = nn.CrossEntropyLoss()

# Optymalizator
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Trening modelu
epochs = 5
for epoch in range(epochs):
    model.train()  # Tryb treningowy
    running_loss = 0.0

    # Pętla po partiach
    for images, labels in train_loader:
        images = images.view(-1, 28*28)  # Obraz przekształcamy na wektor
        optimizer.zero_grad()  # Zerowanie gradientów
        outputs = model(images)  # Predykcje
        loss = criterion(outputs, labels)  # Obliczanie straty
        loss.backward()  # Backpropagation
        optimizer.step()  # Optymalizacja
        running_loss += loss.item()

    print(f"Epoka {epoch+1}/{epochs}, Strata: {running_loss/len(train_loader)}")  # Straty na epokę

# Klasa Dataset do ładowania własnych próbek pisma
class MyDataset(Dataset):
    def __init__(self, img_folder, transform=None):
        self.img_folder = img_folder
        self.transform = transform
        self.image_paths = []
        self.labels = []

        # Załaduj obrazy i przypisz etykiety na podstawie nazwy folderu
        for label in range(10):  # Cyfry od 0 do 9
            digit_folder = os.path.join(img_folder, str(label))  # Katalog z cyfry
            if os.path.exists(digit_folder):
                for filename in os.listdir(digit_folder):
                    if filename.endswith(".jpg"):  # Sprawdzamy tylko pliki .jpg
                        self.image_paths.append(os.path.join(digit_folder, filename))
                        self.labels.append(label)  # Etykieta na podstawie folderu (0-9)
            else:
                print(f"Brak folderu: {digit_folder}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(img_path).convert('L')  # Wczytujemy jako szaro-skalowy obraz

        if self.transform:
            image = self.transform(image)

        return image, label


# Przekształcenia dla własnych próbek
my_samples_transform = transforms.Compose([
    transforms.Resize((28, 28)),  # Przeskaluj obraz do rozmiaru 28x28
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja
])

current_folder = os.getcwd()
img_folder = os.path.join(current_folder, "lista1\\numbers")
# Wczytanie własnych próbek
my_samples_dataset = MyDataset(img_folder, transform=my_samples_transform)
my_samples_loader = DataLoader(my_samples_dataset, batch_size=1, shuffle=False)

# Testowanie modelu na własnych próbkach
model.eval()  # Tryb testowy
correct = 0
total = 0

y_true = []
y_pred = []

with torch.no_grad():
    for images, labels in my_samples_loader:
        outputs = model(images.view(-1, 28*28))  # Przekształcamy obraz na wektor
        _, predicted = torch.max(outputs, 1)  # Wybór klasy z najwyższym prawdopodobieństwem
        
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        y_true.extend(labels.cpu().numpy())
        y_pred.extend(predicted.cpu().numpy())

# Obliczanie dokładności
#accuracy = 100 * correct / total
#print(f"Dokładność na własnych próbkach: {accuracy}%")

print("----------Prawdziwe cyfry dla obrazów:", y_true)
# Wyświetlanie przewidywanych etykiet
print("Przewidywane cyfry dla Twoich obrazów:", y_pred)

