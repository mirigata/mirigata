// display dialog for non-existing features
$(function() {
    var $body = $("main");

    $("a[data-feature]").click(function() {
        var $el = $(this);

        var $card = $("<div class='mdl-card mdl-shadow--2dp card-coming-soon'>" +
            "<div class='mdl-card__title'><h2 class='mdl-card__title-text'>Coming soon</h2></div>" +
            "<div class='mdl-card__supporting-text'> " +
            "The feature '" + $el.data('feature') + "' is not yet implemented. You can follow the latest " +
            "developments on <a href='http://livecoding.tv/publysher'>Livecoding.tv</a>. " +
            "</div>" +
            "<div class='mdl-card__actions mdl-card--border'> <a class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'>OK</a> </div>" +
            "</div>");

        var $old = $body.children();

        $card.find("a").click(function() {
            $body.append($old);
            $card.remove();
        });

        $old.detach();
        $body.append($card);
    });
});


// move labels to placeholders
$(function() {
    $(".control-label").each(function() {
        var $label = $(this);
        var $input = $(this).parent().find("input");

        if (!$input.length) {
            return;
        }

        var text = $label.text().trim().replace('*', '');
        $input.attr("placeholder", text);

        $label.remove();
    });
});
