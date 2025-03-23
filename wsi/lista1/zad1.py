import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

transform = transforms.Compose([
    transforms.ToTensor(),  
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja z średnią 0.5 i odchyleniem standardowym 0.5
])

train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# Dane ładowane w partiach po 64
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

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
correct = 0
total = 0

with torch.no_grad():  # Wyłączenie obliczania gradientów
    for images, labels in test_loader:
        images = images.view(-1, 28*28)
        
        outputs = model(images)
        
        # Wybór klasy (cyfry) z najwyższym prawdopodobieństwem
        _, predicted = torch.max(outputs, 1)
        
        # Obliczanie liczby poprawnych klasyfikacji
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

# Obliczanie dokładności
accuracy = 100 * correct / total
print(f"Dokładność na zbiorze testowym: {accuracy}%")