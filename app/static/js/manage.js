new Vue({
    el: '#manage',
    data: {
        collection: location.pathname.split('/').pop(),
        collections: []
    },
    filters: {
        datetime: function(value) {
            var d = new Date(value*1000);
            var dateString = d.toString().split(' ');
            return dateString[1] + ' ' + dateString[2] + ', ' + dateString[3] + ', ' + dateString[4] + ' ' + dateString[6];
        },
        summary: function(value) {
            var omit = '';
            if (value.length > 40) {
                omit = '...';
            }
            return value.toString().substr(0, 40) + omit;
        }
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/' + self.collection, function(data) {
            self.collections = data[self.collection];
        });
        $("#navbarleft li:first-child").removeClass("active");
        $("#navbarleft li:nth-child(2)").addClass("active");
    },
    methods: {
        delete: function(item) {
            var self = this;
                $.ajax('/api/' + self.collection + '/' + item._id + '/delete', {
                    method: "POST"
                }).done(function() {
                    self.collections.$remove(item);
                });
        }
    }
});