const h = document.querySelector('header')
h.innerHTML = `
<div id="title"> Заповедные места Беларуси</div>
<div id="headerImg"> </div>
`
const container = document.querySelector('#headerImg');

for (let i = 1; i < 9; i++) {
    container.innerHTML += `<img src="files/img/header/${i}.jpg">`
}

const headImg = document.querySelectorAll('#headerImg img')
for (let i = 1; i < 8; i++) {
    headImg[i].style.opacity = '0';
}
let k = 0;

function changeOpacity() {
    k++;
    if (k > 8) {
        k = 0;
        for (let i = 1; i < 8; i++) {
            headImg[i].style.opacity = '0';
        }
    }
    headImg[k].style.opacity = '1';
}

setInterval(changeOpacity, 4000);