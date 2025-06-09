document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('textarea').forEach(function(el) {
        ClassicEditor.create(el, {
            table: {
                contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
            },
            image: {
                toolbar: ['imageTextAlternative', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side']
            }
        }).catch(error => { console.error(error); });
    });
}); 