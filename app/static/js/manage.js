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
        }
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/' + self.collection, function(data) {
            self.collections = data[self.collection];
        });
    }
});