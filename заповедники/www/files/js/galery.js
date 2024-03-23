let allImg = document.querySelectorAll('main img');
for (let item of allImg) {
    item.setAttribute('title', 'Кликните для увеличения');
    item.style.cursor = "pointer";
    item.setAttribute('onclick', 'imgZoom(this)')
}

let allSrc = [];
for (let i = 0; i < allImg.length; i++) {
    allSrc[i] = allImg[i].getAttribute('src')
}

let wrap = document.createElement('div');
wrap.id = "wrapper";
wrap.innerHTML = `
    <div id="nav">
        <div onclick="changePhoto(-1)"> < </div>
        <div onclick="changePhoto(1)"> > </div>
        <div onclick="closeImg()"> X </div>
    </div>
    <div id="container"></div>
`
document.body.prepend(wrap);
let src;
const cont = document.getElementById('container');

function imgZoom(e) {
    wrap.style.height = '100vh'
    src = e.getAttribute('src')
    cont.innerHTML = `<img src="${src}">`
}

function closeImg() {
    wrap.style.height = '0'
}
let j = 0;

function changePhoto(n) {
    for (let i = 0; i < allSrc.length; i++) {
        if (allSrc[i] == src) {
            j = i;
        }
    }

    j += n;
    if (j < 0) { j = allSrc.length - 1 }
    if (j >= allSrc.length) { j = 0 }

    src = allSrc[j]
    cont.innerHTML = `<img src="${src}">`

}