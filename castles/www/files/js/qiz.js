const a = document.querySelector('.allone');
let n = 0;

let result = 0;
let click = true;

function checking(e) {
    if (click) {

        click = false;
        if (e.innerText == quest[n].corAns) {
            result++;
            e.style.background = "#77ff99";
            e.style.color = "#000";
            sound('correct.mp3')
        } else {
            e.style.background = "#ff7777";
            e.style.color = "#fff"
            sound('failure.mp3')
        }
        let but = '<input type="button" onclick="start()" value="Следующий вопрос">'
        a.insertAdjacentHTML('beforeEnd', but);
        quest.splice(n, 1)
    }

}



function start() {
    if (quest.length > 0) {
        click = true;
        n = Math.floor(Math.random() * quest.length)
        a.innerHTML = `
        <div id="quest"> ${quest[n].textQuest}</div>
        <div id="ansvers">
        <div class="ans" onclick="checking(this)">  ${quest[n].ansA}</div>
        <div class="ans" onclick="checking(this)">  ${quest[n].ansB}</div>
        <div class="ans" onclick="checking(this)">  ${quest[n].ansC}</div>
        <div class="ans" onclick="checking(this)">  ${quest[n].ansD}</div>
    </div>
    `
    } else {
        sound('winning.mp3')
        let hi = sessionStorage.getItem('best');
        if (hi < result) {
            sessionStorage.setItem('best', result);
            hi = result
        }

        a.innerHTML = `<h2>Правильных тветов ${result} из 10</h2>`
        let com = '';
        if (result > 8) com = comment[0];
        if (result > 4 && result < 9) com = comment[1];
        if (result > 1 && result < 5) com = comment[2];
        if (result < 2 && result > 0) com = comment[3];
        if (result == 0) com = comment[4];
        a.insertAdjacentHTML('beforeend', com)
        a.insertAdjacentHTML('beforeend', `<p>Ваш лучший результат ${hi} </p>`)
    }
}

let comment = [];
comment[0] = '<p>Блестяще, вашим знаниям можно позавидовать</p>'
comment[1] = '<p>В целом неплохо. Но есть над чем поработать</p>'
comment[2] = '<p> На этом сайте вы найдете ответы на все вопросы викторины. Попробуйте ещё раз. </p>'
comment[3] = '<p>Лучше чем ничего. Но для начало не мешало бы почитать материалы на нашем сайте </p>'
comment[4] = '<p>Это фиаско</p>'

let quest = [
    {}
];
quest[0] = {
    textQuest: 'В каком веке был основан Несвижский дворец',
    ansA: '14',
    ansB: '15',
    ansC: '16',
    ansD: '17',
    corAns: '16',
}

quest[1] = {
    textQuest: 'В каком году открылся для посетителей Мирский замок после реставрации?',
    ansA: '1693',
    ansB: '1936',
    ansC: '1995',
    ansD: '2010',
    corAns: '2010',
}
quest[2] = {
    textQuest: 'В каком году пожар уничтожил Лидский замок?',
    ansA: '1891',
    ansB: '1327',
    ansC: '2010',
    ansD: '1917',
    corAns: '1891',
}
quest[3] = {
    textQuest: 'В каком замке расплагалась резиденция князей Пусловских?',
    ansA: 'Мирский',
    ansB: 'Лидский',
    ansC: 'Косовский',
    ansD: 'Несвижский',
    corAns: 'Косовский',
}

quest[4] = {
    textQuest: 'Кто начал строительство любчанского дворца в 1581г.?',
    ansA: 'Радзивилл Николай Чёрный',
    ansB: 'Великий князь литовский Александр Ягеллончик',
    ansC: 'Князь Миндовг',
    ansD: 'Влиятельный вельможа Ян Кишка',
    corAns: 'Влиятельный вельможа Ян Кишка',
}
quest[5] = {
    textQuest: 'Где хранилась богатая коллекция книг – личная библиотека Николая Румянцева?',
    ansA: 'Мирский замок',
    ansB: 'Несвижский замок',
    ansC: 'Гомельский дворец',
    ansD: 'Любчанский замок',
    corAns: 'Гомельский дворец',
}
quest[6] = {
    textQuest: 'Какой замок является памятником архитектуры, самым старейшим представителем и единственным сохранившимся из королевских замков на территории Беларуси?',
    ansA: 'Гродненский замок',
    ansB: 'Несвижский замок',
    ansC: 'Гомельский дворец',
    ansD: 'Любчанский замок',
    corAns: 'Гродненский замок',
}
quest[7] = {
    textQuest: 'Какой замок  первый на территории современной Беларуси , полностью построенный из камня.?',
    ansA: 'Гродненский замок',
    ansB: 'Кревский замок',
    ansC: 'Гомельский дворец',
    ansD: 'Любчанский замок',
    corAns: 'Кревский замок',
}

quest[8] = {
    textQuest: 'Какой замок  на территории современной Беларуси в 1706г.  был взорван шведами и сохранился до нашего времени лишь в виде руин?',
    ansA: 'Гродненский замок',
    ansB: 'Кревский замок',
    ansC: 'Новогрудский замок',
    ansD: 'Любчанский замок',
    corAns: 'Новогрудский замок',
}

quest[9] = {
    textQuest: 'Кто построил Ружанский замок?',
    ansA: 'Великий литовский канцлер Лев Сапега',
    ansB: 'Великий князь литовский Александр Ягеллончик',
    ansC: 'Влиятельный вельможа Ян Кишка',
    ansD: 'Радзивилл Николай Чёрный',
    corAns: 'Великий литовский канцлер Лев Сапега',
}

function sound(s) {
    let audio = new Audio();
    audio.src = 'www/files/sound/' + s
    audio.autoplay = true;
    audio.volume = 0.5
}