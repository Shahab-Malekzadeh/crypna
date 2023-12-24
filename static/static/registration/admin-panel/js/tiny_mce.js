document.addEventListener("DOMContentLoaded", function (event) {
    let sc = document.createElement('script');
    sc.setAttribute('src', 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.6.2/tinymce.min.js');
    sc.setAttribute('integrity', 'sha512-sOO7yng64iQzv/uLE8sCEhca7yet+D6vPGDEdXCqit1elBUAJD1jYIYqz0ov9HMd/k30e4UVFAovmSG92E995A==');
    sc.setAttribute('crossorigin', 'anonymous');
    document.head.appendChild(sc);

    sc.onload = () => {
        tinymce.init({
            selector: '#id_description',
            /* enable title field in the Image dialog*/
            image_title: true,
            /* enable automatic uploads of images represented by blob or data URIs*/
            automatic_uploads: true,
            /*
              URL of our upload handler (for more details check: https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_url)
              images_upload_url: 'postAcceptor.php',
              here we add custom filepicker only to Image dialog
            */
            file_picker_types: 'image',
            /* and here's our custom image picker*/
            file_picker_callback: function (cb, value, meta) {
                var input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', 'image/*');

                /*
                  Note: In modern browsers input[type="file"] is functional without
                  even adding it to the DOM, but that might not be the case in some older
                  or quirky browsers like IE, so you might want to add it to the DOM
                  just in case, and visually hide it. And do not forget do remove it
                  once you do not need it anymore.
                */

                input.onchange = function () {
                    var file = this.files[0];

                    var reader = new FileReader();
                    reader.onload = function () {
                        /*
                          Note: Now we need to register the blob in TinyMCEs image blob
                          registry. In the next release this part hopefully won't be
                          necessary, as we are looking to handle it internally.
                        */
                        var id = 'blobid' + (new Date()).getTime();
                        var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                        var base64 = reader.result.split(',')[1];
                        var blobInfo = blobCache.create(id, file, base64);
                        blobCache.add(blobInfo);

                        /* call the callback and populate the Title field with the file name */
                        cb(blobInfo.blobUri(), {title: file.name});
                    };
                    reader.readAsDataURL(file);
                };

                input.click();
            },
            // content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
            toolbar_mode: 'wrap',
            resize: 'both',
            media_live_embeds: true,
            placeholder: 'Write your article ...',
            // directionality : 'rtl',
            directionality : 'ltr',
            height: 700,
            autosave_interval: '15s',
            plugins: [
                'image code advlist autolink link image lists charmap print preview hr anchor pagebreak',
                'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
                'table template paste autosave help'
            ],
            toolbar: 'undo redo | styleselect | media link image | bold italic | forecolor backcolor |' +
                'alignleft aligncenter alignright alignjustify | ' +
                'bullist numlist outdent indent | print preview fullpage |' +
                '| help | | | | restoredraft',
            menu: {
                file: {
                    title: 'File', items: 'newdocument restoredraft | preview | print '
                },
                edit: {
                    title: 'Edit', items: 'undo redo | cut copy paste | selectall | searchreplace'
                },
                view: {
                    title: 'View',
                    items: 'code | visualaid visualchars visualblocks | spellchecker | preview fullscreen'
                },
                insert: {
                    title: 'Insert',
                    items: 'image link media template codesample inserttable | charmap hr |' +
                        'pagebreak nonbreaking anchor toc | insertdatetime'
                },
                format: {
                    title: 'Format',
                    items: 'bold italic underline strikethrough superscript subscript codeformat |' +
                        'formats blockformats align lineheight | forecolor backcolor | removeformat'
                },
                tools: {
                    title: 'Tools', items: 'spellchecker spellcheckerlanguage | code wordcount'
                },
                table: {
                    title: 'Table', items: 'inserttable | cell row column | tableprops deletetable'
                },
                help: {
                    title: 'Help', items: 'help'
                }
            },
            menubar: 'favs file edit view insert format tools table help',
            content_css: 'css/content.css'
        });
    }
});
