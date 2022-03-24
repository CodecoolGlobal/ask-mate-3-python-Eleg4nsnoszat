// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    for(let item of items){
        let voteCount = item['VoteCount']
        let voteCountNew = parseInt(voteCount)
        item['VoteCount'] = voteCountNew
        let viewNumber = item['ViewNumber']
        let viewNumberNew = parseInt(viewNumber)
        item['ViewNumber'] = viewNumberNew
    }

    if(sortDirection === 'asc') {
       return items.sort(function(x, y) {
          if (x[sortField] < y[sortField]) {
            return -1;
          }
          if (x[sortField] > y[sortField]) {
            return 1;
          }
          return 0;
        });

    } else {
       return items.sort(function(x, y) {
          if (x[sortField] > y[sortField]) {
            return -1;
          }
          if (x[sortField] < y[sortField]) {
            return 1;
          }
          return 0;
        });
    }
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