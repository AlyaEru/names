$(document).ready(function() {
	//var names = ['Biffy','Daniel','Adam','Corrie'];
	//var advectives = ['fat','googly','freakish','jaundiced'];
	//var nouns = ['lard','wizard','molecule','turd'];
	//insert after head a li 
	var spewNames = false;
	
	setInterval(function(){
		if(spewNames)
		{
			$.ajax({
				url: '/spew/generate',
				/*data: {
				  'um': 'not needed?'
				},*/
				dataType: 'json',
				success: function (data) {
					$('h1').after('<li class="spewing" style="color: rgb('+ (Math.floor(Math.random() * 200 + 56)).toString() +','+ (Math.floor(Math.random() * 200 + 56)).toString() +','+ (Math.floor(Math.random() * 200 + 56)).toString() +');">'+ data.sentence +'</li>');
				}
			});
			
		}
	}, 2000);
	
	$('#main').click(function() {
		if($('#spewnames').hasClass('spewon')) {
			$('#spewnames').removeClass('spewon');
			spewNames = false;
		}
		else {
			$('#spewnames').addClass('spewon');
			spewNames = true;
		}
	});
	
	$('input.cmd').click( function () {
		$('form').submit( function(e) {
			e.preventDefault();
		});
		$('#word').val($('#word').val().replace("'","`")); //fixes apostrophe bug
		var wordType = $('input[type=radio]:checked').val();
		var Word = $('#word').val();
		var command = $(this).val();
		if(command == 'add') {
			$.ajax({
				url: '/spew/newword',
				data: {
				  'word': Word,
				  'pos': wordType
				},
				dataType: 'json',
				success: function (data) {
					$('h1').after('<li class="spewing" style="color: white;">'+ data.response +'</li>');
				}
			});
		}
		if(command == 'delete') {
			$.ajax({
				url: '/spew/deleteword',
				data: {
				  'word': Word,
				  'pos': wordType
				},
				dataType: 'json',
				success: function (data) {
					$('h1').after('<li class="spewing" style="color: white;">'+ data.response +'</li>');
				}
			});
		}
		
		$('#word').val("");
	});
	$('input[value=se]').click( function() {
		if($('#word').val()=='') {
			$('#word').val('ex: [NAME] is a [ADJ] [NOUN]');
		}
		
		$('#word').click( function() {
			if($('#word').val()=='ex: [NAME] is a [ADJ] [NOUN]') {
				$(this).val('');
			}
			});
		$('input[value=se]').siblings().click( function() {
			if($('#word').val()=='ex: [NAME] is a [ADJ] [NOUN]') {
				$('#word').val('');
			}
		});
	});
	
});