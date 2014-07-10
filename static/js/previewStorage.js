function save_settings(){
    sessionStorage.setItem("title", $("#title").val());
}

$(function(){
    $('form#blog_data').submit(function(event){
        event.preventDefault();
        save_settings();
        window.location.href = document.URL + "preview/";
    });
});
