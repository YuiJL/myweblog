new Vue({
    el: '#main',
    data: {
        id: location.pathname.split('/').pop(),
        comment: '',
        comments: []
    },
    filters: {
        datetime: function(value) {
            var d = new Date(value*1000);
            var dateString = d.toString().split(' ');
            return dateString[1] + ' ' + dateString[2] + ', ' + dateString[3] + ', ' + dateString[4] + ' ' + dateString[6];
        },
        count: function(data) {
            return data.length;
        }
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
                self.comments = data.comments;
            });
        }
    }
});