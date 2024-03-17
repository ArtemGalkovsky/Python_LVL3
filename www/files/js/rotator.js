const photo = document.getElementById('photo');
const img = document.querySelectorAll('#photo img')
const n = img.length;
photo.style.width = n * 730 + 'px';
let m = 0;
const count = document.getElementById('counter');
let num = 1;
count.innerText = num + ' из ' + n;

function movePhoto(a) {
    m += a;
    num += a;
    if (num < 1) num = n;
    if (num > n) num = 1;
    count.innerText = num + ' из ' + n;
    if (m == n) { m = 0 }
    if (m == -1) { m = n - 1 }
    photo.style.marginLeft = m * 730 * (-1) + 'px';
}