document.addEventListener('DOMContentLoaded', function() {
    if (typeof tinymce !== "undefined") {
        tinymce.init({
            selector: '#id_content, #id_description, #id_short_description',
            height: 500,
            width: '100%',
            plugins: 'image link media code table lists',
            toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code',
            image_advtab: true,
            file_picker_types: 'image',
            automatic_uploads: true,
            relative_urls: false,
            remove_script_host: false,
            content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, San Francisco, Segoe UI, Roboto, Helvetica Neue, sans-serif; font-size: 14px; }',
            branding: false,
            promotion: false,
            menubar: false,
            statusbar: false,
            resize: false,
            setup: function(editor) {
                editor.on('change', function() {
                    editor.save();
                });
            }
        });
    }
}); 