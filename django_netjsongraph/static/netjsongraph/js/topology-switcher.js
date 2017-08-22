$(function() {
    $('#dp').datepicker();
    d = new Date();
    month = d.getMonth() + 1;
    day = d.getDate();
    default_date = (month<10? '0':'') + month + '/' +
        (day<10? '0':'') + day + '/' +
        d.getFullYear();
    $('#dp').val(default_date);
    current_date = d.getFullYear() + '-' +
        (month<10? '0':'') + month + '-' +
        (day<10? '0':'') + day;
    $('#submit').click(function() {
        query_date = $('#dp').val();
        date = query_date.split('/').reverse();
        if(date != []){
            var x = date[1];
            date[1] = date[2];
            date[2] = x;
        }
        date = date.join('-');
        graph_url = $('.switcher').attr('graph-url') + '?date=' + date;
        if(current_date == date){
            graph_url = window.location.href;
        }
        body = $('body');
        $.get(graph_url, function(html) {
            body.html(html);
            $('#dp').val(query_date);
        });
    });
});
