function validEmail(email) {
    var re = /^[\w\.\-]+\@[\w\-]+(\.[\w\-]+){1,4}$/;
    return re.test(email);
}

new Vue({
    el: '#signupform',
    data: {
        name: '',
        email: '',
        pw1: '',
        pw2: '',
        message: ''
    },
    ready: function() {
        $("#navbarleft li:first-child").removeClass("active");
        $("#last").addClass("active");
    },
    methods: {
        register: function() {
            this.email = this.email.trim();
            var self = this;
            if (!validEmail(this.email)) {
                this.message = "Please enter a valid e-mail address!";
                return $('.alert').show();
            }
            if (this.pw1.length < 6) {
                this.message = "Password must be at least 6 characters!";
                return $('.alert').show();
            }
            if (this.pw1 !== this.pw2) {
                this.message = "Passwords don't match!";
                return $('.alert').show();
            }
            $.ajax('/register', {
                data: {
                    name: self.name.trim(),
                    email: self.email,
                    sha1_password: sha1(self.email + ':' + self.pw1),
                    recaptcha: grecaptcha.getResponse()
                }, 
                method: "POST"
            }).done(function() {
                return location.assign('/');
            }).fail(function(xhr) {
                self.message = xhr.responseText;
                return $('.alert').show();
            });
        }
    }
})