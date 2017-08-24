window.initTopologyHistory = function($){
    $('#dp').datepicker();
    var d = new Date(),
        month = d.getMonth() + 1,
        day = d.getDate(),
        defaultDate = (month < 10 ? '0' : '') + month + '/' +
                      (day < 10 ? '0' : '') + day + '/' + d.getFullYear(),
        currentDate = d.getFullYear() + '-' + (month < 10 ? '0' : '') +
                      month + '-' + (day < 10 ? '0' : '') + day;
    $('#dp').val(defaultDate);
    $('#submit').click(function() {
        var queryDate = $('#dp').val(),
            date = queryDate.split('/').reverse(),
            graphUrl;
        if(date != []){
            var x = date[1];
            date[1] = date[2];
            date[2] = x;
        }
        date = date.join('-');
        graphUrl = $('.switcher').attr('data-history-api') + '?date=' + date;
        // load latest data when looking currentDate
        if(currentDate == date){ graphUrl = undefined }
        window.graph = window.loadNetJsonGraph(graphUrl);
    });
};
