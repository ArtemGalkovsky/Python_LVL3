const header = document.querySelector('header');
let s = `<img src="www/files/img/header/1.jpg" onerror="changeImg('www/files/img/header')"  onload="changeImg(www/img/header)">`
header.innerHTML = s;

function changeImg(path) {
    s = `<div id="title">Замки Беларуси</div>
    <div id="headerImg">
       <img src="www/${path}/1.jpg" alt="Фото не найдено">
       <img src="www/${path}/2.jpg" alt="Фото не найдено">
       <img src="www/${path}/3.jpg" alt="Фото не найдено">
       <img src="www/${path}/4.jpg" alt="Фото не найдено">
       <img src="www/${path}/5.jpg" alt="Фото не найдено">
       <img src="www/${path}/6.jpg" alt="Фото не найдено">
       <img src="www/${path}/7.jpg" alt="Фото не найдено">
       <img src="www/${path}/8.jpg" alt="Фото не найдено">
       <img src="www/${path}/9.jpg" alt="Фото не найдено">
    </div>`
    header.innerHTML = s;

    let headImg = document.querySelectorAll('header img')
    for (let i = 1; i < 9; i++) {
        headImg[i].style.opacity = '0';
    }
    setInterval(changeOpacity, 4000)
}
let k = 0;



function changeOpacity() {
    let headImg = document.querySelectorAll('header img');
    k++;
    if (k > 8) {
        for (let i = 1; i < 9; i++) {
            headImg[i].style.opacity = '0';
        }
        k = 0;
    }
    headImg[k].style.opacity = '1';

}