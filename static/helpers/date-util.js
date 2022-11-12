export function formatLongDate(dateString) {
    const date = new Date(dateString)
    return `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`
}
