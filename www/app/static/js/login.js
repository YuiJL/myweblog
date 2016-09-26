// enable tab key in textarea
$("textarea").keydown(function(e) {
    if(e.keyCode === 9) {
        var start = this.selectionStart;
        var end = this.selectionEnd;
        var $this = $(this);
        var value = $this.val();
        $this.val(value.substring(0, start)
                    + "    "
                    + value.substring(end));
        this.selectionStart = this.selectionEnd = start + 4;
        e.preventDefault();
    }
});

$(document).ready(function() {
    $("#change").click(function() {
        $("#upload").fadeToggle('fast');
    });
    $("#control").click(function() {
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