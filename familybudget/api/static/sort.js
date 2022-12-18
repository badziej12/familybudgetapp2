// function sortdiv() {
//     var container = document.getElementById("goal-section");
//     var elements = container.children;

//     var sortMe = [elements[0]];
//     for (var i = 1; i < elements.length; i++) {
//         var day = parseInt(elements[i].lastElementChild.lastElementChild.innerHTML.split(" ")[0]);
//         for (let elem of sortMe) {
//             if ()
//         }
//     }

// }



function sortDiv(event) {
    console.log(this.options[this.selectedIndex].text);
    if (this.options[this.selectedIndex].text == "Data rosnąco") {
        sortDivAscending();
    }
    if (this.options[this.selectedIndex].text == "Data malejąco") {
        sortDivDescending();
    }
}

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
}

window.onload = sortDivDescending

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
}     