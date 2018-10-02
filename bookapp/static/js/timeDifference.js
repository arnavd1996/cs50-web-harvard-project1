function timeDifference(current, previous) {
    console.log('timeDifference fired!');
    var milliSecondsPerMinute = 60 * 1000;
    var milliSecondsPerHour = milliSecondsPerMinute * 60;
    var milliSecondsPerDay = milliSecondsPerHour * 24;
    var milliSecondsPerMonth = milliSecondsPerDay * 30;
    var milliSecondsPerYear = milliSecondsPerDay * 365;
  
    var elapsed = current - previous
  
    if (elapsed < milliSecondsPerMinute / 3) {
      return 'just now';
    }
  
    else if (elapsed < milliSecondsPerHour) {
      return Math.round(elapsed/milliSecondsPerMinute) + ' m';
    }
  
    else if (elapsed < milliSecondsPerDay ) {
      return Math.round(elapsed/milliSecondsPerHour ) + ' h';
    }
  
    else if (elapsed < milliSecondsPerMonth) {
      return Math.round(elapsed/milliSecondsPerDay) + ' d';
    }
  
    else if (elapsed < milliSecondsPerYear) {
      return Math.round(elapsed/milliSecondsPerMonth) + ' mon';
    }
  
    else {
      return Math.round(elapsed/milliSecondsPerYear ) + ' y';
    }
}

function timeDifferenceForDate(id, date) {
    var now = new Date().getTime();
    var updated = new Date(date).getTime();
    var text = timeDifference(now, updated);
    if (id) {
      var timeDifferenceElement = document.getElementById("timeDifferenceElement" + id)
      timeDifferenceElement.innerHTML = text;
    } else {
      return text;
    }
}