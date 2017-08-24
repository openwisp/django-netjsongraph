window.initTopologyHistory = function($){
    var datepicker = $('#njg-datepicker'),
        d = new Date(),
        month = d.getMonth() + 1,
        day = d.getDate(),
        defaultDate = (month < 10 ? '0' : '') + month + '/' +
                      (day < 10 ? '0' : '') + day + '/' + d.getFullYear(),
        currentDate = d.getFullYear() + '-' + (month < 10 ? '0' : '') +
                      month + '-' + (day < 10 ? '0' : '') + day;
    datepicker.datepicker();
    datepicker.val(defaultDate);
    datepicker.change(function() {
        var queryDate = datepicker.val(),
            date = queryDate.split('/').reverse(),
            graphUrl;
        if(date != []){
            var x = date[1];
            date[1] = date[2];
            date[2] = x;
        }
        date = date.join('-');
        graphUrl = datepicker.attr('data-history-api') + '?date=' + date;
        // load latest data when looking currentDate
        if(currentDate == date){ graphUrl = undefined }
        window.graph = window.loadNetJsonGraph(graphUrl);
    });
};
