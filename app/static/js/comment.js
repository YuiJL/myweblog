new Vue({
    el: '#main',
    data: {
        id: location.pathname.split('/').pop(),
        comment: '',
        comments: []
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/blogs/' + self.id + '/comments', function(data) {
            self.comments = data.comments;
        });
    },
    methods: {
        submit: function() {
            var self = this;
            $.ajax('/api/blogs/' + self.id + '/comments', {
                data: {content: self.comment},
                method: "POST"
            }).done(function(data) {
                self.comment = '';
                self.comments = data.comments.concat(self.comments);
            });
        }
    }
});