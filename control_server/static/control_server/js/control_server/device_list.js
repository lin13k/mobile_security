function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
    	var value = $.trim(cookies[i]);
        if (value.startsWith("csrftoken=")) {
            return value.substring("csrftoken=".length, value.length);
        }
    }
    return "unknown";
}

function selectHandler(imei) {
	var e = document.getElementById('device_assign_'+imei);
	var value = e.options[e.selectedIndex].value;
	var text = e.options[e.selectedIndex].text;
	console.log(imei,value);
	assignDriver(imei, value);
}


function success(argument) {
	location.reload();
}


function assignDriver(imei, mode) {
	var payload = {"alarm_type":mode};
	$.ajax({
        url: '/sync/' + imei + '/',
        datatype: 'json',
        contentType: "application/json",
        type: 'PUT',
        success: success,
        data: JSON.stringify(payload)
    });
}