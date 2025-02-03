$.fn.select2.defaults.set("theme", "bootstrap-5");

$(window).ready(function() {
    // Show page content after loading
    $('.loading-progress').remove();
    $('.container').css('visibility', 'visible');
});

$(document).ready(function() {
    // Hide notification messages
    $(".alert").delay(5000). animate(
        {height:"toggle", opacity:"toggle"},
        1000
    );
});

$(document).ready(function () {
    // Highlight current position in navbar
    var pathname = window.location.pathname;

    $('#navbarMainNavigation a').filter(function() {
        return this.pathname == pathname;
    }).addClass('active');

    $('#navbarMainNavigation a').filter(function() {
        return this.pathname != pathname;
    }).removeClass('active');
});
