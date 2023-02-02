function sortDivAscending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window p span:first-child').innerText;

    console.log(document.querySelector('.goal-window p span:first-child').innerText);

    const ascendingOrder = false;
    const isNumeric = true;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator(undefined, { numeric: isNumeric, sensitivity: 'base' });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementA, elementB] : [elementB, elementA];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Data Malejąco"
}

function sortDivDescending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window p span:first-child').innerText;

    console.log(document.querySelector('.goal-window p span:first-child').innerText);

    const descendingOrder = false;
    const isNumeric = true;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator(undefined, { numeric: isNumeric, sensitivity: 'base' });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = descendingOrder ? [elementB, elementA] : [elementA, elementB];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Data Rosnąco"
}

function sortDivNameAscending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window .goal-pay>h2').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementB, elementA] : [elementA, elementB];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Nazwa rosnąco"
}

function sortFamilyDivNameAscending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window>h2').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementB, elementA] : [elementA, elementB];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Nazwa rosnąco"
}

function sortDivNameDescending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window .goal-pay>h2').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementA, elementB] : [elementB, elementA];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Nazwa malejąco"
}

function sortFamilyDivNameDescending() {
    const parentElement = document.getElementById("goal-section");

    const selector = element => element.querySelector('.goal-window>h2').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('.goal-window')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementA, elementB] : [elementB, elementA];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info').innerHTML = "Sortowanie: Nazwa malejąco"
}



function sortDateAscending() {
    const parentElement = document.getElementById("transaction-body");

    const selector = element => Date.parse(element.querySelector('#date').innerText);

    date = Date.parse(document.querySelector('#date').innerText);

    const ascendingOrder = false;
    const isNumeric = true;

    const elements = [...document.querySelectorAll('#transaction-table tbody tr')];

    const collator = new Intl.Collator(undefined, { numeric: isNumeric, sensitivity: 'base' });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementA, elementB] : [elementB, elementA];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info2').innerHTML = "Sortowanie: Data Malejąco"
}

function sortDateDescending() {
    const parentElement = document.getElementById("transaction-body");

    const selector = element => Date.parse(element.querySelector('#date').innerText);

    date = Date.parse(document.querySelector('#date').innerText);

    const ascendingOrder = false;
    const isNumeric = true;

    const elements = [...document.querySelectorAll('#transaction-table tbody tr')];

    const collator = new Intl.Collator(undefined, { numeric: isNumeric, sensitivity: 'base' });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementB, elementA] : [elementA, elementB];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info2').innerHTML = "Sortowanie: Data rosnąco"
}

function sortHistoryNameDescending() {
    const parentElement = document.getElementById("transaction-body");

    const selector = element => element.querySelector('#title').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('#transaction-table tbody tr')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementB, elementA] : [elementA, elementB];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info2').innerHTML = "Sortowanie: Nazwa rosnąco"
}

function sortHistoryNameAscending() {
    const parentElement = document.getElementById("transaction-body");

    const selector = element => element.querySelector('#title').innerText;

    const ascendingOrder = false;

    const elements = [...document.querySelectorAll('#transaction-table tbody tr')];

    const collator = new Intl.Collator('pl', {
        ignorePunctuation: false,
        sensitivity: "base",
        usage: 'sort'
    });

    elements
        .sort((elementA, elementB) => {
            const [firstElement, secondElement] = ascendingOrder ? [elementA, elementB] : [elementB, elementA];
            const textOfFirstElement = selector(firstElement);
            const textofSecondElement = selector(secondElement);
            return collator.compare(textOfFirstElement, textofSecondElement);
        })
        .forEach(element => parentElement.appendChild(element));

    document.getElementById('sort-info2').innerHTML = "Sortowanie: Nazwa malejąco"
}