const previewSegment = $('#preview-segment')
const previewTitle = $('.previewTitle')
const previewText = $('.previewText')

const showPreviewText = (title, text) => {
    previewTitle.text(title)
    previewText.text(text)
}

export function openPreview(title, text) {
    showPreviewText(title, text)
    previewSegment.transition('fade up in')
}

export function openModalPreview(title, text) {
    showPreviewText(title, text)
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
