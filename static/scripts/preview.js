window.addEventListener('load', function () {
    var fields = [source_url, extract_css_selector, title_regex, content_regex, ignore_bozo];

    preview_button.addEventListener('click', function (e) {
        setPreviewState('disabled');

        if (form.checkValidity()) {
            var params = [];

            fields.forEach(function (field) {
                if (field.type != 'checkbox' || field.checked) {
                    params.push(encodeURIComponent(field.name) + '=' + encodeURIComponent(field.value));
                }
            });

            var url = preview_action_url.value + '?' + params.join('&');
            preview.location.replace(url);
            setPreviewState('loading');

            e.preventDefault();
        }
    });

    fields.forEach(function (field) {
        field.addEventListener('change', function (e) {
            preview.location.replace('about:blank');
        });
    });

    slug.addEventListener('keydown', function (e) {
        if (e.keyCode == 13) { // Because browsers can't seem to agree on a unified API here :(
            e.preventDefault();
            save.click();
        }
    });


    document.getElementById('preview').addEventListener('load', function () {
        setPreviewState('loaded');
        try {
            if (preview.location.href == 'about:blank') {
                setPreviewState('disabled');
            }
        } catch (e) {
        }
    });

    function setPreviewState(newState) {
        ['disabled', 'loading', 'loaded'].forEach(function (oldState) {
            munched_section.classList.remove('munched-' + oldState);
        });
        munched_section.classList.add('munched-' + newState);

        ['fa-refresh', 'fa-spin', 'fa-check-circle'].forEach(function (oldIcon) {
            preview_status_icon.classList.remove(oldIcon);
        });
        switch (newState) {
            case 'disabled':
                slug.required = false;
                break;

            case 'loading':
                preview_status_icon.classList.add('fa-refresh');
                preview_status_icon.classList.add('fa-spin');
                slug.required = false;
                slug.disabled = true;
                save.disabled = true;
                break;

            case 'loaded':
                preview_status_icon.classList.add('fa-check-circle');
                slug.required = true;
                slug.disabled = false;
                save.disabled = false;
                break;
        }
    }
});