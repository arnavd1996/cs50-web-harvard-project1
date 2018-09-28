function timeDifference(current, previous) {
    console.log('timeDifference fired!')
    const milliSecondsPerMinute = 60 * 1000
    const milliSecondsPerHour = milliSecondsPerMinute * 60
    const milliSecondsPerDay = milliSecondsPerHour * 24
    const milliSecondsPerMonth = milliSecondsPerDay * 30
    const milliSecondsPerYear = milliSecondsPerDay * 365
  
    const elapsed = current - previous
  
    if (elapsed < milliSecondsPerMinute / 3) {
      return 'just now'
    }
  
    if (elapsed < milliSecondsPerMinute) {
      return 'less than 1 min ago'
    }
  
    else if (elapsed < milliSecondsPerHour) {
      return Math.round(elapsed/milliSecondsPerMinute) + ' min ago'
    }
  
    else if (elapsed < milliSecondsPerDay ) {
      return Math.round(elapsed/milliSecondsPerHour ) + ' h ago'
    }
  
    else if (elapsed < milliSecondsPerMonth) {
      return Math.round(elapsed/milliSecondsPerDay) + ' days ago'
    }
  
    else if (elapsed < milliSecondsPerYear) {
      return Math.round(elapsed/milliSecondsPerMonth) + ' mo ago'
    }
  
    else {
      return Math.round(elapsed/milliSecondsPerYear ) + ' years ago'
    }
}

function timeDifferenceForDate(id, date) {
    console.log('timeDifferenceForDate fired!');
    console.log('date = ', date);
    console.log('this! = ', this)
    const now = new Date().getTime()
    const timeDifferenceElement = document.getElementById("timeDifferenceElement" + id)
    const updated = new Date(date).getTime()
    console.log('now = ', now);
    console.log('updated = ', updated);
    const diffe = timeDifference(now, updated);
    console.log('diffe = ', diffe);
    timeDifferenceElement.innerHTML = diffe
}