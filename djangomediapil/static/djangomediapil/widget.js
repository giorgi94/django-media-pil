
function imgLoaded (event) {
    var el = event.target;
    setTimeout(function () {
        el.parentElement.style.width =
            el.getBoundingClientRect().width + 'px';
    }, 500);
}

function imgClicked (event) {
    var target = event.target.parentElement.querySelector('img');
    var id = target.id;
    var rect = target.getBoundingClientRect();
    var point = document.querySelector('#' + id + '-point');
    var el_json = document.querySelector('#' + id.replace(/-img$/, '-json'));
    var el_json_value = JSON.parse(el_json.value);

    el_json_value.point = [
        Math.floor(100 * (event.clientX - rect.left) / rect.width),
        Math.floor(100 * (event.clientY - rect.top) / rect.height)
    ];

    point.style.left = el_json_value.point[0] + '%';
    point.style.top = el_json_value.point[1] + '%';

    el_json.value = JSON.stringify(el_json_value);
}

function changeURL (event) {
    var id = event.target.id;
    var url_prefix = event.target.dataset.url;
    var el_json = document.querySelector('#' + id + '-json');
    var el_img = document.querySelector('#' + id + '-img');
    var el_box = el_img.parentElement.parentElement;

    if (event.target.value) {
        el_img.src = url_prefix + event.target.value;
        el_box.style.display = 'block';
    } else {
        el_img.src = '';
        el_box.style.display = 'none';
    }

    var el_json_value = JSON.parse(el_json.value);
    el_json_value.pathway = event.target.value;
    el_json_value.url = url_prefix + event.target.value;
    el_json.value = JSON.stringify(el_json_value);
}

function previewUpload (event, upload_to) {
    var id = event.target.id.replace('-upload', '');
    var el = document.querySelector('#' + id);
    var el_json = document.querySelector('#' + id + '-json');
    var el_img = document.querySelector('#' + id + '-img');
    var el_box = el_img.parentElement.parentElement;

    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        el_img.src = e.target.result;
        el.value = upload_to + '/' + file.name;
        el_box.style.display = 'block';

        var url_prefix = event.target.dataset.url;
        var el_json_value = JSON.parse(el_json.value);
        el_json_value.pathway = el.value;
        el_json_value.url = url_prefix + el.value;
        el_json.value = JSON.stringify(el_json_value);
    };
    reader.readAsDataURL(file);
}

function openMediaManager (target) {
    var url = `${window.__MEDIA_MANAGER_PATH__}`;
    var myWindow = window.open(url, 'Media Manager', 'width=1000,height=500');
    myWindow.target = target;
}
