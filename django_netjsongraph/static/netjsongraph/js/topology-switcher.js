$(function() {
    $('#dp').datepicker();
    d = new Date();
    month = d.getMonth() + 1;
    day = d.getDate();
    defaultDate = (month < 10 ? '0' : '') + month + '/' +
        (day < 10 ? '0' : '') + day + '/' +
        d.getFullYear();
    $('#dp').val(defaultDate);
    currentDate = d.getFullYear() + '-' +
        (month < 10 ? '0' : '') + month + '-' +
        (day < 10 ? '0' : '') + day;
    $('#submit').click(function() {
        queryDate = $('#dp').val();
        date = queryDate.split('/').reverse();
        if(date != []){
            var x = date[1];
            date[1] = date[2];
            date[2] = x;
        }
        date = date.join('-');
        graphUrl = $('.switcher').attr('graph-url') + '?date=' + date;
        if(currentDate == date){
            graphUrl = window.location.href;
        }
        body = $('body');
        $.get(graphUrl, function(html) {
            body.html(html);
            $('#dp').val(queryDate);
        });
    });
});
