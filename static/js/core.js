$(document).ready(function () {
    $('a.model').click(function () {
        var url = $(this).attr('href');
        $.getJSON(url, function (data) {
            $('table#data').remove();
            var $data_table = $('<table id="data"></table>');

            var $tr = '<tr>';
            $.each(data['field_verbose_names'], function (indx, value) {
                $tr += '<th>' + value + '</th>';
            });

            $tr += '</tr>';
            $data_table.append($tr);

            $.each(data['items'], function (indx, item_vals) {
                var $tr = '<tr class="item">';
                $.each(item_vals, function (indx, val) {
                    $tr += '<td>' + val + '</td>';
                });
                $tr += '</tr>';
                $data_table.append($tr);
            });
            $('table#models').after($data_table);
        });
        return false;
    });
});