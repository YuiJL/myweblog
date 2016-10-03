$(document).ready(function() {
    $('#avatar').click(function() {
        upload.image = '';
    });
});

var upload = new Vue({
    el: '#upload',
    data: {
        image: ''
    },
    methods: {
        onFileChange: function(e) {
            var file = e.target.files[0];
            if (file.name.length < 1) {
                return;
            } else if (file.size > 1000000) {
                alert("The file is too big, should be at most 1 MB");
                return;
            } else if (file.type != 'image/png' && file.type != 'image/jpg' && file.type != 'image/gif' && file.type != 'image/jpeg' && file.type != 'image/bmp') {
                alert("The file does not match png, jpg, bmp or gif");
                return;
            } else {
                var reader = new FileReader();
                var self = this;
                reader.onload = function(e) {
                    self.image = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        },
        removeImage: function() {
            this.image = '';
        }
    }
})