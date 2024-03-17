const bg = document.createElement('div');
bg.className = "background";
document.body.prepend(bg);



function changePhoto(a) {
    if (a.className == 'small') {
        a.className = 'large';
        bg.style.height = '100%'
    } else {
        a.className = 'small';
        bg.style.height = '0%'
    }
}