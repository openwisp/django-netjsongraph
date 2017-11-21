window.initTopologyHistory = function($){
    var datepicker = $('#njg-datepicker'),
        today = new Date(),
        apiUrl = datepicker.attr('data-history-api');
    var kindpicker=$("input[name='visualization_kind']");
    var kind = 'normal';
    kindpicker.change(function() {;
        kind = this.value
    });
    today.setHours(0, 0, 0, 0);
    datepicker.datepicker({dateFormat: 'dd/mm/yy'});
    datepicker.datepicker('setDate', today);
    datepicker.change(function() {;
        var date = datepicker.val().split('/').reverse().join('-'),
            url = apiUrl + '?kind=' + kind + '&date=' + date;
        // load latest data when looking currentDate
        if(datepicker.datepicker('getDate').getTime() == today.getTime()){
            url = window.__njg_default_url__;
        }
        // load latest data when looking currentDate
        $.getJSON(url).done(function(data){
            window.graph = window.loadNetJsonGraph(data);
        }).error(function(xhr){
            alert(xhr.responseJSON.detail);
        });
    });
};
