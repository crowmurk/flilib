$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_authors').attr('autocomplete', 'off')
        $('#id_title').attr('autocomplete', 'off')

        // Add frorm-control bootstrap classes
        const field_list = ['#id_authors', '#id_title', '#id_genres', '#id_language', '#id_libraryrate_0', '#id_libraryrate_1', '#id_deleted',]
        field_list.forEach(function(item) {$(item).addClass('form-control')})

        $('#id_libraryrate_1').wrap('<div class="input-group-append"></div>')

        // Enable select2 on fields
        var current_language = $("select[id='id_global_language']").val();

        $("#id_genres").select2({
            language: current_language,
        });
        $("#id_language").select2({
            language: current_language,
        });
        $("#id_libraryrate_1").select2({
            minimumResultsForSearch: Infinity,
            width: 'style',
        });
        $("#id_deleted").select2({
            minimumResultsForSearch: Infinity,
            width: 'style',
        });
    }
);
