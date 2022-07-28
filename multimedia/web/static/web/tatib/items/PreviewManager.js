const previewSegment = $('#preview-segment')
const previewTitle = $('#preview-title')
const previewText = $('#preview-text')

export const showPreviewText = (title, text) => {
    previewTitle.text(title)
    previewText.text(text)
    previewSegment.transition('fade up in')
}

export function closePreview() {
    if (previewSegment.is(':visible')) {
        previewSegment.transition({
            animation: 'fade up out',
            duration: '125ms',
            queue: false,
        })
    }
}

previewSegment.click(() => {
    closePreview()
})
