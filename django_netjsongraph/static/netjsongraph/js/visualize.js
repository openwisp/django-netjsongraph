django.jQuery(function($) {
    var overlay = $('.djnjg-overlay'),
        body = $('body'),
        inner = overlay.find('.inner'),
        visualize_url = $('.visualizelink').attr('data-url');

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
});
