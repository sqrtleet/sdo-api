let main = document.querySelector(".main");
let currentButton = null;
let depth1 = document.querySelector(".depth1");
let content = null
let depth2 = null;
let depth3 = null;
let depth4 = null;
let category = null;
let spec = null;
let semester_data = null;
let course_data = null;
let dict_data = null;

function changeColor(button) {
    if (currentButton !== null) {
        currentButton.classList.remove("pressed");
    }
    currentButton = button;
    currentButton.classList.add("pressed");
}

function showDepth1() {
    depth1.style.visibility = "visible";
}

function showDepth2(arg, data) {
    dict_data = data;
    if (depth2 === null) {
        content = document.createElement("div");
        content.classList.add("depth_content");
        depth2 = document.createElement("div");
        depth2.classList.add("depth2");
        main.appendChild(content);
        content.appendChild(depth2);
    } else {
        depth2.innerHTML = "";
    }

    if (depth3 != null) {
        depth2.innerHTML = "";
        depth3.innerHTML = "";
    }

    if (depth4 != null) {
        depth2.innerHTML = "";
        depth4.innerHTML = "";
    }

    category = arg;

    for (const key in data[arg]) {
        const button = document.createElement("button");
        button.classList.add("specialty_btn");
        button.innerText = key;
        button.onclick = function () {
            changeColor(button);
            showDepth3(key, data);
        };
        depth2.appendChild(button);
    }
}

function showDepth3(arg, data) {
    if (depth3 === null) {
        depth3 = document.createElement("div");
        depth3.classList.add("depth3");
        content.appendChild(depth3);
    } else {
        depth3.innerHTML = "";
    }
    depth2.innerHTML = "";
    spec = arg;

    for (const key in data[category][arg]) {
        const button = document.createElement("button");
        button.classList.add("course_btn");
        button.innerText = key;
        button.onclick = function () {
            changeColor(button);
            showDepth4(key, data);
        };
        depth3.appendChild(button);
    }
}

function showDepth4(arg, data) {
    if (depth4 === null) {
        depth4 = document.createElement("div");
        depth4.classList.add("depth4");
        content.appendChild(depth4);
    } else {
        depth4.innerHTML = "";
    }
    depth3.innerHTML = "";

    const block = document.createElement("div");
    const button = document.createElement("button");
    block.classList.add('content');
    button.classList.add("btn");
    button.innerText = "Назад";
    button.onclick = function () {
        changeColor(button);
        depth4.innerHTML = "";
        depth3.innerHTML = "";
        showDepth3(spec, data);
    };


    for (const key in data[category][spec][arg]) {
        let id = data[category][spec][arg][key];
        const button = document.createElement("button");
        button.classList.add("course_btn");
        button.innerText = key;
        button.id = id;
        button.onclick = async function () {
            let buttons = document.querySelectorAll('button')
            buttons.forEach(function (button) {
                button.disabled = true;
            });
            await semester_request(id)
            console.log(semester_data);
            for (let i in semester_data['data']) {
                let course_id = semester_data['data'][i]['id'];
                await course_request(course_id);
                await getExcel(course_data);
            }
            buttons.forEach(function (button) {
                button.disabled = false;
            });
        };
        depth4.appendChild(button);
    }
    depth4.appendChild(block);
    block.appendChild(button);
}


async function semester_request(btn_id) {
    await fetch('/semester_parse?semester_id=' + btn_id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            semester_data = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

async function course_request(btn_id) {
    await fetch('/course_parse?course_id=' + btn_id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            course_data = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

async function getExcel(data) {
    const response = await fetch('/get_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: data }),
    });

    if (!response.ok) {
        console.error('Error:', response.statusText);
        return;
    }

    const blob = await response.blob();

    const downloadLink = document.createElement('a');
    downloadLink.href = window.URL.createObjectURL(blob);
    downloadLink.download = 'semester.xlsx';
    downloadLink.click();
}

async function check() {
    for (let level in dict_data) {
        console.log(`Уровень: ${level}`);
        for (let specialty in dict_data[level]) {
            console.log(`Направление: ${specialty}`);
            for (let year in dict_data[level][specialty]) {
                console.log(`Курс: ${year}`);
                for (let semester in dict_data[level][specialty][year]) {
                    console.log(`Семестр: ${semester}`);
                    let s_id = dict_data[level][specialty][year][semester]
                    await semester_request(s_id);
                    for (let course in semester_data['data']) {
                        console.log(`Предмет: ${course}`);
                        if (semester_data['data'][course].hasOwnProperty('id')) {
                            let c_id = semester_data['data'][course]['id'];
                            await course_request(c_id);
                            console.log(course_data['data'])
                        }
                    }
                }
            }
        }
    }
}