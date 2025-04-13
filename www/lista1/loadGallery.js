const imageUrls = ['z2.jpg', 'z3.jpg', 'z4.jpg', 'z6.jpg'];

const loadImage = (url) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.src = url;
    img.alt = url;
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Nie można załadować ${url}`));
  });
};

Promise.all(imageUrls.map(loadImage))
  .then(images => {
    const gallery = document.getElementById('gallery');
    images.forEach(img => gallery.appendChild(img));
  })
  .catch(error => {
    console.error('Błąd przy ładowaniu zdjęć:', error);
  });