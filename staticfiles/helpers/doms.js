const createDOMFromJSON = (data) => {
    const element = document.createElement(data.tag)
    element.classList.add(...data.classList)

    if (data.children)
        element.append(...data.children.map((child, _) => createDOMFromJSON(child)))
    else if (data.innerText)
        element.innerText = data.innerText

    return element
}
