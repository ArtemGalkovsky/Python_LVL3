const a = document.querySelector('.alone');
let n = 0;
let result = 0;
let click = true;
const tl = document.getElementById('timeLine');

function checking(e) {
    if (click) {
        clearInterval(timer)
        click = false
        if (e.innerText == questions[n].corAns) {
            result++;
            e.style.background = "#77ff99";
            e.style.color = "#000"
            sound('correct.mp3')
        } else {
            e.style.background = "#ff7777";
            e.style.color = "#fff";
            sound('failure.mp3')
        }
        let str = '<input type="button" value="Следующий вопрос"  onclick="start()">'
        a.insertAdjacentHTML('beforeend', str)
        questions.splice(n, 1);
    }

}
let timer;

function start() {
    if (questions.length > 0) {
        click = true;
        n = Math.floor(Math.random() * questions.length);
        a.innerHTML = `
    <div id="quest"> ${questions[n].questText} </div>
    <div id="ansvers">
        <div class="ans" onclick="checking(this)"> ${questions[n].ansA} </div>
        <div class="ans" onclick="checking(this)"> ${questions[n].ansB} </div>
        <div class="ans" onclick="checking(this)"> ${questions[n].ansC} </div>
        <div class="ans" onclick="checking(this)"> ${questions[n].ansD} </div>
    </div>
    `
        tl.style.height = '100%';
        timer = setInterval(moveTime, 1000);
        time = 30;

    } else {
        a.innerHTML = `<h2>Количество правильных ответов ${result}  из 10</h2>
        <h1> ${result/10*100}% </h1>
        `
        sound('winning.mp3');
        let hi = localStorage.getItem('best');
        if (hi <= result) {
            localStorage.setItem('best', result);
            hi = result;
        }
        let c;
        if (result == 10) {
            c = comments[0]
        }
        if (result > 6 && result < 10) { c = comments[1] }
        if (result > 3 && result < 7) { c = comments[2] }
        if (result < 4) { c = comments[3] }
        a.insertAdjacentHTML('beforeend', `<p>${c}</p>`)
        a.insertAdjacentHTML('beforeend', `<p>Ваш лучший результат - ${hi} </p>`)
    }
}

let comments = ['Потрясающе. Вашей эрудиции можно позовидовать', 'Очень даже не плохо. Но есть над чем поработать', 'Ваши знания треуют корекции. На нашем сайте вы найдете ответы на все вопросы викторины.', 'Возможно стоило сначала ознакомится с содержанием сайта']

let questions = [
    {}
];
questions[0] = {
    questText: 'В каком заповеднике обитает 1/3 всей белорусской популяции бурого медведя?',
    ansA: 'Березинский',
    ansB: 'Полесский',
    ansC: 'Нарочанский',
    ansD: 'Припятский',
    corAns: 'Березинский',
}
questions[1] = {
    questText: 'Какой заповедник появиля спуся 2 года после чернобыльской аварии?',
    ansA: 'Березинский',
    ansB: 'Полесский',
    ansC: 'Нарочанский',
    ansD: 'Припятский',
    corAns: 'Полесский',
}
questions[2] = {
    questText: 'Сколько видов рыб обитает в национальном парке  Нарочанский?',
    ansA: '8',
    ansB: '18',
    ansC: '32',
    ansD: '35',
    corAns: '35',
}

questions[3] = {
    questText: 'В каком году Беловежская пуща стала заповедной зоной?',
    ansA: '1939',
    ansB: '1991',
    ansC: '1812',
    ansD: '1917',
    corAns: '1939',
}
questions[4] = {
    questText: 'Где раположены сомае большое по площади и самое глубокое озера Бларуси?',
    ansA: 'Национальный парк «Нарочанский»',
    ansB: 'Национальный парк «Браславские озёра»',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Национальный парк Припятский',
    corAns: 'Национальный парк «Браславские озёра»',
}
questions[5] = {
    questText: 'Большую часть территории какого национального парка занимают дремучие леса и болота?',
    ansA: 'Национальный парк «Нарочанский»',
    ansB: 'Национальный парк «Браславские озёра»',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Национальный парк Припятский',
    corAns: 'Национальный парк Припятский',
}
questions[6] = {
    questText: 'Где расположен самый большой лесной массив в Беларуси?',
    ansA: 'Национальный парк «Нарочанский»',
    ansB: 'Налибокская пуща',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Национальный парк Припятский',
    corAns: 'Налибокская пуща',
}
questions[7] = {
    questText: 'Где расположена  самая большая экологическая тропа с деревянным настилом – 2,5 км?',
    ansA: 'Национальный парк «Нарочанский»',
    ansB: 'Налибокская пуща',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Республиканский ландшафтный заказник «Ельня»',
    corAns: 'Республиканский ландшафтный заказник «Ельня»',
}
questions[8] = {
    questText: 'В каком заповеднике обитает самая большая популяция зубров?',
    ansA: 'Беловежская пуща',
    ansB: 'Налибокская пуща',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Республиканский ландшафтный заказник «Ельня»',
    corAns: 'Беловежская пуща',
}

questions[9] = {
    questText: 'В каком заповеднике обитают порядка 40 видов исчезающих животных,  в  том числе – лошади Пржвальского?',
    ansA: 'Беловежская пуща',
    ansB: 'Налибокская пуща',
    ansC: 'Полесский государственный заповедник',
    ansD: 'Республиканский ландшафтный заказник «Ельня»',
    corAns: 'Полесский государственный заповедник',
}



function sound(s) {
    let audio = new Audio();
    audio.src = 'files/sound/' + s;
    audio.autoplay = true;
    audio.volume = 1;
}

let time = 30;

function moveTime() {
    tl.style.height = time * 100 / 30 + '%'
    time--;
    if (time < 0) {
        clearInterval(timer);
        sound('failure.mp3')
        let ans = document.getElementsByClassName('ans');
        for (let item of ans) {
            item.style.background = "#ff7777"
        }
        let str = '<input type="button" value="Следующий вопрос"  onclick="start()">'
        a.insertAdjacentHTML('beforeend', str);



    }
}