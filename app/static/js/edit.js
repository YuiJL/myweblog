function getParamFromUrl(key) {
    var re = new RegExp('(\\?|&)' + key + '=(.*?)(&|$)');
    var result = location.search.match(re);
    return result && decodeURIComponent(result[2]);
}

new Vue({
    el: '#blog',
    data: {
        url: '/api/blogs',
        blog: {
            title: '',
            tag: '',
            content: ''
        },
        message: ''
    },
    ready: function() {
        var self = this;
        if (location.pathname.split('/').pop() === 'edit') {
            var id = getParamFromUrl('id');
            self.url = self.url + '/' + id;
            $.getJSON('/api/blogs' + id, function(blog) {
                self.blog = blog;
            });
        }
    },
    methods: {
        submit: function() {
            var self = this;
            $.ajax(self.url, {
                data: {
                    title: self.blog.title,
                    tag: self.blog.tag,
                    content: self.blog.content
                },
                method: "POST"
            }).done(function(blog) {
                return location.assign(location.pathname.split('manage')[0] + 'blog/' + blog.blog_id);
            }).fail(function(xhr) {
                self.message = xhr.responseText;
                return $('.alert').show();
            });
        }
    }
})