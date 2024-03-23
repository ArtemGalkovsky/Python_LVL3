const bg = document.createElement('div');
bg.id = 'background';
document.body.prepend(bg);

function changePhoto(e) {

    if (e.className == "small") {
        e.className = "large"
        bg.style.height = "100%"
    } else {
        e.className = "small"
        bg.style.height = "0"
    }
}