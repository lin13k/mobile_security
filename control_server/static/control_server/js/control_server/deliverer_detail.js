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

function success(argument) {
	location.reload();
}

function changeStatus(orderId, status) {
	var payload = {
		"order":orderId, "csrfmiddlewaretoken":getCSRFToken(),
		"status":status
	};
	$.ajax({
        url: '/dashboard/change_status/',
        datatype: 'json',
        type: 'POST',
        success: success,
        data: payload
    });
}
