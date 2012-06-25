/*Å@*/
$(document).ready(function() {
	$("#dogform").validate({
		rules: {
			kaisaibi: {
				required: true,
				dateISO: true
			}
		}
	});
});
