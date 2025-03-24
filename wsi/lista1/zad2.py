import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import confusion_matrix
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

current_folder = os.getcwd()
numbers_folder_path = os.path.join(current_folder, "lista1\\numbers")


def adapt_image(number_image_path):
    img = cv2.imread(number_image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img) 
    img = cv2.resize(img, (28,28))
    img = img.astype(np.float32) / 255.0 
    '''
    plt.imshow(img, cmap='gray')
    plt.title("Obraz po przetworzeniu")
    plt.show()
    '''
    img = torch.tensor(img).view(-1, 28*28)  
    return img


test_numbers = []

# Etykiety dla obrazów
numbers_labels = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0]

folder_names = os.listdir(numbers_folder_path)

for folder in folder_names:

    path_to_folder_with_digit = os.path.join(numbers_folder_path, folder)
    filenames = os.listdir(path_to_folder_with_digit)

    for filename in filenames:
        if filename.endswith(".jpg"):
            number_image_path = os.path.join(path_to_folder_with_digit, filename)
            img_tensor = adapt_image(number_image_path)
            test_numbers.append(img_tensor)

            img = cv2.imread(number_image_path, cv2.IMREAD_GRAYSCALE)
            
            '''
            plt.imshow(img, cmap='gray')
            plt.title(f"Plik: {filename}")
            plt.show()'
            '''
        

# Lista obrazów na tensor
test_numbers = torch.cat(test_numbers, dim=0)

transform = transforms.Compose([
    transforms.ToTensor(),  
    transforms.Normalize((0.5,), (0.5,))  # Normalizacja z średnią 0.5 i odchyleniem standardowym 0.5
])

train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)

# Dane ładowane w partiach po 64
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

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

y_true = []
y_pred = []


with torch.no_grad():
    for img_tensor, true_label in zip(test_numbers, numbers_labels):
        img_tensor = img_tensor.view(1, 28 * 28)  
        outputs = model(img_tensor)  
        _, predicted = torch.max(outputs, 1)  

        total += 1  # Zliczamy liczbę próbek
        correct += (predicted == true_label).sum().item()  # Porównujemy przewidywania z prawdziwą etykietą

        y_true.append(true_label)  # Etykieta prawdziwa
        y_pred.append(predicted.item())  # Etykieta przewidywana

# Obliczamy dokładność
accuracy = 100 * correct / total
print(f"Dokładność na zbiorze testowym: {accuracy}%")

print("----------Prawdziwe cyfry dla obrazów:", y_true)
# Wyświetlanie przewidywanych etykiet
print("Przewidywane cyfry dla Twoich obrazów:", y_pred)