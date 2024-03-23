document.head.insertAdjacentHTML('beforeend', `<link rel="stylesheet" href="files/css/galery.css">`)
const block = document.createElement('div');
block.id = 'wrapper';
block.innerHTML = `
  <div id="nav">
        <div onclick="changePhoto(-1)"><</div>
        <div onclick="changePhoto(1)">></div>
        <div onclick="closeImg()">X</div>
  </div>
  <div id="container"></div>
`
document.body.prepend(block);


let allImg = document.querySelectorAll('main img')
for (let item of allImg) {
    item.setAttribute('title', 'Нажмите для увеличения');
    item.style.cursor = 'pointer';
    item.setAttribute('onclick', 'imgZoom(this)')
}

let allSrc = [];
for (let i = 0; i < allImg.length; i++) {
    allSrc[i] = allImg[i].getAttribute('src')
}


let src;
const cont = document.getElementById('container');

function imgZoom(e) {
    src = e.getAttribute('src');
    cont.innerHTML = `<img src="${src}">`
    block.style.height = '100vh'
}

function closeImg() {
    block.style.height = '0'
}

let j = 0;

function changePhoto(n) {
    for (let i = 0; i < allSrc.length; i++) {
        if (allSrc[i] == src) { j = i }
    }

    j += n;
    if (j == allSrc.length) { j = 0 }
    if (j < 0) { j = allSrc.length - 1 }

    src = allSrc[j]
    cont.innerHTML = `<img src="${src}">`
}