const imageUrls = ["z2.jpg", "z3.jpg", "z4.jpg", "z6.jpg"];

function loadImage(url) {
  return new Promise(function (resolve, reject) {
    const img = new Image();
    img.src = url;
    img.alt = url;
    img.onload = function () {
      resolve(img);
    };
    img.onerror = function () {
      reject(new Error("Nie można załadować " + url));
    };
  });
}

Promise.all(imageUrls.map(function (url) {
  return loadImage(url);
}))
  .then(function (images) {
    const gallery = document.getElementById("gallery");
    images.forEach(function (img) {
      gallery.appendChild(img);
    });
  })
  .catch(function (error) {
    console.error("Błąd przy ładowaniu zdjęć:", error);
  });
