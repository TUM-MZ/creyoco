var multichoice = {
    init: function () {
        "use strict";
        $(document).ready(function () {
            $(".check_multichoice").off("click").on("click", function (e) {
                var options = $(this).parent().find("input[type='radio'], input[type='checkbox']");
                var wrong = false;
                var result_el = $(this).parent().find(".result");
                $.each(options, function (n, el) {
                    $(el).next()
                        .removeClass("wrong_answer")
                        .removeClass("right_answer");
                    if ($(el).attr("data-right") === "true") {
                        $(el).next().addClass('right_answer');
                        if (!($(el).prop("checked"))) {
                            wrong = true;
                        }
                    } else {
                        if ($(el).prop("checked")) {
                            $(el).next().addClass('wrong_answer');
                            wrong = true;
                        }
                    }
                });
                if (wrong) {
                    result_el.removeClass("right")
                        .addClass("wrong")
                        .text("Incorrect answer!");
                    return false;
                } else {
                    result_el.removeClass("wrong")
                        .addClass("right")
                        .text("Correct!");
                }
            });
        });
    }
};

if (typeof(requirejs) !== "undefined") {
    define("multichoice", ['jquery'], function ($) {
        return multichoice;
    })
} else {
    multichoice.init();
}
