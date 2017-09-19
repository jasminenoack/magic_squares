function setupSimple(max, buttonSelector, intervalLength) {

    var interval;
    var button = document.getElementById(buttonSelector)
    var equation = document.getElementById(buttonSelector + '-equation')
    var stepsElement = document.getElementById(buttonSelector + "-steps")
    //
    function clearCurrentInterval() {
        clearInterval(interval)
        interval = null

    }
    //
    button.addEventListener('click', () => {
        var first, second
        var runnningTotal = 0;
        if (interval) {
            clearCurrentInterval()
        } else {
            function nextCurrent() {
                if (first === undefined) {
                    first = 0
                } else if (second === undefined) {
                    second = 1
                } else {
                    var newValue = first + second
                    first = second
                    second = newValue
                }
            }
            function nextSimple() {
                var html = ''
                html  += '<p>'
                if (first !== undefined && second !== undefined) {
                    html  += 'The last numbers are ' + first + " & " + second + '. '
                }
                nextCurrent()
                nextNum = second === undefined ? first : second
                html  += 'The next number is ' + nextNum + '.</p>'

                if (nextNum >= max) {
                    html += "<p>The next number is above the max(" + max + ").</p>"
                    html += "<p>The running total " + runnningTotal + '.</p>'
                    clearCurrentInterval()
                } else if (nextNum % 2 === 0) {
                    html += "<p>The number is even add it to the running total " + runnningTotal + " + " + nextNum + " = " + (runnningTotal + nextNum) + '.</p>'
                    runnningTotal += nextNum
                } else {
                    html += "<p>The number is odd, the running total " + runnningTotal + '.</p>'
                }

                stepsElement.innerHTML = html
            }
            nextSimple()
            interval = setInterval(nextSimple, intervalLength)
        }
    })
}

// setup super simple
setupSimple(100, 'simple', 1000)
setupSimple(100000, 'simple-100000', 500)
setupSimple(4000000, 'simple-4000000', 200)
