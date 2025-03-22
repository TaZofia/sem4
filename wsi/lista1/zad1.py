import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

transform = transforms.Compose([
    transforms.ToTensor(),  # Przekształcenie obrazu na tensor
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja z średnią 0.5 i odchyleniem standardowym 0.5
])

# Pobranie danych treningowych
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
# Pobranie danych testowych
test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# Definiowanie sieci neuronowej
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Warstwa wejściowa -> ukryta (784 wejścia -> 128 neuronów)
        self.fc1 = nn.Linear(28*28, 128)
        # Warstwa ukryta -> wyjście (128 neuronów -> 10 klas)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Funkcja aktywacji ReLU
        x = torch.relu(self.fc1(x))
        # Wyjście
        x = self.fc2(x)
        return x

# 5. Inicjalizacja modelu, funkcji straty i optymalizatora
model = SimpleNN()

# Funkcja straty (CrossEntropyLoss dla klasyfikacji wieloklasowej)
criterion = nn.CrossEntropyLoss()

# Optymalizator (SGD lub Adam)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 6. Trenowanie modelu
epochs = 5  # Liczba epok

for epoch in range(epochs):
    model.train()  # Ustawienie modelu w tryb treningowy
    running_loss = 0.0

    for images, labels in train_loader:
        # Spłaszczanie obrazu 28x28 na wektor 784
        images = images.view(-1, 28*28)
        
        # Zerowanie gradientów
        optimizer.zero_grad()
        
        # Przewidywanie
        outputs = model(images)
        
        # Obliczanie straty
        loss = criterion(outputs, labels)
        
        # Backpropagation
        loss.backward()
        
        # Optymalizacja
        optimizer.step()
        
        # Akumulowanie straty
        running_loss += loss.item()
    
    # Wyświetlanie straty na końcu epoki
    print(f"Epoka {epoch+1}/{epochs}, Strata: {running_loss/len(train_loader)}")

# 7. Testowanie modelu na zbiorze testowym
model.eval()  # Ustawienie modelu w tryb testowy
correct = 0
total = 0

with torch.no_grad():  # Wyłączenie obliczania gradientów
    for images, labels in test_loader:
        images = images.view(-1, 28*28)
        
        # Przewidywanie
        outputs = model(images)
        
        # Wybór klasy z najwyższym prawdopodobieństwem
        _, predicted = torch.max(outputs, 1)
        
        # Obliczanie liczby poprawnych klasyfikacji
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

# 8. Obliczanie dokładności
accuracy = 100 * correct / total
print(f"Dokładność na zbiorze testowym: {accuracy}%")