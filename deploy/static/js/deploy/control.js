function start(deploy_id, csrf_token) {
	console.log(`Attempting to start deployment with ID ${deploy_id}`)
	$.ajax({
		url: `/deploy/api/${deploy_id}/`,
		type: 'PUT',
		dataType: 'json',
		contentType: "application/json",
		data: JSON.stringify({
			"actions": ["start", "stop"]
		}),
		beforeSend: xhr => {
			xhr.setRequestHeader("X-CSRFToken", csrf_token)
		}
		// beforeSend: xhr => {
		// 	xhr.setRequestHeader(
		// 		"Authorization",
		// 		"JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1MTEyMDA2LCJpYXQiOjE3MzUwMjU2MDYsImp0aSI6ImQ2YzcyMWNhYzIxZDRlNjJiMWMyYzYzMGQ1MzRjMDIwIiwidXNlcl9pZCI6MX0.XWCwILNGI80uA6IhnaJSTuYkH8M87ZmAYeyZJl2TeYA"
		// 	)
		// }
	})
}