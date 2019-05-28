$(document).ready(function() {
	
	
	$('input#join').click( function () {
		$('form').submit( function(e) {
			e.preventDefault();
		});
		
		var name = $('#groupname').val();
		var pwd = $('#grouppassword').val();
		
		$.ajax({
			url: '/spew/joingroup',
			data: {
				'name': name,
				'pwd': pwd
			},
			dataType: 'json',
			success: function (data) {
				console.log(data)
				if (data.success == 0) {
					console.log(window.location)
					console.log(window.location.origin)
					window.location = window.location.origin + "/spew"
				}
				else {
					//display error
					$('#group-form p').remove()
					$('#groupname').value = ''
					$('#groupname').after('<p style="color:red">' + data.message + '</p>')
				}
			}
		});
	});
	
	$('input#create').click( function () {
		$('form').submit( function(e) {
			e.preventDefault();
		});
		
		var name = $('#groupname').val();
		var pwd = $('#grouppassword').val();
		
		$.ajax({
			url: '/spew/creategroupsetup',
			data: {
				'name': name,
				'pwd': pwd
			},
			dataType: 'json',
			success: function (data) {
				
				if(data.success == 0) {
					$('#group-form p').remove()
					$('#confirmgrouppassword').show()
					$('#join').hide()
					$('#create').hide()
					$('#final-create').show()
					$('#cancel').show()
					
				}
				else {
					//display error
					$('#group-form p').remove()
					$('#groupname').value = ''
					$('#groupname').after('<p style="color:red">' + data.message + '</p>')
				}
			}
		});
	});
	
	$('#group-form').on('click', '#final-create', function () {
		name = $('#groupname').val();
		pwd = $('#grouppassword').val();
		confirmpwd = $('#confirmgrouppassword').val();
		
		if(pwd == confirmpwd)
		{
			$.ajax({
				url: '/spew/creategroup',
				data: {
					'name': name,
					'pwd': pwd
				},
				dataType: 'json',
				success: function (data) {
					console.log(data)
					if (data.success == 0) {
						console.log(window.location)
						console.log(window.location.origin)
						window.location = window.location.origin + "/spew"
					}
					//display error
					$('#group-form p').remove()
					$('#groupname').value = ''
					$('#groupname').after('<p style="color:red">' + data.message + '</p>')
				}
			});
		}
		else {
			//display error
			$('#group-form p').remove() 
			$('#grouppassword').value = ''
			$('#confirmgrouppassword').value = ''
			$('#confirmgrouppassword').after('<p style="color:red">passwords do not match</p>')
		}
	});
	
	$('#group-form').on('click', '#cancel', function () {
		$('#group-form p').remove()
		$('#group-form input').value = ''
		$('#confirmgrouppassword').show()
		$('#join').show()
		$('#create').show()
		$('#final-create').hide()
		$('#cancel').hide()
	});
	
})