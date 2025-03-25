from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report


mnist = fetch_openml('mnist_784', version=1, as_frame=False)
X, y = mnist.data, mnist.target     # Podział na dane i etykiety

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Stworzenie i wytrenowanie klasyfikatora Random Forest o 100 drzewach decyzyjnych
forest = RandomForestClassifier(n_estimators=100)
forest.fit(X_train, y_train)

y_pred = forest.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')    # Precyzja
recall = recall_score(y_test, y_pred, average='macro')          # Czułość

print(f'Dokładność: {accuracy:.4f}')
print(f'Precyzja: {precision:.4f}')
print(f'Czułość: {recall:.4f}')