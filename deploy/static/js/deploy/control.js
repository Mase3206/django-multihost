function start(deploy_id, csrf_token) {
	console.log(`Attempting to start deployment with ID ${deploy_id}`)
	$.ajax({
		url: `/deploy/api/${deploy_id}/`,
		type: 'PUT',
		dataType: 'json',
		contentType: "application/json",
		data: JSON.stringify({
			"actions": ["start"]
		}),
		beforeSend: xhr => {
			xhr.setRequestHeader("X-CSRFToken", csrf_token)
		}
	})
}


function stop(deploy_id, csrf_token) {
	console.log(`Attempting to stop deployment with ID ${deploy_id}`)
	$.ajax({
		url: `/deploy/api/${deploy_id}/`,
		type: 'PUT',
		dataType: 'json',
		contentType: "application/json",
		data: JSON.stringify({
			"actions": ["stop"]
		}),
		beforeSend: xhr => {
			xhr.setRequestHeader("X-CSRFToken", csrf_token)
		}
	})
}