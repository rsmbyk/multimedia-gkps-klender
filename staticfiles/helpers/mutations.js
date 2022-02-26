/*
 A solution from https://stackoverflow.com/a/20683311/5447454 to
 listen to changes to 'style' attribute in order to keep 'flex'
 display in modal as it kept getting set to 'block' everytime
 it is shown. Semantics sets the value to inline style attribute,
 hence it can't be overridden via !important keyword in css.
 The workaround here is to change the display to flex everytime
 semantics tries to change it to block on showing the modal.
 */
export const observeFlexModal = modal => {
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutationRecord => {
            if ($(mutationRecord.target).css('display') === 'block')
                /*
                 This line use code from here:
                 https://stackoverflow.com/a/59073080/5447454
                 to apply !important style attribute.
                 */
                modal.style.setProperty('display', 'flex', 'important')
        });
    });

    observer.observe(modal, { attributes : true, attributeFilter : ['style'] });
}
