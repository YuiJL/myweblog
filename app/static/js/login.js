$(document).ready(function() {
    $("#change").click(function() {
        $("#upload").fadeToggle('fast');
    });
    $("#blogs, #control, #edit, #manage").click(function() {
        $("#upload").fadeOut('fast');
    });
});

new Vue({
    el: '#loginform',
    data: {
        email: '',
        password: '',
        message: ''
    },
    methods: {
        login: function() {
            this.email = this.email.trim();
            var self = this;
            $.ajax('/auth', {
                data: {
                    email: self.email,
                    sha1_password: sha1(self.email + ':' + self.password)
                }, 
                method: "POST"
            }).done(function() {
                return location.assign(location.pathname);
            }).fail(function(xhr) {
                self.message = xhr.responseText;
                return $('.alert').show();
            });
        }
    }
})