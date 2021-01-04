// Creates a new file and add it to our list.
function ui_multi_add_file(id, file)
{
    var template = $('#files-template').text();
    template = template.replace('%%filename%%', file.name);

    template = $(template);
    template.prop('id', 'uploaderFile' + id);
    template.data('file-id', id);

    $('#files').find('li.empty').fadeOut(); // remove the 'no files yet'
    $('#files').prepend(template);
}

// Changes the status messages on our list.
function ui_multi_update_file_status(id, status, message)
{
    $('#uploaderFile' + id).find('span').html(message).prop('class', 'status text-' + status);
}

// Updates a file progress, depending on the parameters it may animate it or change the color.
function ui_multi_update_file_progress(id, percent, color, active)
{
    color = (typeof color === 'undefined' ? false : color);
    active = (typeof active === 'undefined' ? true : active);

    var bar = $('#uploaderFile' + id).find('div.progress-bar');

    bar.width(percent + '%').attr('aria-valuenow', percent);
    bar.toggleClass('progress-bar-striped progress-bar-animated', active);

    if (percent === 0) {
        bar.html('');
    } else {
        bar.html(percent + '%');
    }

    if (color !== false) {
        bar.removeClass('bg-success bg-info bg-warning bg-danger');
        bar.addClass('bg-' + color);
    }
}

$(function() {
    $('#drag-and-drop-zone').dmUploader({
        url: '/upload',
        dataType: 'text',
        multiple: true,
        fieldName: 'image',
        allowedTypes: 'image/jpeg|image/png',
        maxFileSize: 30000000, // 30 MBs.
        onDragEnter: function() {
            // Happens when dragging something over the DnD area.
            this.addClass('active');
        },
        onDragLeave: function() {
            // Happens when dragging something OUT of the DnD area.
            this.removeClass('active');
        },
        onInit: function() {
            // Plugin is ready to use.
        },
        onComplete: function() {
            // All files in the queue are processed (success or error).
        },
        onNewFile: function(id, file) {
            // When a new file is added using the file selector or the DnD area.
            ui_multi_add_file(id, file);
        },
        onBeforeUpload: function(id) {
            // About tho start uploading a file.
            ui_multi_update_file_status(id, 'uploading', 'Uploading...');
            ui_multi_update_file_progress(id, 0, '', true);
        },
        onUploadCanceled: function(id) {
            // Happens when a file is directly canceled by the user.
            ui_multi_update_file_status(id, 'warning', 'Canceled by User');
            ui_multi_update_file_progress(id, 0, 'warning', false);
        },
        onUploadProgress: function(id, percent) {
            // Updating file progress.
            ui_multi_update_file_progress(id, percent);
        },
        onUploadSuccess: function(id, data) {
            // A file was successfully uploaded.
            data;
            ui_multi_update_file_status(id, 'success', 'Upload Complete');
            ui_multi_update_file_progress(id, 100, 'success', false);
        },
        onUploadError: function(id, xhr, status, message) {
            ui_multi_update_file_status(id, 'danger', message);
            ui_multi_update_file_progress(id, 0, 'danger', false);    
        },
        onFallbackMode: function() {
            // When the browser doesn't support this plugin :(
        }
    });
});