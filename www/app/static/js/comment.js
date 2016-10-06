function blackMagic(tag, mode) {
    if (mode === 1) {
        var it = $(tag).parent().find('form');
        if (it.hasClass('replybox')) {
            if (vm.subcomment !== '') {
                vm.subcomment = '';
            } else {
                it.removeClass('replybox');
            }
        }
        $('.replybox').hide();
        $('.replybox').removeClass('replybox');
        it.addClass('replybox');
    } else {
        var it = $(tag).parent().parent().parent().find('form');
        if (!it.hasClass('replybox')) {
            $('.replybox').hide();
            $('.replybox').removeClass('replybox');
            it.addClass('replybox');
        }
    }
}

new Vue({
    el: '#commentsignin',
    methods: {
        clear: function() {
            base.email = '';
            base.password = '';
            base.message = '';
            $('#error').hide();
        }
    }
})

var vm = new Vue({
    el: '#control',
    data: {
        id: location.pathname.split('/').pop(),
        subcomment: '',
        comment: '',
        comments: [],
        path: '',
        image: ''
    },
    filters: {
        datetime: function(value) {
            var d = new Date(value*1000);
            var dateString = d.toString().split(' ');
            return dateString[1] + ' ' + dateString[2] + ', ' + dateString[3] + ', ' + dateString[4] + ' ' + dateString[6];
        },
        count: function(data) {
            return data.length;
        },
        getIndex: function(value, length) {
            return "#" + (length - value).toString();
        }
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/blogs/' + self.id + '/comments', function(data) {
            self.comments = data.comments;
        });
        $("#navbarleft li:first-child").removeClass("active");
    },
    methods: {
        submit: function() {
            var self = this;
            $.ajax('/api/blogs/' + self.id + '/comments', {
                data: {content: self.comment},
                method: "POST"
            }).done(function(data) {
                self.comment = '';
                self.comments = data.comments;
            });
        },
        reply: function(mode) {
            var self = this;
            $('.replybox').hide();
            self.path = $('.replybox textarea').attr('name');
            $.ajax('/api/blogs/' + self.id + '/comments/' + self.path, {
                data: {content: self.subcomment},
                method: "POST"
            }).done(function(data) {
                self.subcomment = '';
                self.comments = data.comments;
            });
        },
        replyBox: function(id, length, mode, name) {
            var self = this;
            if (mode === 1) {
                $('.replybox').toggle();
                self.subcomment = '';
            } else {
                $('.replybox').show();
                self.subcomment = 'RE @' + name + ': ';
            }
            $('.replybox textarea').attr('name', id);
            $('.replybox textarea').attr('placeholder', 'Write a reply to ' + "#" + (self.comments.length - length).toString());
        },
        delete: function(item) {
            var self = this;
            $.ajax('/api/comments/' + item._id + '/delete', {
                method: "POST"
            }).done(function(data) {
                self.comments = data.comments;
            });
        },
        delete_one: function(item, comment) {
            var self = this;
            $.ajax('/api/comments/' + item._id + '/delete/' + comment._id, {
                method: "POST"
            }).done(function(data) {
                self.comments = data.comments;
            });
        }
    }
});