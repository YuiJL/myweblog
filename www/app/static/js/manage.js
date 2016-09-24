new Vue({
    el: '#control',
    data: {
        collection: location.pathname.split('/').pop(),
        collections: [],
        comment: {}
    },
    filters: {
        datetime: function(value) {
            var d = new Date(value*1000);
            var dateString = d.toString().split(' ');
            return dateString[1] + ' ' + dateString[2] + ', ' + dateString[3] + ', ' + dateString[4] + ' ' + dateString[6];
        },
        summary: function(value, limit) {
            var omit = '';
            var num = 0, count = 0;
            for (var i = 0; i < value.length; i++) {
                if (num >= limit) {
                    break;
                }
                if (value.charCodeAt(i) > 255) {
                    num += 2;
                } else {
                    num++;
                }
                count++;
            }
            if (value.length > count) {
                omit = '...';
            }
            return value.substr(0, count) + omit;
        }
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/' + self.collection, function(data) {
            self.collections = data[self.collection];
        });
        $("#navbarleft li:first-child").removeClass("active");
        $("#navbarleft li:nth-child(2)").addClass("active");
        $(".breadcrumb, #maintable").mousedown(function() {
            $("#subtable").fadeOut("fast");
        });
    },
    methods: {
        delete: function(item) {
            var self = this;
            $.ajax('/api/' + self.collection + '/' + item._id + '/delete', {
                method: "POST"
            }).done(function() {
                self.collections.$remove(item);
            });
        },
        delete_one: function(comment, item) {
            var self = this;
            $.ajax('/api/comments/' + comment._id + '/delete/' + item._id, {
                method: "POST"
            }).done(function(data) {
                self.comment.subcontent.$remove(item);
            });
        },
        show: function(id) {
            var self = this;
            $('#subtable').fadeToggle('fast');
            $.getJSON('/api/comments/' + id, function(data) {
                self.comment = data;
            });
        }
    }
});