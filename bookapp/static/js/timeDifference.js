function timeDifference(current, previous) {
    console.log('timeDifference fired!');
    var milliSecondsPerMinute = 60 * 1000;
    var milliSecondsPerHour = milliSecondsPerMinute * 60;
    var milliSecondsPerDay = milliSecondsPerHour * 24;
    var milliSecondsPerMonth = milliSecondsPerDay * 30;
    var milliSecondsPerYear = milliSecondsPerDay * 365;
  
    var elapsed = current - previous
  
    if (elapsed < milliSecondsPerMinute / 3) {
      return 'Published just now';
    }
  
    else if (elapsed < milliSecondsPerHour) {
      return 'Published ' + Math.round(elapsed/milliSecondsPerMinute) + ' m ago';
    }
  
    else if (elapsed < milliSecondsPerDay ) {
      return 'Published ' + Math.round(elapsed/milliSecondsPerHour ) + ' h ago';
    }
  
    else if (elapsed < milliSecondsPerMonth) {
      return 'Published ' + Math.round(elapsed/milliSecondsPerDay) + ' d ago';
    }
  
    else if (elapsed < milliSecondsPerYear) {
      return 'Published ' + Math.round(elapsed/milliSecondsPerMonth) + ' mon ago';
    }
  
    else {
      return 'Published ' + Math.round(elapsed/milliSecondsPerYear ) + ' y ago';
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