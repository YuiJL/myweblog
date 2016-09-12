function validEmail(email) {
    var re = /^[\w\.\-]+\@[\w\-]+(\.[\w\-]+){1,4}$/;
    return re.test(email);
}

new Vue({
    el: '#signupform',
    data: {
        name: '',
        email: '',
        password1: '',
        password2: '',
        message: ''
    },
    methods: {
        submit: function() {
            var email = this.email.trim();
            if (!validEmail(email)) {
                this.message = "Please enter a valid e-mail address!";
                return $('.alert').show();
            }
            if (this.password1.length < 6) {
                this.message = "Password must be at least 6 characters!";
                return $('.alert').show();
            }
            if (this.password1 !== this.password2) {
                this.message = "The two passwords don't match!";
                return $('.alert').show();
            }
            $.post('/register', {
                name: this.name.trim(),
                email: email,
                sha1_password: sha1(email + ':' + this.password1)
            }, function() {
                return location.assign('/');
            });
        }
    }
});