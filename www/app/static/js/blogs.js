new Vue ({
    el: '#home',
    methods: {
        viewmode: function(path) {
            $.ajax('/' + path, {
                method: "POST"
            }).done(function() {
                return location.assign(location.pathname);
            })
        }
    }
})