$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_code').attr('autocomplete', 'off');
        $('#id_description').attr('autocomplete', 'off');

        // Add frorm-control bootstrap classes
        const field_list = ['#id_code', '#id_description', '#id_books_0', '#id_books_1', ]
        field_list.forEach(function(item) {$(item).addClass('form-control')})

        $('#id_books_1').wrap('<div class="input-group-append"></div>')

        // Enable select2 on fields
        var current_language = $("select[id='id_global_language']").val();

        $("#id_books_1").select2({
            minimumResultsForSearch: Infinity,
            width: 'style',
        });

        $("#id_description").select2({
            language: current_language,
        });
    }
);
