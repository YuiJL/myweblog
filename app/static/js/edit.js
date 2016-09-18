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
            var id = location.search.split('?id=').pop();
            self.url = self.url + '/' + id;
            $.getJSON('/api/blogs/' + id, function(blog) {
                self.blog = blog;
                var a = self.blog.tag;
                self.blog.tag = a.join(' ');
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