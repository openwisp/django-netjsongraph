window.initTopologyHistory = function($){
    var datepicker = $('#njg-datepicker'),
        today = new Date(),
        apiUrl = datepicker.attr('data-history-api');
    today.setHours(0, 0, 0, 0);
    datepicker.datepicker({dateFormat: 'dd/mm/yy'});
    datepicker.datepicker('setDate', today);
    datepicker.change(function() {;
        var date = datepicker.val().split('/').reverse().join('-'),
            url = apiUrl + '?date=' + date;
        // load latest data when looking currentDate
        if(datepicker.datepicker('getDate').getTime() == today.getTime()){
            url = undefined
        }
        window.graph = window.loadNetJsonGraph(url);
    });
};
