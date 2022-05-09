$(document).ready(function () {
    var idFilters = "#filters"

    //If shown.bs.collapse add the unique id to local storage
    $(idFilters).on("shown.bs.collapse", function () {
        localStorage.setItem("show_collapse_" + this.id, true);
    });
    //If hidden.bs.collaspe remove the unique id from local storage
    $(idFilters).on("hidden.bs.collapse", function () {
        localStorage.removeItem("show_collapse_" + this.id);
    });
    //If the key exists and is set to true, show the collapsed, otherwise hide
    $(idFilters).each(function () {
        if (localStorage.getItem("show_collapse_" + this.id) == "true") {
            $(this).collapse("show");
        }
        else {
            $(this).collapse("hide");
        }
    });
});
