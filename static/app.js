$("document").ready(function() {

    var allItems = {
        "create": {
            "loading-items": [
                '#create-loading-space',
                '#create-loading-icon'
            ],
            "form-items": [
                '#create-num-sig',
                '#create-raw-data',
                '#create-btn'
            ],
            'result-items': [
                '#create-resp'
            ]
        },
        "delete": {
            "loading-items": [
                '#delete-loading-space',
                '#delete-loading-icon'
            ],
            "form-items": [
                '#delete-private-key',
                '#delete-btn'
            ],
            'result-items': [
                '#delete-resp'
            ]
        },
        "update": {
            "loading-items": [
                '#update-loading-space',
                '#update-loading-icon'
            ],
            "form-items": [
                '#update-raw-data',
                '#update-private-key',
                '.update-other-keys',
                '#update-add-private-key-btn',
                '#update-del-private-key-btn',
                '#update-btn'
            ],
            'result-items': [
                '#update-resp'
            ]
        },
        "retrieve": {
            "loading-items": [
                '#retrieve-loading-space',
                '#retrieve-loading-icon'
            ],
            "form-items": [
                '#retrieve-private-key',
                '.retrieve-other-keys',
                '#retrieve-add-private-key-btn',
                '#retrieve-del-private-key-btn',
                '#retrieve-btn'
            ],
            'result-items': [
                '#retrieve-resp'
            ]
        }
    };

    var DisableValAllItem = function(idArrays, disabled) {
        idArrays.forEach(function(idName) {
            $(idName).each(function() {
                $(this).attr("disabled", disabled);
            });
       });
    };

    var HideValAllItem = function(idArrays, hide) {
        idArrays.forEach(function(idName) {
            if (true === hide) {
                $(idName).hide();
            } else {
                $(idName).show();
            }
        });
    };

    var UpdateCreateResp = function(resp) {
        $('#create-my-private-key').text(resp.my_private_key);
        for (var key in resp.others_private_key) {
            var elementKey = '<td>' + key + '</td>';
            var elementVal = '<td>' + resp.others_private_key[key] + '</td>';
            $('#create-other-private-keys-table tr:last').after('<tr>' + elementKey + elementVal + '</tr>');
        }
    };

    HideValAllItem(allItems.create['loading-items'], true);
    HideValAllItem(allItems.create['result-items'], true);
    HideValAllItem(allItems.delete['loading-items'], true);
    HideValAllItem(allItems.delete['result-items'], true);
    HideValAllItem(allItems.retrieve['loading-items'], true);
    HideValAllItem(allItems.retrieve['result-items'], true);
    HideValAllItem(allItems.update['loading-items'], true);
    HideValAllItem(allItems.update['result-items'], true);

    $("#create-form").submit(function(e) {
        e.preventDefault();

        DisableValAllItem(allItems.create['form-items'], true);
        HideValAllItem(allItems.create['loading-items'], false);

        var num_sig = $("#create-num-sig").val();
        var raw_data = $("#create-raw-data").val();

        $.post("will/create", {
            "num_sig": num_sig,
            "raw_data": raw_data
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateCreateResp(resp);
            DisableValAllItem(allItems.create['form-items'], false);
            HideValAllItem(allItems.create['loading-items'], true);
            HideValAllItem(allItems.create['result-items'], false);
        });
    });

    $(document).on('click', '#retrieve-add-private-key-btn', function(e) {
        e.preventDefault();

        var controlForm = $(this).parents('.form-group');
        var currentEntry = $(this).parents('.retrieve-private-entry:first').clone();
        var newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.retrieve-private-entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .attr('id', 'retrieve-del-private-key-btn')
            .html('<div class="fa fa-minus"></div>');

    }).on('click', '#retrieve-del-private-key-btn', function(e) {
        e.preventDefault();
        $(this).parents('.retrieve-private-entry:first').remove();
    });
    var ComposeSelectOtherPrivateKeys = function() {
        var otherPrivateKeysDict = {};
        var idx = 0;
        $(".retrieve-private-entry").each(function() {
            otherPrivateKeysDict[idx] = $(this).find(".form-control").val();
            idx++;
        });
        return otherPrivateKeysDict;
    };

    var UpdateRetrieveResp = function(resp) {
        $('#retrieve-raw-data').text(resp.raw_data);
        HideValAllItem(allItems.retrieve['result-items'], false);
    };

    $("#retrieve-form").submit(function(e) {
        e.preventDefault();
        DisableValAllItem(allItems.retrieve['form-items'], true);
        HideValAllItem(allItems.retrieve['loading-items'], false);

        var my_private_key = $("#retrieve-private-key").val();
        var others_private_key = ComposeSelectOtherPrivateKeys();

        $.post("will/retrieve", {
            "my_private_key": my_private_key,
            "others_private_key": JSON.stringify(others_private_key)
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateRetrieveResp(resp);
            DisableValAllItem(allItems.retrieve['form-items'], false);
            HideValAllItem(allItems.retrieve['loading-items'], true);
        });
    });


    var UpdateDeleteResp = function(resp) {
        $('#delete-status').text('OK');
        HideValAllItem(allItems.delete['result-items'], false);
    };

    $("#delete-form").submit(function(e) {
        e.preventDefault();
        DisableValAllItem(allItems.delete['form-items'], true);
        HideValAllItem(allItems.delete['loading-items'], false);

        var my_private_key = $("#delete-private-key").val();

        $.post("will/delete", {
            "my_private_key": my_private_key
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateDeleteResp(resp);
            DisableValAllItem(allItems.delete['form-items'], false);
            HideValAllItem(allItems.delete['loading-items'], true);
        });
    });


    $(document).on('click', '#update-add-private-key-btn', function(e) {
        e.preventDefault();

        var controlForm = $(this).parents('.form-group');
        var currentEntry = $(this).parents('.update-private-entry:first').clone();
        var newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.update-private-entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .attr('id', 'update-del-private-key-btn')
            .html('<div class="fa fa-minus"></div>');

    }).on('click', '#update-del-private-key-btn', function(e) {
        e.preventDefault();
        $(this).parents('.update-private-entry:first').remove();
    });
    var ComposeUpdateOtherPrivateKeys = function() {
        var otherPrivateKeysDict = {};
        var idx = 0;
        $(".update-private-entry").each(function() {
            otherPrivateKeysDict[idx] = $(this).find(".form-control").val();
            idx++;
        });
        return otherPrivateKeysDict;
    };

    var UpdateUpdateResp = function(resp) {
        $('#update-status').text('OK');
        HideValAllItem(allItems.update['result-items'], false);
    };

    $("#update-form").submit(function(e) {
        e.preventDefault();
        DisableValAllItem(allItems.update['form-items'], true);
        HideValAllItem(allItems.update['loading-items'], false);

        var raw_data = $("#update-raw-data").val();
        var my_private_key = $("#update-private-key").val();
        var others_private_key = ComposeUpdateOtherPrivateKeys();

        $.post("will/update", {
            'raw_data': raw_data,
            "my_private_key": my_private_key,
            "others_private_key": JSON.stringify(others_private_key)
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateUpdateResp(resp);
            DisableValAllItem(allItems.update['form-items'], false);
            HideValAllItem(allItems.update['loading-items'], true);
        });
    });
});
