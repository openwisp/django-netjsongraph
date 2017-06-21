(function($) {
    $(document).ready(function() {
        var strategy = $('#id_strategy'),
            fetch_rows = $('#id_url').parents('.form-row'),
            receive_rows = $('#id_key, #id_expiration_time, #id_receive_url').parents('.form-row');
        strategy.change(function(e){
            if (strategy.val() == 'fetch'){
                fetch_rows.show();
                receive_rows.hide();
            }
            else{
                fetch_rows.hide();
                receive_rows.show();
            }
        });
        strategy.trigger('change');
    });
})(django.jQuery);
