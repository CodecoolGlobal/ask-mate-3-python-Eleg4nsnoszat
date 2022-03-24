// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    let filterWord = filterValue;
    let columnCapitalized = 'Title';

    if(filterWord.includes(':')){
        let wordParts = filterWord.split(':');
        let column = wordParts[0];
        columnCapitalized = column.charAt(0).toUpperCase() + column.slice(1);
        if(columnCapitalized.includes('!')) {
            let filterParts = columnCapitalized.split('!');
            let column = filterParts[1]
            columnCapitalized = column.charAt(0).toUpperCase() + column.slice(1);
            }
        filterWord = wordParts[1];
    }


    if(filterWord.includes('!')){
        let wordParts = filterWord.split('!')
        filterWord = wordParts[1]
        }

    if(filterValue.includes('!')){
        return items.filter(function (item) {
            return !item[columnCapitalized].toLowerCase().includes(filterWord.toLowerCase());
        });

    } else {
        return items.filter(function (item) {
            return item[columnCapitalized].toLowerCase().includes(filterWord.toLowerCase());
        });
    }
    }


function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}