jQuery.extend(jQuery.validator.messages, {
	required: "必須項目です",
});
$(function(){
	$('#dogform').validate();
});
$(function(){
	$('.limited').maxlength({
		'feedback' : '.charsLeft' //残り数を表示する場所
	});
});
