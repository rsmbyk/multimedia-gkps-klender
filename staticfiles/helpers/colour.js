// SO answer from https://stackoverflow.com/a/5624139/5447454
// to convert hex to rgb and vice versa.
export const hexToRgb = hex => {
    // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    // Edit: Add another group to capture optional alpha colour.
    const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])([a-f\d])?$/i;

    hex = hex.replace(shorthandRegex, (m, r, g, b, a='') => {
        // 'a' needs to be set a default value of empty string
        // as it is undefined when capturing hex of form #???
        return r + r + g + g + b + b + a + a
    })

    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})?$/i.exec(hex)

    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
        a: parseInt(result[4], 16),
    } : null
}
