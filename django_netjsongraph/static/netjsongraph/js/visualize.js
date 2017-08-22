django.jQuery(function($) {
    var overlay = $('.djnjg-overlay'),
        body = $('body'),
        inner = overlay.find('.inner'),
        visualize_url = $('.visualizelink').attr('data-url');

    var d = new Date(),
        month = d.getMonth() + 1,
        day = d.getDate(),
        default_date = (month < 10 ? '0': '') + month + '/' +
            (day < 10 ? '0': '') + day + '/' +
            d.getFullYear(),
        current_date = d.getFullYear() + '-' +
            (month < 10 ? '0': '') + month + '-' +
            (day < 10 ? '0': '') + day;

    var openOverlay = function() {
        // show overlay
        $.get(visualize_url, function(html) {
            inner.html(html);
            $('svg').appendTo(inner);
            $('.njg-overlay').appendTo(inner);
            $('.njg-metadata').appendTo(inner);
            overlay.show();
            body.css('overflow', 'hidden');
            inner.css('overflow', 'hidden');
            overlay.find('.close').click(function(e){
                e.preventDefault();
                closeOverlay();
            })
            overlay.find('#dp').val(default_date);
            overlay.find('#submit').click(function(e){
                e.preventDefault();
                getTopologyHistory();
            })
        })
        .error(function(xhr) {
            if (xhr.status == 400) {
                $('#content-main form').trigger('submit');
            }
            else {
                var message = 'Error while generating network topology graph';
                if (gettext) { message = gettext(message); }
                alert(message + ':\n\n' + xhr.responseText);
            }
        });
        $(document).keydown(disableArrowKeys);
    };

    var closeOverlay = function () {
        $(document).unbind('keydown', disableArrowKeys);
        inner.html('');
        overlay.hide()
        body.attr('style', '');
    };

    $('.visualizelink').click(function(e){
        openOverlay();
    });

    $(document).keyup(function(e) {
        // ALT+P
        if (e.altKey && e.which == 80) {
            // unfocus any active input before proceeding
            $(document.activeElement).trigger('blur');
            // corresonding raw value before proceding
            setTimeout(openOverlay, 15);
        }
        // ESC
        else if (!e.ctrlKey && e.which == 27) {
            closeOverlay();
        }
    });

    var disableArrowKeys = function(e) {
        var ar = new Array(37, 38, 39, 40);
        if ($.inArray(e.keyCode, ar)>=0){
            e.preventDefault();
        }
    }

    var getTopologyHistory = function(e) {
        query_date = $('#dp').val();
        date = query_date.split('/').reverse();
        if(date != []){
            var x = date[1];
            date[1] = date[2];
            date[2] = x;
        }
        date = date.join('-');
        graph_url = $('.switcher').attr('graph-url') + '?date=' + date;
        if(date == current_date) graph_url = visualize_url;
        $.get(graph_url, function(html) {
            inner.html(html);
            $('svg').appendTo(inner);
            $('.njg-overlay').appendTo(inner);
            $('.njg-metadata').appendTo(inner);
            overlay.find('#dp').val(query_date);
            overlay.show();
            body.css('overflow', 'hidden');
            inner.css('overflow', 'hidden');
            overlay.find('.close').click(function(e){
                e.preventDefault();
                closeOverlay();
            })
            overlay.find('#submit').click(function(e){
                e.preventDefault();
                getTopologyHistory();
            })
        })
    }
});
