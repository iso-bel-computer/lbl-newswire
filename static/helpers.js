
export function prettyFormatDate(year, month, day) {
    const nowYear = new Date().getFullYear()
    let suffix = ''
    day = parseInt(day)
    if (day === 1 || day === 21 || day === 31) {suffix = 'st'}
    else if (day === 2 || day === 22) {suffix = 'nd'}
    else if (day === 3 || day === 23) {suffix = 'rd'}
    else {suffix = 'th'}

    // oops - shouldn't have done strftime on the backend
    const months = ['null', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const monthstr = months[parseInt(month)]

    let yearStr = ''
    if (parseInt(year) != parseInt(nowYear)) {yearStr =  year}

    return `${day}${suffix} ${monthstr} ${yearStr}`
}
