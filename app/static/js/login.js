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
                    self.message = 'E-mail address not found!';
                }
                if (xhr.responseText === "wrong password") {
                    self.message = 'Password is wrong!';
                }
                return $('.alert').show();
            });
        }
    }
});

new Vue({
    el: '#dropdownlogin',
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
                    self.message = 'E-mail address not found!';
                }
                if (xhr.responseText === "wrong password") {
                    self.message = 'Password is wrong!';
                }
                return $('.alert').show();
            });
        }
    }
});