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
                return location.assign('/');
            }).fail(function(xhr) {
                if (xhr.responseText === "invalid email") {
                    self.message = 'E-mail not found!';
                }
                if (xhr.responseText === "wrong password") {
                    self.message = 'Wrong password!';
                }
                return $('.alert').show();
            });
        }
    }
});