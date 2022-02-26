export const createDOMFromJSON = ({ tag, classList=[], children=null, innerText=null }) => {
    const element = document.createElement(tag)
    element.classList.add(...classList)

    if (children !== null && innerText !== null)
        throw 'Cant have children and innerText at the same time for now :)'

    if (children !== null && children.constructor.name === 'Array')
        $(element).append(...children.map(createDOMFromJSON))

    if (innerText !== null)
        element.innerText = innerText

    return $(element)
}
