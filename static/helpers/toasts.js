export const toast = (type, message, position='top attached') => {
    $('body').toast({
        class: `${type} centered`,
        message: message,
        position: position,
    })
}

export const success = (message, position) => {
    toast('success', message, position)
}

export const error = (message, position) => {
    toast('error', message, position)
}
