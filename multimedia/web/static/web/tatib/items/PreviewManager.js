const previewSegment = $('#preview-segment')
const previewText = $('#preview-text')

export const showPreviewText = text => {
    previewText.text(text)
    previewSegment.transition('fade up in')
}

previewSegment.click(() => {
    previewSegment.transition({
        animation: 'fade up out',
        duration: '125ms',
        queue: false,
    })
})
