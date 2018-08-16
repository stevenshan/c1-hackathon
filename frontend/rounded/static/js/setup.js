$(function(){
    $(".multistep-form").each(setupMultistepForm);
});

function setupMultistepForm() {
    var form = $(this);
    var pages = form.find(".tab-pane");
    var pages_ = pages.toArray();
    var page = 0;

    var tabIndicator = $(
        '<div class="tab-indicator"></div>'
    );
    var indexIndicator = $(
        '<div class="index-indicator"></div>'
    );
    tabIndicator.prepend(indexIndicator);

    var showPage = (index) => {
        if (pages.length <= index || index < 0) {
            return;
        }

        pages.css("display", "none");
        $(pages_[index]).css("display", "");

        indexIndicator.html("Step " + (index + 1));
        var labels = pages_.slice(0, index + 1);

        tabIndicator.find(".label").remove();
        for (var i in labels) {
            var label = $(pages_[i]).attr("label");
            if (label == undefined) {
                label = parseInt(i) + 1 + "";
            }
            tabIndicator.append('<div class="label">' + label + '</div>')
        }
    };

    var init = () => {
        form.prepend(tabIndicator);

        pages.each(function(i){
            var navButtons = $(
                '<div class="tab-nav-bar"></div>'
            );

            if (i > 0) {
                var prevButton = $(
                    '<div class="button previous">Previous</div>'
                );
                prevButton.click(() => showPage(i - 1));
                navButtons.append(prevButton);
            }

            if (i < pages.length - 1 && pages.length > 0) {
                var nextButton = $(
                    '<div class="button next">Next</div>'
                );
                nextButton.click(() => showPage(i + 1));
                navButtons.append(nextButton);
            }

            if (i == pages.length - 1) {
                var submitButton = $(
                    '<div class="button submit">Submit</div>'
                );
                navButtons.append(submitButton);
            }


            navButtons.append(nextButton);

            $(this).append(navButtons);

        });

        showPage(1);
    };

    init();

};