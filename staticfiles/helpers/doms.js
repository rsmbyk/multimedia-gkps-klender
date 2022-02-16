export const createDOMFromJSON = ({ tag, classList, children, innerText}) => {
    const element = document.createElement(tag)
    element.classList.add(...classList)

    if (children)
        $(element).append(...children.map(createDOMFromJSON))
    else if (innerText)
        element.innerText = innerText

    return $(element)
}
