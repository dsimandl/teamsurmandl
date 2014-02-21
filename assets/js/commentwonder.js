$(document).ready(function() {

    $("#comment form").submit(function(event){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: event.currentTarget.action,
            dataType: "json",
            data: $("#comment form").serialize(),
            success: function(data) {
                appendCommentList(data);
            }
        })
    });

    function appendCommentList(obj){
        event.preventDefault();
        var new_element = $('<h3 class="list-group-item-heading">' + obj.first_name + " " + obj.last_name + " " +
                '<small>' + obj.created_at + '</small>' + '</h3>' +
                '<p class="list-group-item-text">' + obj.comment + '</p>');
        $(".list-group").append(new_element);

    }

    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});