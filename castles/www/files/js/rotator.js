const photo = document.getElementById('photo');
const img = document.querySelectorAll('#photo img');
let n = img.length; //количество картинок
photo.style.width = n * 840 + 'px';
let m = 0;
const count = document.getElementById('count');
let num = 1;
count.innerText = num + ' из ' + n

function movePhoto(a) {
    num -= a;
    if (num > n) { num = 1 }
    if (num < 1) { num = n }
    count.innerText = num + ' из ' + n

    m += a;
    if (m < -1 * (n - 1)) {
        m = 0;
    }
    if (m > 0) { m = -1 * (n - 1) }

    photo.style.marginLeft = m * 840 + 'px';
}